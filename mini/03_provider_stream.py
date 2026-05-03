"""provider streaming 和 tool-call assembly 的最小复现。

Tiny reproduction of provider streaming and tool-call assembly.

JCode providers normalize platform-specific streams into internal events.
The agent loop collects tool input deltas, executes the tool, and appends
the result as the next user-side message.
"""

from dataclasses import dataclass
import json
from typing import Callable, Iterator, Any


@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    schema: dict[str, Any]
    handler: Callable[[dict[str, Any]], str]


class Registry:
    def __init__(self) -> None:
        self.tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self.tools[tool.name] = tool

    def execute(self, name: str, payload: dict[str, Any]) -> str:
        return self.tools[name].handler(payload)


@dataclass(frozen=True)
class Event:
    kind: str
    data: dict[str, Any]


def fake_provider_stream() -> Iterator[Event]:
    yield Event("text_delta", {"text": "I will inspect the repo. "})
    yield Event("tool_use_start", {"id": "toolu_1", "name": "repo_summary"})
    yield Event("tool_input_delta", {"delta": '{"branch": "'})
    yield Event("tool_input_delta", {"delta": 'main"}'})
    yield Event("tool_use_end", {})


def build_registry() -> Registry:
    registry = Registry()
    registry.register(
        Tool(
            name="repo_summary",
            description="Return a small repository summary.",
            schema={"type": "object"},
            handler=lambda payload: f"branch: {payload['branch']}\nfiles: 42",
        )
    )
    return registry


def run_turn() -> list[dict[str, Any]]:
    registry = build_registry()
    messages: list[dict[str, Any]] = []
    current_tool: dict[str, Any] | None = None
    current_input = ""

    for event in fake_provider_stream():
        if event.kind == "text_delta":
            messages.append({"role": "assistant", "text": event.data["text"]})
        elif event.kind == "tool_use_start":
            current_tool = {"id": event.data["id"], "name": event.data["name"]}
            current_input = ""
        elif event.kind == "tool_input_delta":
            current_input += event.data["delta"]
        elif event.kind == "tool_use_end" and current_tool is not None:
            payload = json.loads(current_input) if current_input else {}
            output = registry.execute(current_tool["name"], payload)
            messages.append(
                {
                    "role": "user",
                    "type": "tool_result",
                    "tool_use_id": current_tool["id"],
                    "content": output,
                }
            )

    return messages


def main() -> None:
    for message in run_turn():
        print(message)


if __name__ == "__main__":
    main()
