# mini/ 最小复现

`mini/` 里放的是 JCode 核心机制的缩小版。它们不是练习题，也不是另一套任务线。

正文课程仍然读 JCode 源码。这里的文件只负责把一个大机制压到几十行里，让你先看清边界，再回到真实 runtime。

用系统 Python 直接运行：

```bash
python3 mini/01_server_client.py
python3 mini/02_tool_registry.py
python3 mini/03_provider_stream.py
python3 mini/04_memory_sidecar.py
python3 mini/05_session_journal.py
python3 mini/06_swarm_channel.py
python3 mini/07_ambient_scheduler.py
python3 mini/08_selfdev_reload_gate.py
```

## 对应课程

| 文件 | 最小复现的机制 | 对应课程 |
| --- | --- | --- |
| `01_server_client.py` | 常驻 server 拥有 session，client 可以断开再连 | `s02` |
| `02_tool_registry.py` | 工具定义和 runtime 执行共用一个 registry | `s04` |
| `03_provider_stream.py` | provider stream 同时吐 text 和 tool-call delta | `s03`, `s05` |
| `04_memory_sidecar.py` | memory 非阻塞更新，下一轮再使用 | `s07` |
| `05_session_journal.py` | journal event 可以 render 和 replay 成 session state | `s05` |
| `06_swarm_channel.py` | server 持有 swarm 成员、channel 和进度状态 | `s08` |
| `07_ambient_scheduler.py` | ambient work 被排队、取出、结束、重新调度 | `s09` |
| `08_selfdev_reload_gate.py` | self-dev reload 受 session 和 recovery state 保护 | `s09` |

这些文件刻意不包含真实 LLM 调用、socket、文件编辑。重点不是复刻 JCode，而是保留机制形状。

# mini/ Minimal Reproductions

This directory contains small runnable files that isolate one JCode harness mechanism.

It is not a separate task track. The main course still reads JCode source. These files are minimal reproductions for moments where the real source is too large to see the mechanism at once.

Run them with the system Python:

```bash
python3 mini/01_server_client.py
python3 mini/02_tool_registry.py
python3 mini/03_provider_stream.py
python3 mini/04_memory_sidecar.py
python3 mini/05_session_journal.py
python3 mini/06_swarm_channel.py
python3 mini/07_ambient_scheduler.py
python3 mini/08_selfdev_reload_gate.py
```

## Map To Lessons

| File | Mechanism | Lesson |
| --- | --- | --- |
| `01_server_client.py` | resident server owns sessions; clients connect and disconnect | `s02` |
| `02_tool_registry.py` | tool definitions and runtime execution share one registry | `s04` |
| `03_provider_stream.py` | provider stream emits text and tool-call deltas | `s03`, `s05` |
| `04_memory_sidecar.py` | memory update is non-blocking and used on the next turn | `s07` |
| `05_session_journal.py` | structured journal events render and replay into session state | `s05` |
| `06_swarm_channel.py` | server-owned swarm state tracks members, channels, and progress | `s08` |
| `07_ambient_scheduler.py` | ambient work is queued, popped, ended, and rescheduled | `s09` |
| `08_selfdev_reload_gate.py` | self-dev reload is gated by session and recovery state | `s09` |

These files deliberately omit real LLM calls, sockets, and file edits. The point is to preserve the shape of the mechanism without the full JCode runtime.
