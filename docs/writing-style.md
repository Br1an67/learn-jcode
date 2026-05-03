# 写作规范

这份规范用来约束 `learn-jcode` 的写法。目标不是“正式”，而是让教程像一个懂工程的人在带读源码。

## 1. 角色与读者

作者身份：我是一个读过 JCode 源码的工程同事，写这份教程给想读懂 coding-agent harness 的开发者看。语气像代码走查和学习笔记，不像发布会文案，也不像咨询报告。

读者画像：读者有技术背景，知道一点 LLM/agent，但时间有限，不想听空话；他们想直接在教程里看懂核心代码、设计边界和后续能做的小改造，不想在 IDE 和文档之间来回跳。

## 2. 风格要点

### 说人话，不堆概念

正面示例：

```text
JCode 不是每次启动一个独立 CLI。它先找本地 server，没有就拉起一个 daemon，然后 TUI client 连上去。
```

反面示例：

```text
JCode 通过先进的多端协同架构实现了高效的智能体运行时闭环。
```

### 有判断，不装中立

正面示例：

```text
如果你只想学最小 agent loop，先看 pi。JCode 太大，不适合当第一个项目。
```

反面示例：

```text
不同项目各有优劣，读者可以根据自己的需求选择合适方案。
```

### 每段都落到源码或结论

正面示例：

```text
`Registry::base_tools()` 同时决定“模型能看到什么工具”和“运行时能执行什么工具”。这就是 JCode 工具系统不把 schema 和执行器拆成两套注册表的原因。
```

反面示例：

```text
工具系统是 agent 能力的重要组成部分，对整体体验有显著提升。
```

### 引用文件时必须带读

正面示例：

```text
先打开 `src/main.rs`，只看 `main()`：它基本不处理业务，只配置 allocator 和 tokio runtime，然后把控制权交给 `jcode::run()`。下一步再跳到 `src/lib.rs`，看 `run()` 如何进入 `cli::startup::run()`。
```

反面示例：

```text
先读 `src/main.rs`、`src/lib.rs`、`src/cli/startup.rs`。
```

规则：文件路径只能作为源码出处，不要把教程写成“阅读顺序清单”。关键流程要直接摘核心代码，并说清楚“这个函数/结构体在链路里承担什么角色”。

### 带读要把核心代码放进教程

正面示例：

```rust
pub async fn run() -> Result<()> {
    cli::startup::run().await
}
```

这段代码说明 `src/lib.rs` 只是入口转发，真正启动逻辑在 `src/cli/startup.rs`。读者不需要打开 IDE 才知道这一步发生了什么。

反面示例：

```text
接着读 `src/lib.rs`，它会进入启动逻辑。
```

规则：关键流程必须给源码节选、精简版源码或结构体字段摘录。代码块后面要解释它在流程里做了什么，不要只写“见源码”。不要整段搬大文件，只摘最能说明问题的 5-25 行。

### 复杂流程优先画 Mermaid

正面示例：

```mermaid
flowchart LR
  User[User input] --> Turn[run_turn]
  Turn --> Provider[provider.complete_split]
  Provider --> ToolCall[tool call]
  ToolCall --> Registry[Registry::execute]
  Registry --> Result[tool result]
  Result --> Turn
```

这张图先给出 agent loop 的闭合路径。代码节选解释函数细节，Mermaid 负责让读者先看到结构。

反面示例：

```text
JCode 的 agent loop 会经过 provider、tool registry、tool result、message。
```

规则：启动过程、agent loop、tool registry、provider stream、server/client event、memory sidecar、swarm coordination 这类内容应优先配 Mermaid。图要解释状态放在哪里或数据怎么流动，不画纯装饰图。每张图后面必须用一句话解释图里最重要的关系。

### 解释设计取舍，不写功能清单

正面示例：

```text
Memory 不阻塞当前 turn。第 N 轮触发查询，第 N+1 轮用结果。这样牺牲一点即时性，换交互延迟稳定。
```

反面示例：

```text
JCode 支持 memory、session search、embedding、graph retrieval 等能力。
```

### 口吻克制，但可以直接

正面示例：

```text
不要第一天改 swarm。你还没看懂 server state，进去只会被生命周期和通信逻辑绕晕。
```

反面示例：

```text
强烈建议读者谨慎探索高级功能模块，以免产生不必要的学习成本。
```

### 改文案要通读，不只扫关键词

正面示例：

```text
通读一节以后，发现“这段代码说明...”连续出现，就把它改成更具体的旁注：这里能看出什么状态被保存、谁在调用谁、少了这一步会怎样。
```

反面示例：

```text
只搜索“赋能”“闭环”“总之”，没搜到就认为没有 AI 味。
```

规则：关键词扫描只能做最后兜底。正式改正文时，必须按章节顺序通读，重点检查段落是否像正常技术作者在带读代码，而不是只检查禁用词。

## 3. 禁止清单

这些表达一律删掉或改写。

| 禁止类型 | 不要写 | 替换方式 |
| --- | --- | --- |
| 废话开场 | `众所周知`、`在当今 AI 时代`、`随着大模型的发展` | 直接进入问题 |
| 语气拐棍 | `说实话`、`不得不说`、`有一说一`、`值得一提的是` | 删除 |
| 商业黑话 | `赋能`、`闭环`、`抓手`、`落地`、`体系化能力` | 换成具体动作 |
| AI 味总结 | `总之`、`综上所述`、`通过以上分析可以看出` | 用一句具体判断收尾 |
| 空泛形容 | `强大`、`高效`、`灵活`、`完善`、`先进` | 写清楚强在哪里、代价是什么 |
| 模板句 | `本文将深入探讨`、`接下来我们将` | 改成“这一课读...” |
| 模板标题 | `本课目标`、`本课一句话`、`这课应该带走的结论`、`读完你应该能解释什么` | 改成“先看...”“读完后检查一下” |
| 生硬比喻 | `运行时仪表盘`、`第一把钥匙`、`磨平成一种 stream`、`为状态付账` | 改成直接工程描述 |
| 端着的判断 | `更硬的判读方法`、`硬判断`、`一件很硬的事`、`工具哲学` | 改成“更实际的判断方法”“更直接地说”“工具取向” |
| 假客观 | `各有优劣`、`因人而异` | 给出默认建议，再说明例外 |
| 过度拟人 | `JCode 帮你轻松搞定` | 写 JCode 具体做了什么 |

例子：

```text
不要写：JCode 通过完善的工具生态赋能开发者实现高效编码闭环。
改成：JCode 把文件、shell、MCP、memory、swarm 都注册成工具。代价是 tool registry 必须处理排序、截断、alias 和动态注册。
```

## 4. 参考资料与术语

### 内容参考范围

- [JCode](https://github.com/1jehuang/jcode) 源码是主体。
- [pi-mono](https://github.com/badlogic/pi-mono) 只用于校准最小 coding harness 的边界。
- [OpenCode](https://github.com/anomalyco/opencode) 只用于校准开源多端 coding-agent runtime 的边界。
- Claude Code 只讨论公开行为，不讨论非公开源码。

### 术语写法

| 术语 | 中文写法 | 说明 |
| --- | --- | --- |
| harness | harness | 不强翻成“框架”或“载具”，首次可解释为运行环境 |
| agent loop | agent loop | 保持英文，避免翻译成“智能体循环” |
| tool call | tool call | 保持英文，必要时解释为模型请求工具执行 |
| tool result | tool result | 保持英文，表示工具输出回到模型上下文 |
| provider | provider | 指模型平台适配层 |
| session | session | 指长期会话状态，不只是聊天记录 |
| TUI | TUI | 终端 UI |
| swarm | swarm | 指 JCode 的多 agent 协作 runtime |
| ambient | ambient | 指后台自主循环，不翻译成“环境模式” |
| self-dev | self-dev | 指 JCode 修改自身的模式 |

### 常见错误

- 不要把 JCode 写成“Claude Code 开源替代品”。它有相似 harness 概念，但工程取向不同。
- 不要把 memory 写成普通 RAG。JCode 重点是非阻塞召回和长期会话经验。
- 不要把 swarm 写成 subagent。swarm 关心 server-level coordination、通信、状态和文件触达。
- 不要只罗列功能。每个功能都要说明它解决什么问题、代价是什么、源码从哪里读。

### 英文版补充

英文版也保持同样语气：plain engineering notes, not marketing copy. Prefer "read this file and answer this question" over "this section explores".
