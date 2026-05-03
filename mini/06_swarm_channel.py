"""JCode server-owned swarm coordination 的最小复现。

Tiny reproduction of JCode's server-owned swarm coordination.

Swarm state lives in the server: members, plans, task progress, and channel
subscriptions are not guessed from chat history.
"""

from dataclasses import dataclass, field


@dataclass
class TaskProgress:
    assigned_session_id: str | None = None
    heartbeat_count: int = 0
    checkpoint_summary: str | None = None
    done: bool = False


@dataclass
class SwarmState:
    members: set[str] = field(default_factory=set)
    channels: dict[str, set[str]] = field(default_factory=dict)
    task_progress: dict[str, TaskProgress] = field(default_factory=dict)
    inbox: dict[str, list[str]] = field(default_factory=dict)

    def add_member(self, session_id: str) -> None:
        self.members.add(session_id)
        self.inbox.setdefault(session_id, [])

    def subscribe(self, session_id: str, channel: str) -> None:
        if session_id not in self.members:
            raise KeyError(f"unknown member: {session_id}")
        self.channels.setdefault(channel, set()).add(session_id)

    def assign_task(self, task_id: str, session_id: str) -> None:
        self.task_progress[task_id] = TaskProgress(assigned_session_id=session_id)
        self.inbox[session_id].append(f"assigned {task_id}")

    def heartbeat(self, task_id: str, summary: str) -> None:
        progress = self.task_progress[task_id]
        progress.heartbeat_count += 1
        progress.checkpoint_summary = summary

    def broadcast(self, channel: str, message: str) -> None:
        for member in sorted(self.channels.get(channel, set())):
            self.inbox[member].append(f"#{channel}: {message}")

    def report_done(self, task_id: str) -> None:
        self.task_progress[task_id].done = True


def main() -> None:
    swarm = SwarmState()
    swarm.add_member("coordinator")
    swarm.add_member("worker-a")
    swarm.add_member("worker-b")
    swarm.subscribe("worker-a", "backend")
    swarm.subscribe("worker-b", "backend")

    swarm.assign_task("task-1", "worker-a")
    swarm.heartbeat("task-1", "parsed server state")
    swarm.broadcast("backend", "avoid touching provider code today")
    swarm.report_done("task-1")

    print("task progress:", swarm.task_progress)
    print("worker-a inbox:", swarm.inbox["worker-a"])
    print("worker-b inbox:", swarm.inbox["worker-b"])


if __name__ == "__main__":
    main()
