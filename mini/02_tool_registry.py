"""JCode tool registry 的最小复现。

Tiny reproduction of JCode's tool registry.

The same registry produces model-visible tool definitions and executes
tool calls at runtime.
"""

from dataclasses import dataclass
from typing import Callable, Any


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    description: str
    schema: dict[str, Any]


@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    schema: dict[str, Any]
    handler: Callable[[dict[str, Any]], str]

    def to_definition(self) -> ToolDefinition:
        return ToolDefinition(self.name, self.description, self.schema)


class Registry:
    def __init__(self) -> None:
        self.tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self.tools[tool.name] = tool

    def definitions(self) -> list[ToolDefinition]:
        return [tool.to_definition() for _, tool in sorted(self.tools.items())]

    def execute(self, name: str, payload: dict[str, Any]) -> str:
        if name not in self.tools:
            raise KeyError(f"unknown tool: {name}")
        output = self.tools[name].handler(payload)
        return self._guard_output(output)

    def _guard_output(self, output: str, limit: int = 120) -> str:
        if len(output) <= limit:
            return output
        return output[:limit] + "\n...[truncated]"


def build_registry() -> Registry:
    registry = Registry()
    registry.register(
        Tool(
            name="repo_summary",
            description="Return a small repository summary.",
            schema={"type": "object", "properties": {"branch": {"type": "string"}}},
            handler=lambda payload: f"branch: {payload.get('branch', 'main')}\nfiles: 42",
        )
    )
    return registry


def main() -> None:
    registry = build_registry()
    print("definitions:", registry.definitions())
    print("execute:", registry.execute("repo_summary", {"branch": "main"}))


if __name__ == "__main__":
    main()
