# Mini Mechanism Specimens

This directory contains small runnable files that isolate one JCode harness mechanism.

It is not a separate task track. The main course still reads JCode source. These files are reduced specimens for moments where the real source is too large to see the mechanism at once.

Run them with the system Python:

```bash
python3 mini/01_server_client.py
python3 mini/02_tool_registry.py
python3 mini/03_provider_stream.py
python3 mini/04_memory_sidecar.py
```

## Map To Lessons

| File | Mechanism | Lesson |
| --- | --- | --- |
| `01_server_client.py` | resident server owns sessions; clients connect and disconnect | `s02` |
| `02_tool_registry.py` | tool definitions and runtime execution share one registry | `s04` |
| `03_provider_stream.py` | provider stream emits text and tool-call deltas | `s03`, `s05` |
| `04_memory_sidecar.py` | memory update is non-blocking and used on the next turn | `s07` |

These files deliberately omit real LLM calls, sockets, and file edits. The point is to preserve the shape of the mechanism without the full JCode runtime.
