# s09 - Ambient and Self-Dev

## Goal

Understand two later-stage JCode capabilities: the ambient background loop and self-dev.

Neither module is just a prompt. Ambient is about scheduling, budgets, and cycle endings. Self-dev is about session boundaries, build/reload, and recovery.

## Ambient

```mermaid
flowchart TD
  Scheduler["scheduler"] --> Cycle["ambient cycle"]
  Cycle --> Prompt["ambient system prompt"]
  Prompt --> Agent["background agent"]
  Agent --> EndTool["end_ambient_cycle"]
  EndTool --> Result["cycle result"]
  EndTool --> Next["next schedule"]
  Next --> Scheduler
```

This diagram shows why ambient needs an ending and scheduling mechanism. The background agent does not run forever; it reports the cycle result through `end_ambient_cycle` and schedules the next wake-up.

Read:

```text
docs/AMBIENT_MODE.md
src/ambient.rs
src/ambient/
src/ambient_runner.rs
src/tool/ambient.rs
```

Read `docs/AMBIENT_MODE.md` first for startup conditions, budgets, and safety boundaries. A background agent without boundaries is not assistance; it is noise.

Then read `src/ambient.rs` to see how `directives`, `manager`, `runner`, `scheduler`, and `persistence` fit together. It is a better map than starting inside a child module.

Next read `src/ambient/runner.rs` and `src/ambient_runner.rs`. Look for how one ambient cycle starts, how results are recorded, and how the next wake-up is decided. Keep one judgment in mind: background work must not interrupt the user's main line of work.

Then read `src/ambient/scheduler.rs`. Inspect how schedule items are ordered and woken. The hard part of ambient is not just prompting; it is time, priority, and resources.

Read `src/tool/ambient.rs` last. Start with `EndAmbientCycleTool`, `ScheduleAmbientTool`, `RequestPermissionTool`, and `ScheduleTool`. These tools show that an ambient agent cannot just act freely. It must end cycles, schedule future work, and request permission when needed.

The module map lives in `src/ambient.rs`:

The excerpts below come from the current local JCode revision. Some are simplified for explanation. Use them for concepts; use the source tree for exact edits.

```rust
// src/ambient.rs, excerpt
mod directives;
mod manager;
mod paths;
mod persistence;
mod prompt;
pub mod runner;
pub mod scheduler;

pub use directives::{add_directive, has_pending_directives, take_pending_directives};
pub use manager::AmbientManager;
pub use persistence::{AmbientLock, ScheduledQueue};
pub use prompt::{
    ResourceBudget,
    build_ambient_system_prompt,
    gather_recent_sessions,
    gather_memory_graph_health,
};
```

This shows ambient is not a single tool file. It has directives, manager, persistence, prompt, runner, and scheduler. The real topic is the background loop and budgets.

An ambient cycle must explicitly report how it ends:

```rust
// src/tool/ambient.rs, excerpt
struct EndCycleInput {
    summary: String,
    memories_modified: u32,
    compactions: u32,
    proactive_work: Option<String>,
    next_schedule: Option<NextScheduleInput>,
}

impl Tool for EndAmbientCycleTool {
    fn name(&self) -> &str { "end_ambient_cycle" }

    fn parameters_schema(&self) -> Value {
        json!({
            "required": ["summary", "memories_modified", "compactions"]
        })
    }
}
```

This shows the ambient agent does not just run and vanish. It must report what happened, how many memories changed, whether compaction happened, and when to wake next.

Ambient is a background agent. Instead of responding only to user prompts, it can do maintenance when resources allow:

- clean up memory
- inspect recent sessions
- check git activity
- perform low-risk proactive tasks
- decide when to wake next

This is experimental, but important because it points toward long-running agent environment maintenance.

When reading ambient, watch resource limits. A background agent without budget and priority rules becomes another source of interference.

## Self-Dev

```mermaid
flowchart LR
  Normal["normal session"] --> Enter["selfdev enter"]
  Enter --> Canary["self-dev / canary session"]
  Canary --> Build["selfdev build / test"]
  Build --> Reload["selfdev reload"]
  Reload --> Server["shared server"]
  Server --> Resume["resume sessions"]
```

This diagram shows the self-dev boundary: enter a self-dev session first, then build/test, then reload the shared server and resume sessions. Dangerous actions should not run directly from a normal session.

Read:

```text
src/cli/selfdev.rs
src/tool/selfdev/mod.rs
src/tool/selfdev/launch.rs
src/tool/selfdev/build_queue.rs
src/tool/selfdev/reload.rs
src/tool/selfdev/status.rs
src/prompt/selfdev_mode.txt
src/prompt/selfdev_hint.txt
docs/UNIFIED_SELFDEV_SERVER_PLAN.md
```

Start with `src/cli/selfdev.rs::run_self_dev()`. This explains how explicit `jcode self-dev` creates or resumes a self-dev session, marks it canary, decides whether a build is required, and launches the TUI.

Then read `src/tool/selfdev/mod.rs`. Start with the `SelfDevTool` action schema, then inspect how `execute()` dispatches `enter/build/cancel-build/reload/status/socket-info`. Notice that `reload`, `socket-info`, and `socket-help` check whether the current session is self-dev. That is the risk boundary.

Next read `src/tool/selfdev/launch.rs`. Inspect `enter_selfdev_session()` and `schedule_selfdev_prompt_delivery()`. This answers how a normal session moves into a self-dev session and why a new terminal may be spawned.

Then read `src/tool/selfdev/build_queue.rs` and `src/tool/selfdev/reload.rs`. The first manages build requests, dedupe, locks, and background status. The second manages how a new binary takes over the old server. Do not edit here early. First draw the build -> publish -> reload -> resume path.

Read `src/prompt/selfdev_mode.txt` and `src/prompt/selfdev_hint.txt` last. Use prompts to check the tool and CLI boundaries, not to reduce self-dev to "a different system prompt."

Start with the self-dev tool action schema:

The excerpts below come from the current local JCode revision. Some are simplified for explanation. Use them for concepts; use the source tree for exact edits.

```rust
// src/tool/selfdev/mod.rs, excerpt
impl Tool for SelfDevTool {
    fn name(&self) -> &str {
        "selfdev"
    }

    fn parameters_schema(&self) -> Value {
        json!({
            "properties": {
                "action": {
                    "enum": [
                        "enter",
                        "build",
                        "test",
                        "cancel-build",
                        "reload",
                        "status",
                        "socket-info",
                        "socket-help"
                    ]
                }
            },
            "required": ["action"]
        })
    }
}
```

This shows self-dev is not only a hidden command. It is a model-callable tool exposing a controlled action set: enter self-dev, build, test, reload, and inspect status.

Then read the risk boundary:

```rust
// src/tool/selfdev/mod.rs, excerpt
match action.as_str() {
    "enter" => self.do_enter(params.prompt, &ctx).await,
    "build" => self.do_build(params.reason, params.target, params.notify, params.wake, &ctx).await,
    "test" => self.do_test(params.command, params.reason, params.notify, params.wake, &ctx).await,
    "reload" => {
        if !SelfDevTool::session_is_selfdev(&ctx.session_id) {
            Ok(ToolOutput::new(
                "`selfdev reload` is only available inside a self-dev session. Use `selfdev enter` first.",
            ))
        } else {
            self.do_reload(params.context, &ctx.session_id, ctx.execution_mode).await
        }
    }
    "status" => self.do_status().await,
    _ => Ok(ToolOutput::new(format!("Unknown action: {}", action))),
}
```

This shows dangerous self-dev actions are not available in every session. `reload` must run inside a self-dev session. That is one of JCode's guardrails for letting the agent modify itself.

Self-dev lets JCode modify itself.

Be conservative:

- Create a branch.
- Keep the worktree clean.
- Commit each step.
- Start with small changes.
- Run `cargo check`.
- Do not start with provider, server reload, compaction, or swarm.

## Judgments To Keep

Ambient covers the fact that users will not explicitly ask for every bit of environment maintenance. It moves recent-session, memory, and git-activity maintenance into a background loop.

Self-dev covers the need to modify JCode itself quickly. The boundaries are branch, commit, build/test, self-dev session, and reload recovery.

Keep the risks with the benefits: ambient without resource limits becomes interference; self-dev changing reload or server state can lose running-session state.

## What You Should Be Able To Explain

- Why ambient needs a scheduler, budget, and `end_ambient_cycle`.
- Why an ambient agent cannot run forever in the background.
- Why self-dev must first enter a self-dev session.
- Why `selfdev reload` needs a session gate and recovery logic.
