from __future__ import annotations

import argparse
import threading
from typing import Any, Callable

from Model import Model, ServerConnection


class Controller:
    """Coordinate network updates from Model with the pygame interface."""

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 8765,
        interface_factory: Callable[[Model, Callable[[dict[str, Any]], None]], Any] | None = None,
    ) -> None:
        self.host = host
        self.port = port
        self.model = Model()
        self.interface_factory = interface_factory or self._load_interface
        self.interface = None

        if host is not None and port is not None:
            self.connection = ServerConnection(self.host, self.port)
        else:
            self.connection = None

    @staticmethod
    def _load_interface(
        model: Model,
        send_command: Callable[[dict[str, Any]], None],
    ) -> Any:
        from Interface import UserInterface

        return UserInterface(model, send_command)

    def run(self, test_message: dict[str, Any] | None = None) -> None:
        """Connect to the server, load the interface, and start its event loop."""

        updates = self.connection.receive()
        try:
            self.model.receive(next(updates))
        except StopIteration as error:
            raise RuntimeError("The server closed before sending game data.") from error

        if test_message is not None:
            print("Received initial game state:", self.model.to_dict())
            self.send_message(test_message)
            print("Sent message:", test_message)
            self.connection = None
            return

        update_thread = threading.Thread(
            target=self._receive_updates,
            args=(updates,),
            daemon=True,
        )
        update_thread.start()
        self.interface = self.interface_factory(self.model, self.send_message)
        self.interface.Main()
        self.connection = None

    def send_message(self, message: dict[str, Any]) -> None:
        """Send a JSON message over the existing server connection."""
        if self.connection is None:
            raise RuntimeError("The controller is not connected to the server.")
        self.connection.send(message)

    def _receive_updates(self, updates: Any) -> None:
        for server_data in updates:
            self.model.receive(server_data)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the TI4 client interface.")
    parser.add_argument("--host", default="127.0.0.1", help="Server address to connect to.")
    parser.add_argument("--port", default=8765, type=int, help="Server port to connect to.")
    args = parser.parse_args()
    controller = Controller(args.host, args.port)
    controller.send_message({"type": "test_message", "content": "Hello, server!"})
    controller.run()


if __name__ == "__main__":
    main()
