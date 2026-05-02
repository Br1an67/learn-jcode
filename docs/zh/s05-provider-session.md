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

## 练习

回答：

```text
如果要把 OpenCode 的一个 session 导入 JCode，
你认为最难对齐的三个字段是什么？
```

再回答：

```text
为什么 provider stream 需要统一成 JCode 内部的 StreamEvent？
```
