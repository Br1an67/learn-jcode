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

## Exercise

Answer:

```text
If an OpenCode session must be imported into JCode,
what are the three hardest fields to align?
```

Then answer:

```text
Why does provider streaming need to be normalized into JCode StreamEvent?
```

The answer must mention at least two provider differences. "For a unified interface" is not enough.
