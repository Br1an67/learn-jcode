"""mini/ 最小复现共用的小类型。

Shared tiny types for the mini minimal reproductions.
"""

from dataclasses import dataclass
from typing import Callable, Any


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
