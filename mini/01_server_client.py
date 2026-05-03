"""JCode 常驻 server/client 形状的最小复现。

Tiny reproduction of JCode's resident server/client shape.

JCode does not put all state in the TUI client. A resident server owns
sessions and accepts clients that can connect, disconnect, and reconnect.
"""

from dataclasses import dataclass, field


@dataclass
class Session:
    session_id: str
    messages: list[str] = field(default_factory=list)


class ResidentServer:
    def __init__(self) -> None:
        self.sessions: dict[str, Session] = {}
        self.client_count = 0

    def connect(self) -> "Client":
        self.client_count += 1
        return Client(self)

    def disconnect(self) -> None:
        self.client_count -= 1

    def get_session(self, session_id: str) -> Session:
        if session_id not in self.sessions:
            self.sessions[session_id] = Session(session_id)
        return self.sessions[session_id]


class Client:
    def __init__(self, server: ResidentServer) -> None:
        self.server = server

    def send(self, session_id: str, text: str) -> None:
        session = self.server.get_session(session_id)
        session.messages.append(text)

    def history(self, session_id: str) -> list[str]:
        return list(self.server.get_session(session_id).messages)

    def close(self) -> None:
        self.server.disconnect()


def main() -> None:
    server = ResidentServer()

    client_a = server.connect()
    client_a.send("s1", "first client message")
    client_a.close()

    client_b = server.connect()
    client_b.send("s1", "second client message after reconnect")

    print("clients connected:", server.client_count)
    print("session history:", client_b.history("s1"))


if __name__ == "__main__":
    main()
