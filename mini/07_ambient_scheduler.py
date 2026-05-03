"""JCode ambient scheduler 的最小复现。

Tiny reproduction of JCode's ambient scheduler.

Ambient work is not an infinite background loop. Work becomes a scheduled item,
the runner pops ready items, and the agent must end the cycle explicitly.
"""

from dataclasses import dataclass, field


@dataclass(order=True)
class ScheduledItem:
    due_at: int
    priority: int
    prompt: str = field(compare=False)


class ScheduledQueue:
    def __init__(self) -> None:
        self.items: list[ScheduledItem] = []

    def push(self, item: ScheduledItem) -> None:
        self.items.append(item)

    def pop_ready(self, now: int) -> list[ScheduledItem]:
        ready = [item for item in self.items if item.due_at <= now]
        self.items = [item for item in self.items if item.due_at > now]
        return sorted(ready, key=lambda item: (-item.priority, item.due_at))


@dataclass
class CycleResult:
    summary: str
    next_due_at: int | None = None
    next_prompt: str | None = None


def run_ambient_cycle(item: ScheduledItem) -> CycleResult:
    print("ambient prompt:", item.prompt)
    return CycleResult(
        summary="checked recent sessions and memory health",
        next_due_at=item.due_at + 60,
        next_prompt="follow up on memory health",
    )


def end_ambient_cycle(queue: ScheduledQueue, result: CycleResult) -> None:
    print("cycle summary:", result.summary)
    if result.next_due_at is not None and result.next_prompt is not None:
        queue.push(ScheduledItem(result.next_due_at, priority=1, prompt=result.next_prompt))


def main() -> None:
    queue = ScheduledQueue()
    queue.push(ScheduledItem(due_at=10, priority=2, prompt="inspect pending directives"))
    queue.push(ScheduledItem(due_at=30, priority=1, prompt="later maintenance"))

    for item in queue.pop_ready(now=10):
        end_ambient_cycle(queue, run_ambient_cycle(item))

    print("queued after cycle:", queue.items)


if __name__ == "__main__":
    main()
