# s09 - Ambient 和 Self-Dev

## 本课目标

读懂 JCode 两个更靠后的能力：ambient 后台循环，以及 self-dev 自我修改。

这两个模块都不能只看 prompt。Ambient 的关键是调度、预算和结束机制；self-dev 的关键是 session 边界、build/reload 和恢复。

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

这张图说明 ambient 必须有结束和调度机制。后台 agent 不是无限跑，它通过 `end_ambient_cycle` 汇报结果并安排下一次唤醒。

先读：

```text
docs/AMBIENT_MODE.md
src/ambient.rs
src/ambient/
src/ambient_runner.rs
src/tool/ambient.rs
```

先读 `docs/AMBIENT_MODE.md`，只看 ambient 的启动条件、预算和安全边界。ambient 如果没有边界，就不是助手，而是后台噪音。

然后读 `src/ambient.rs`，看它怎样把 `directives`、`manager`、`runner`、`scheduler`、`persistence` 串起来。这个文件通常比直接读子模块更适合当地图。

第三步读 `src/ambient/runner.rs` 和 `src/ambient_runner.rs`。重点找 runner 怎么启动一轮 ambient cycle、怎么记录结果、怎么决定下次是否继续。这里要带着“后台任务不能打断用户主线”这个判断读。

第四步读 `src/ambient/scheduler.rs`。看 schedule item 怎么排序、怎么被唤醒。ambient 的难点不只是 prompt，而是时间、优先级和资源。

最后读 `src/tool/ambient.rs`。先看 `EndAmbientCycleTool`、`ScheduleAmbientTool`、`RequestPermissionTool`、`ScheduleTool`。这些工具说明 ambient agent 不是随便行动，它需要显式结束 cycle、安排下次运行，必要时请求权限。

ambient 的模块地图在 `src/ambient.rs` 里：

下面代码摘自本地 JCode 当前 revision，部分为了讲解做了精简。读概念看这里，改代码以源码为准。

```rust
// src/ambient.rs，节选
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

这段代码说明 ambient 不是一个工具文件。它有指令、管理器、持久化、prompt、runner、scheduler。真正要读的是后台循环和预算，不是只看工具 schema。

ambient cycle 结束也必须通过工具显式上报：

```rust
// src/tool/ambient.rs，节选
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

这段代码说明 ambient agent 不是跑完就消失。它必须汇报本轮做了什么、改了多少 memory、是否做了 compaction、下次什么时候醒。

Ambient 是后台 agent。它不是用户发一句做一句，而是在资源允许时做维护：

- 整理 memory。
- 检查最近 session。
- 看 git 活动。
- 做低风险主动任务。
- 自己决定下次什么时候醒来。

这个方向还很实验，但值得读，因为它指向长期 agent 环境维护。

读 ambient 时重点看资源限制。后台 agent 如果没有预算和优先级控制，会变成另一个干扰源。

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

这张图说明 self-dev 的边界：先切到 self-dev session，再 build/test，最后 reload shared server 并恢复会话。危险动作不应该从普通 session 直接执行。

先读：

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

先读 `src/cli/selfdev.rs` 的 `run_self_dev()`。这条线解释显式 `jcode self-dev` 怎么创建或恢复 self-dev session，怎么设置 canary 标记，什么时候要求先 build，最后怎么启动 TUI。

然后读 `src/tool/selfdev/mod.rs`。先看 `SelfDevTool` 的 action schema，再看 `execute()` 里对 `enter/build/cancel-build/reload/status/socket-info` 这些 action 的分发。注意 `reload`、`socket-info`、`socket-help` 会检查当前 session 是否 self-dev，这就是风险边界。

第三步读 `src/tool/selfdev/launch.rs`。看 `enter_selfdev_session()` 和 `schedule_selfdev_prompt_delivery()`。这部分回答“普通会话怎么切到 self-dev 会话”，也解释为什么它可能要新开 terminal。

第四步读 `src/tool/selfdev/build_queue.rs` 和 `src/tool/selfdev/reload.rs`。前者管 build 请求、去重、锁和后台状态，后者管新 binary 怎么接管旧 server。这里不要急着改，先画出 build -> publish -> reload -> resume 的链路。

最后读 `src/prompt/selfdev_mode.txt` 和 `src/prompt/selfdev_hint.txt`。prompt 放最后读，是为了验证工具和 CLI 的边界，而不是把 self-dev 理解成“换一段系统提示词”。

Self-dev 工具的 action schema 先看这一段：

下面代码摘自本地 JCode 当前 revision，部分为了讲解做了精简。读概念看这里，改代码以源码为准。

```rust
// src/tool/selfdev/mod.rs，节选
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

这段代码说明 self-dev 不是一个隐藏命令，而是模型能调用的工具。它暴露的是一组受控动作：进入 self-dev、build、test、reload、看状态。

再看风险边界：

```rust
// src/tool/selfdev/mod.rs，节选
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

这段代码说明 self-dev 的危险动作不是所有 session 都能用。`reload` 必须在 self-dev session 里执行，这是 JCode 给“让 agent 改自己”加的边界。

Self-dev 是让 JCode 改自己。

建议非常保守：

- 新建分支。
- 保持工作区干净。
- 每一步 commit。
- 小改动开始。
- 必须跑 `cargo check`。
- 不要一上来改 provider、server reload、compaction、swarm。

## 这课应该带走的判断

Ambient 补的是用户不会每次显式要求维护环境的短板。它把近期 session、memory、git 活动这类维护工作放到后台循环里。

Self-dev 补的是 JCode 自己也需要被快速改造的需求。边界是分支、commit、build/test、self-dev session 和 reload 恢复。

风险也要一起记住：ambient 没有资源限制会变成干扰源；self-dev 改 reload 或 server state 可能让正在运行的 session 丢状态。

## 读完你应该能解释什么

- ambient 为什么需要 scheduler、budget 和 `end_ambient_cycle`。
- ambient agent 为什么不能无限后台运行。
- self-dev 为什么要先切到 self-dev session。
- `selfdev reload` 为什么需要 session gate 和恢复逻辑。
