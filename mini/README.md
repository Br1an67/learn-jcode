# Mini Mechanism Specimens

This directory contains small runnable files that isolate one JCode harness mechanism.

It is not a separate task track. The main course still reads JCode source. These files are reduced specimens for moments where the real source is too large to see the mechanism at once.

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
