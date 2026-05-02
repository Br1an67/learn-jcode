# s05 - Provider, Auth, Session

## Goal

Understand how JCode connects different model platforms and long-running sessions.

Many agent demos reduce the provider layer to one API call. In a real product, provider integration becomes a large piece of engineering.

## Read First

```text
src/provider/
src/auth/
src/usage/
src/session/
src/storage.rs
OAUTH.md
```

Start with:

```text
src/provider/mod.rs
src/provider/dispatch.rs
src/provider/selection.rs
src/provider/openai.rs
src/provider/claude.rs
src/provider/gemini.rs
src/provider/copilot.rs
src/auth/commands.rs
src/auth/login_flows.rs
```

Do not read every provider at once. Pick one you know, such as OpenAI or Claude, and trace three lines: trait, stream event, auth.

## How to Read These Files

Open `src/provider/mod.rs` first and read the `Provider` trait plus `EventStream`. On the first pass, only inspect `complete()`, `complete_split()`, `name()`, and `model()`. The default `complete_split()` moves dynamic system context into a late synthetic message; providers such as Anthropic can override it with native cache-control behavior for static and dynamic prompt parts.

Then stay in the same file and find `MultiProvider`. Read why it implements `Provider`, then inspect `complete_with_failover()`. JCode does not scatter Claude/OpenAI/Gemini decisions throughout the agent loop. `MultiProvider` decides where the request goes and how failover works.

Next read `src/provider/dispatch.rs`. Start with `CompletionMode`, then inspect `complete_on_provider()` and `complete_split_on_provider()`. These two functions are the narrow waist of provider dispatch: JCode's uniform interface above them, concrete platform calls below them.

Then read `src/provider/selection.rs`. Look at `ActiveProvider`, `ProviderAvailability`, `auto_default_provider()`, and `parse_provider_hint()`. This answers "which provider is default?" and "how does a user hint get parsed?" Provider selection is not a small config detail; it affects startup, model switching, and session resume.

Only then pick one concrete provider. For example, in `src/provider/openai.rs`, trace how `Message`, `ToolDefinition`, and system prompt become an OpenAI request body, and how the stream comes back as JCode `StreamEvent`. Read `src/provider/claude.rs` with the same questions. Do not compare four providers at once on the first pass; field differences will drown out the architecture.

Read auth after provider dispatch. Start with `src/auth/commands.rs`; it handles command discovery, path candidates, WSL, and local environment issues. Then read `src/auth/login_flows.rs`; it handles external login commands and terminal handoff. After that, fill in the `src/cli/login/` flows. This makes the point clear: JCode auth is not "save an API key." It handles real terminal environments.

Read session last, because session depends on provider events and tool results. Start with `src/session/model.rs` and inspect `StoredMessage`, `StoredReplayEvent`, and `StoredCompactionState`. Then read `src/session/journal.rs` for journal entries and persist state. After that, read `src/session/render.rs` to see how stored state becomes displayable content again. Only then read import/replay code.

Read `OAUTH.md` after the source. Use it to check the login flow you already saw in code. If you read the doc first, it feels like login documentation; after source, you can see how it touches provider selection, sessions, and headless environments.

## Core Source Excerpts

The narrow waist of provider integration is the `Provider` trait:

```rust
// src/provider/mod.rs, excerpt
pub type EventStream =
    Pin<Box<dyn Stream<Item = Result<StreamEvent>> + Send>>;

pub trait Provider: Send + Sync {
    async fn complete(
        &self,
        messages: &[Message],
        tools: &[ToolDefinition],
        system: &str,
        resume_session_id: Option<&str>,
    ) -> Result<EventStream>;

    async fn complete_split(
        &self,
        messages: &[Message],
        tools: &[ToolDefinition],
        system_static: &str,
        system_dynamic: &str,
        resume_session_id: Option<&str>,
    ) -> Result<EventStream> {
        let dynamic_messages =
            messages_with_dynamic_system_context(messages, system_dynamic);
        self.complete(&dynamic_messages, tools, system_static, resume_session_id).await
    }
}
```

This shows the internal shape JCode wants from every provider: `Message`, `ToolDefinition`, system prompt in; `StreamEvent` out. OpenAI, Claude, and Gemini-specific formats should be absorbed behind this trait.

The default `complete_split()` also matters. It moves dynamic system context into a later synthetic message instead of mixing it into the stable system prefix. That protects provider prompt-cache stability.

Provider choice is centralized in `MultiProvider`, not scattered through the agent loop:

```rust
// src/provider/selection.rs, simplified
enum ActiveProvider {
    Claude,
    OpenAi,
    Gemini,
    Copilot,
    OpenRouter,
    OpenAiCompatible,
}

impl MultiProvider {
    fn auto_default_provider(availability: ProviderAvailability) -> ActiveProvider {
        if availability.is_configured(ActiveProvider::Claude) {
            ActiveProvider::Claude
        } else if availability.is_configured(ActiveProvider::OpenAi) {
            ActiveProvider::OpenAi
        } else {
            ActiveProvider::OpenAiCompatible
        }
    }
}
```

This is simplified, but the design is clear: provider selection belongs to the provider layer. The agent loop should not know whether Claude or OpenAI is the current default.

The session storage shape is also worth seeing directly:

```rust
// src/session/model.rs, field excerpt
pub struct StoredMessage {
    pub id: String,
    pub role: Role,
    pub content: Vec<ContentBlock>,
    pub display_role: Option<StoredDisplayRole>,
    pub timestamp: Option<DateTime<Utc>>,
    pub tool_duration_ms: Option<u64>,
    pub token_usage: Option<StoredTokenUsage>,
}

pub struct StoredCompactionState {
    pub summary_text: String,
    pub openai_encrypted_content: Option<String>,
    pub covers_up_to_turn: usize,
    pub original_turn_count: usize,
    pub compacted_count: usize,
}
```

This shows that a session is not a text transcript array. Messages carry structured `ContentBlock`s, display roles, timestamps, tool duration, and usage; compaction has its own summary and coverage state. Resume, replay, and import all depend on these details.

## What the Provider Layer Solves

Providers differ in many ways:

- Authentication: API keys, OAuth, device flow, local callback.
- Stream format.
- Thinking support.
- Tool calling format.
- Prompt cache behavior.
- Provider session ID support.
- Model catalog, context window, pricing.
- Error types and rate limits.

JCode's provider layer normalizes these differences into interfaces and events the runtime can consume.

## Auth Is Not a Side Issue

JCode supports many login targets:

```text
claude
openai
gemini
copilot
azure
openai-compatible
openrouter
lmstudio
ollama
...
```

This is not a one-API-key CLI.

OAuth, account switching, headless login, callback URLs, and pending login state are all practical product problems for coding agents.

If your previous demos only read `OPENAI_API_KEY`, this section may feel verbose. JCode is a long-running local tool: users switch accounts, switch providers, log in over SSH, and resume pending login flows. Prompts do not solve those problems.

## Why Session Matters

A JCode session is not just a chat transcript. It needs:

- resume
- replay
- crash recovery
- import
- render
- multi-client support
- memory profile
- active process tracking

Files:

```text
src/session/model.rs
src/session/journal.rs
src/session/render.rs
src/replay.rs
src/import.rs
```

This layer determines whether JCode is a long-running tool or a one-shot script.

## Why Session Import Matters

JCode's README mentions resuming sessions from Codex, Claude Code, OpenCode, and pi. That is not just copying text.

Different harnesses have different session shapes:

- message role representation
- tool call ID format
- tool result representation
- attachments/image representation
- provider metadata
- thinking/reasoning preservation

That is why import/session/render is worth reading.

## Two Judgments to Keep

First, session import is not "move the text over." OpenCode, Codex, Claude Code, and pi can represent sessions differently. JCode needs to align at least:

```text
message role
tool call id
tool result
attachments / images
provider metadata
thinking / reasoning
```

Second, provider streams must be normalized into JCode's internal `StreamEvent`. Otherwise the agent loop, TUI, and tool executor would all need provider-specific branches.

```text
Claude/OpenAI/Gemini/Copilot stream events differ.
JCode cannot let turn loop code know every private provider format.
After normalization into StreamEvent, the rest of the agent loop can handle text, thinking, tool input, and tool result consistently.
```
