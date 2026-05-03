"""非阻塞 memory sidecar 行为的最小复现。

Tiny reproduction of non-blocking memory sidecar behavior.

The main turn submits context without waiting. The sidecar computes a memory
prompt later, so the next turn can inject it.
"""

from dataclasses import dataclass
from queue import Queue, Empty, Full
from threading import Thread
from time import sleep


@dataclass(frozen=True)
class ContextUpdate:
    session_id: str
    messages: tuple[str, ...]


class MemorySidecar:
    def __init__(self) -> None:
        self.queue: Queue[ContextUpdate | None] = Queue(maxsize=1)
        self.pending_prompt: str | None = None
        self.worker = Thread(target=self._run, daemon=True)
        self.worker.start()

    def submit_context(self, session_id: str, messages: list[str]) -> None:
        try:
            self.queue.put_nowait(ContextUpdate(session_id, tuple(messages)))
        except Full:
            pass

    def take_pending_prompt(self) -> str | None:
        prompt = self.pending_prompt
        self.pending_prompt = None
        return prompt

    def close(self) -> None:
        self.queue.put(None)
        self.worker.join(timeout=1)

    def _run(self) -> None:
        while True:
            try:
                update = self.queue.get(timeout=0.1)
            except Empty:
                continue
            if update is None:
                return
            sleep(0.05)
            last = update.messages[-1] if update.messages else ""
            self.pending_prompt = f"Relevant memory for {update.session_id}: remember {last!r}"


def main() -> None:
    memory = MemorySidecar()
    messages = ["user prefers concise source walkthroughs"]

    print("turn N memory:", memory.take_pending_prompt())
    memory.submit_context("s1", messages)
    sleep(0.1)
    print("turn N+1 memory:", memory.take_pending_prompt())

    memory.close()


if __name__ == "__main__":
    main()
