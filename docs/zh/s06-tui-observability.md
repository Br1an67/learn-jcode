# s06 - TUI 和可观察性

## 本课目标

理解 UI 为什么是 harness 的一部分。

很多 agent 工程只关心“模型能不能完成任务”。但实际使用时，用户还需要知道它在干什么、改了什么、卡在哪里、花了多少上下文和钱。

JCode 在 TUI 上投入很多，这不是装饰。

判断一个 UI 模块是不是 harness 的一部分，看它是否影响用户判断 agent 状态。tool 状态、diff、usage、memory 命中都影响判断，所以它们不是皮肤。

```mermaid
flowchart LR
  Server["server / runtime events"] --> Protocol["protocol events"]
  Protocol --> AppState["TUI app state"]
  AppState --> Widgets["InfoWidgetData"]
  AppState --> Tools["ui_tools summaries"]
  AppState --> Diff["ui_diff"]
  Widgets --> Render["render_all"]
  Tools --> Render
  Diff --> Render
  Render --> User["terminal view"]
```

这张图说明 TUI 不是 stdout 包装。server/runtime 事件先写入 TUI state，再分别变成 widget、tool summary、diff，最后渲染成用户能判断 agent 状态的界面。

## 本课直接讲清楚的主线

TUI 的主线是事件变成判断。server/runtime 事件进入 app state，然后分别变成 info widget、tool summary、diff、side panel 和流式文本。用户看到的不是原始 protocol，而是被压缩成“我能不能继续信任这个 agent”的状态。

Info widget 解决布局和信息密度：`InfoWidgetData` 收集状态，`calculate_placements()` 决定位置，`render_all()` 统一渲染。Git、todo、memory、swarm 这些 widget 的差别不在画法，而在它们各自回答用户什么问题。

Tool summary 和 diff 是另外两层压缩。模型工具调用通常是 JSON，TUI 要把它压成一行可扫的动作摘要；文件编辑还可以从 tool input 提前推断 diff，而不是等完整工具结果回来。Side panel 则更进一步：它是模型能写入、追加、聚焦和删除的持久页面，不只是临时展示区。

## 核心代码节选

下面代码摘自本地 JCode 当前 revision，部分为了讲解做了精简。读概念看这里，改代码以源码为准。

Info widget 的入口不是某个具体 widget，而是布局和统一渲染：

```rust
// src/tui/info_widget.rs，节选
pub fn calculate_placements(
    messages_area: Rect,
    margins: &Margins,
    data: &InfoWidgetData,
) -> Vec<WidgetPlacement> {
    let placements = info_widget_layout::calculate_placements(
        messages_area,
        margins,
        data,
        state.enabled,
        &state.placements,
    );
    state.placements = placements.clone();
    placements
}

pub fn render_all(frame: &mut Frame, placements: &[WidgetPlacement], data: &InfoWidgetData) {
    for placement in placements {
        render_single_widget(frame, placement, data);
    }
}
```

这段代码说明 widget 不是随便画在右边。JCode 先根据消息区域、边距和当前数据算 placement，再统一 render。可观察性在这里先变成布局问题。

工具摘要也有单独的压缩层：

```rust
// src/tui/ui_tools.rs，节选
pub(crate) fn get_tool_summary(tool: &ToolCall) -> String {
    get_tool_summary_with_budget(tool, 50, None)
}

fn get_tool_summary_with_budget(tool: &ToolCall, bash_max_chars: usize, max_width: Option<usize>)
    -> String
{
    match canonical_tool_name(&tool.name) {
        "bash" => format!("$ {}", truncate_command_display(cmd, cmd_budget)),
        "read" => path_summary(tool),
        "grep" => query_summary(tool),
        _ => String::new(),
    }
}
```

这是精简版，但能看出 UI 层的责任：模型调用工具时，用户不应该看到完整 JSON。TUI 要把工具名和 input 压成一行可扫的摘要。

diff 也不是只等工具输出：

```rust
// src/tui/ui_diff.rs，节选
pub(super) fn generate_diff_lines_from_tool_input(tool: &ToolCall)
    -> Vec<ParsedDiffLine>
{
    match canonical_tool_name(&tool.name) {
        "edit" => {
            let old = tool.input.get("old_string").and_then(|v| v.as_str()).unwrap_or("");
            let new = tool.input.get("new_string").and_then(|v| v.as_str()).unwrap_or("");
            generate_diff_lines_from_strings(old, new)
        }
        "multiedit" => { /* 对每个 edit 生成 diff lines */ }
        _ => Vec::new(),
    }
}
```

这段代码说明 JCode 可以从 tool input 提前生成 diff 线索。用户看到的“改了多少”不是最后才从文件系统算出来，TUI 在工具开始阶段就能推断一部分。

Side panel 是模型能操作的状态，不只是 UI 组件：

```rust
// src/tool/side_panel.rs，节选
impl Tool for SidePanelTool {
    fn name(&self) -> &str { "side_panel" }

    fn parameters_schema(&self) -> Value {
        json!({
            "properties": {
                "action": {
                    "enum": ["status", "write", "append", "load", "focus", "delete"]
                }
            },
            "required": ["action"]
        })
    }
}
```

这段代码说明 side panel 被注册成工具。模型可以写入、追加、加载、聚焦、删除页面，所以它是 harness 状态的一部分，不只是前端展示。

## JCode TUI 展示什么

JCode 的 TUI 不只是打印 assistant text。它还处理：

- tool call 摘要。
- streaming 状态。
- reasoning/thinking 展示。
- diff。
- side panel。
- markdown。
- mermaid。
- usage。
- model/account picker。
- git 状态。
- memory 状态。
- todo 状态。
- swarm/background 状态。

这些都是 harness 的可观察性。

## Side Panel 的意义

Side panel 是一个很实用的设计。它可以放：

- 当前文件。
- diff。
- 计划。
- review checklist。
- memory 命中。
- agent 生成的辅助内容。

这让用户不用在主聊天流里翻来翻去。

Side panel 的价值不是“多一个面板”。它把稳定参考信息从聊天流里拿出来。聊天流适合时间线，side panel 适合当前状态。

## Info Widget 的意义

Info widget 解决的是“状态显示不能抢主输出空间”的问题。比如：

- 当前模型。
- usage。
- git branch。
- memory 命中。
- todos。
- swarm 状态。

这些信息很重要，但不应该把主对话挤没。

## 和 OpenCode 的对比

OpenCode 也重视 UI，但路线不同。OpenCode 同时走 Web/Desktop/Open platform。JCode 更偏 terminal native，强调 Ratatui 渲染、终端信息密度和本地 runtime。

两者都说明一件事：coding agent 的 UI 不是 shell stdout 就够了。

## 一个 widget 的判断标准

判断 `info_widget_git` 或 `info_widget_todos` 这类 widget 是否成立，就看这条数据链路：

```text
数据从哪里来？
在哪里进入状态？
通过什么 event 更新？
在哪里 render？
用户为什么需要这个信息？
```

判断一个 widget 是否必要，就问一句：删掉它，用户会少知道什么？答不上来，这个 widget 的用途还没讲清楚。

## 读完你应该能解释什么

- 为什么 TUI 是 harness 的一部分，而不是皮肤。
- `InfoWidgetData` 和 `calculate_placements()` 解决什么问题。
- tool summary 为什么不能直接展示原始 JSON。
- side panel 为什么是模型可操作的状态，而不是临时展示区域。
