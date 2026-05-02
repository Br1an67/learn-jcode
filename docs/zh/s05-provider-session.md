# s05 - Provider、Auth、Session

## 本课目标

理解 JCode 怎么把不同模型平台和长期会话接起来。

很多 agent demo 把 provider 层写成一行 API 调用。但真正做产品时，provider 是一大块工程。

## 先读这些文件

```text
src/provider/
src/auth/
src/usage/
src/session/
src/storage.rs
OAUTH.md
```

建议先看：

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

不要一口气读完所有 provider。先选一个你熟悉的，比如 OpenAI 或 Claude，把 trait、stream event、auth 这三条线追通。

## Provider 层解决什么问题

不同 provider 的差异很多：

- 认证方式不同：API key、OAuth、device flow、本地 callback。
- stream 格式不同。
- thinking 支持不同。
- tool calling 格式不同。
- prompt cache 行为不同。
- session id 支持不同。
- 模型目录、context window、价格不同。
- 错误类型和 rate limit 不同。

JCode 的 provider 层就是把这些差异统一成内部 runtime 能消费的接口和事件。

## Auth 不是边角料

JCode 支持很多登录方式：

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

这说明它不是简单面向一个 API key 的 CLI。

OAuth、账号切换、headless login、callback URL、pending login state，这些都是 coding-agent 产品会遇到的实际问题。

如果你做过只读 `OPENAI_API_KEY` 的 demo，这部分会显得啰嗦。但 JCode 面向的是长期本地工具，用户会换账号、换 provider、在 SSH 环境登录、恢复 pending login。这些都不是 prompt 能解决的问题。

## Session 为什么重要

JCode session 不是纯聊天记录。它要支持：

- resume
- replay
- crash recovery
- import
- render
- multi-client
- memory profile
- active process tracking

相关文件：

```text
src/session/model.rs
src/session/journal.rs
src/session/render.rs
src/replay.rs
src/import.rs
```

这层决定了 JCode 能不能成为长期工作的工具，而不是一次性脚本。

## Session import 的意义

JCode README 提到可以从 Codex、Claude Code、OpenCode、pi 恢复会话。这个能力背后不是“复制文本”这么简单。

不同 harness 的会话结构可能不同：

- message role 表示不同。
- tool call id 格式不同。
- tool result 表示不同。
- attachments/image 表示不同。
- provider metadata 不同。
- thinking/reasoning 是否保留不同。

所以 import/session/render 是很值得读的部分。

## 这里要记住的两个判断

第一，session import 难点不是“把文本搬过去”。OpenCode、Codex、Claude Code、pi 的会话结构不同，JCode 至少要对齐这些东西：

```text
message role
tool call id
tool result
attachments / images
provider metadata
thinking / reasoning
```

第二，provider stream 必须统一成 JCode 内部的 `StreamEvent`。否则 agent loop、TUI、tool executor 都要知道每个 provider 的私有格式。

```text
Claude/OpenAI/Gemini/Copilot 的 stream 事件不同。
JCode 不能让 turn loop 到处写 provider-specific 分支。
统一成 StreamEvent 后，后面的 agent loop 才能稳定处理 text、thinking、tool input、tool result。
```
