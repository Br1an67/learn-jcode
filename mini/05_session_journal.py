"""Tiny reproduction of JCode's session journal shape.

A session is not a plain transcript. The runtime appends structured events,
then renders or replays them later.
"""

from dataclasses import dataclass, field
from typing import Literal


EventKind = Literal["user", "assistant", "tool_call", "tool_result", "usage"]


@dataclass(frozen=True)
class JournalEvent:
    kind: EventKind
    payload: dict[str, str]


@dataclass
class Session:
    session_id: str
    journal: list[JournalEvent] = field(default_factory=list)

    def append(self, kind: EventKind, **payload: str) -> None:
        self.journal.append(JournalEvent(kind, payload))

    def render(self) -> list[str]:
        lines: list[str] = []
        for event in self.journal:
            if event.kind == "tool_call":
                lines.append(f"assistant called {event.payload['name']}")
            elif event.kind == "tool_result":
                lines.append(f"tool result: {event.payload['content']}")
            elif event.kind == "usage":
                lines.append(f"usage: {event.payload['tokens']} tokens")
            else:
                lines.append(f"{event.kind}: {event.payload['text']}")
        return lines

    def replay_messages(self) -> list[dict[str, str]]:
        messages: list[dict[str, str]] = []
        for event in self.journal:
            if event.kind in ("user", "assistant"):
                messages.append({"role": event.kind, "content": event.payload["text"]})
            elif event.kind == "tool_result":
                messages.append({"role": "tool", "content": event.payload["content"]})
        return messages


def main() -> None:
    session = Session("s1")
    session.append("user", text="read README")
    session.append("assistant", text="I will inspect the entry point.")
    session.append("tool_call", name="read", path="README.md")
    session.append("tool_result", content="# Learn JCode")
    session.append("usage", tokens="812")

    print("rendered view:")
    print("\n".join(session.render()))
    print("\nreplay messages:")
    print(session.replay_messages())


if __name__ == "__main__":
    main()
