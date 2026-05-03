"""Tiny reproduction of JCode's self-dev reload gate.

Self-dev exposes build and reload as tool actions, but reload must happen from
a self-dev session and must leave recovery state behind.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Session:
    session_id: str
    is_selfdev: bool = False


@dataclass
class BuildManifest:
    canary_version: str | None = None
    pending_activation: dict[str, str] | None = None


@dataclass(frozen=True)
class ReloadContext:
    session_id: str
    version_after: str
    task_context: str


class SelfDevTool:
    def __init__(self) -> None:
        self.manifest = BuildManifest()
        self.reload_context: ReloadContext | None = None

    def enter(self, parent: Session) -> Session:
        return Session(session_id=f"{parent.session_id}-selfdev", is_selfdev=True)

    def build(self, version: str) -> str:
        self.manifest.canary_version = version
        return f"built {version}"

    def reload(self, session: Session, task_context: str) -> str:
        if not session.is_selfdev:
            return "denied: use selfdev enter first"
        if self.manifest.canary_version is None:
            return "denied: build first"

        version = self.manifest.canary_version
        self.manifest.pending_activation = {
            "session_id": session.session_id,
            "new_version": version,
        }
        self.reload_context = ReloadContext(session.session_id, version, task_context)
        return f"reload signal sent for {version}"


def main() -> None:
    tool = SelfDevTool()
    normal = Session("s1")
    print(tool.reload(normal, "finish current patch"))

    dev = tool.enter(normal)
    print(tool.build("abc123"))
    print(tool.reload(dev, "finish current patch"))
    print("pending activation:", tool.manifest.pending_activation)
    print("reload context:", tool.reload_context)


if __name__ == "__main__":
    main()
