"""Start a local Twilight Imperium 4 game."""

from __future__ import annotations

import atexit
import argparse
import json
import os
import queue
import shutil
import socketserver
import sys
import tempfile
import threading
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parent.parent
SERVER_DIR = ROOT_DIR / "Server"
CLIENT_DIR = ROOT_DIR / "Client"
_runtime_directory: Path | None = None


def _configure_imports() -> None:
    """Make the existing server and client modules importable from any cwd."""
    for path in (ROOT_DIR, SERVER_DIR, CLIENT_DIR):
        path_string = str(path)
        if path_string not in sys.path:
            sys.path.insert(0, path_string)


def start_game(victory_points: int = 10):
    """Create and initialize a game, returning the game manager."""
    _configure_imports()

    import Game

    global _runtime_directory
    _runtime_directory = Path(tempfile.mkdtemp(prefix="ti4-server-"))
    _expose_data(CLIENT_DIR / "Assets", _runtime_directory / "Assets")
    _expose_data(CLIENT_DIR / "Objectives", _runtime_directory / "Objectives")
    _expose_data(SERVER_DIR / "System_Tiles", _runtime_directory / "System_Tiles")
    _expose_data(SERVER_DIR / "Systems.json", _runtime_directory / "Systems.json")
    _expose_data(SERVER_DIR / "Technologies.json", _runtime_directory / "Technologies.json")

    os.chdir(_runtime_directory)
    game = Game.Game(victory_points)
    game.GenerateMap()

    return game


def _cleanup_runtime_directory() -> None:
    if _runtime_directory is not None:
        shutil.rmtree(_runtime_directory, ignore_errors=True)


atexit.register(_cleanup_runtime_directory)


def _expose_data(source: Path, destination: Path) -> None:
    """Expose a data path in the runtime directory, with a copy fallback."""
    try:
        if source.is_dir():
            destination.symlink_to(source, target_is_directory=True)
        else:
            destination.symlink_to(source)
    except (OSError, NotImplementedError):
        if source.is_dir():
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)


def _game_state(game) -> dict[str, Any]:
    """Return the public game state that can be sent to connected clients."""
    return {
        "victory_points_to_win": game.VPtoWin,
        "speaker": game.Speaker,
        "selected_system": game.SelectedSystem,
        "selected_strategy_card": game.SelectedStratCard,
        "selected_objective": game.SelectedObjective,
        "active_system": game.ActiveSystem,
        "active_player": game.ActivePlayer,
        "players": [
            {
                "id": player.PlayerID,
                "name": player.PlayerName,
                "colour": player.Colour,
                "race": player.Race.RaceName,
                "victory_points": player.VP,
                "strategy_card": player.StrategyCard,
                "passed": player.Passed,
                "eliminated": player.Eliminated,
                "tactics_tokens": player.TacticsTokens,
                "fleet_tokens": player.FleetTokens,
                "strategy_tokens": player.StrategyTokens,
                "resources": player.Resources,
                "influence": player.Influence,
                "trade_goods": player.TradeGoods,
                "propulsion_techs": player.PropulsionTechs,
                "biological_techs": player.BiologicalTechs,
                "cybernetic_techs": player.CyberneticTechs,
                "warfare_techs": player.WarfareTechs
            }
            for player in game.Players
        ],
        "map": [
            {
                "system_id": tile.SystemID,
                "tile_number": tile.TileNumber,
                "hex_coords": list(tile.HexCoords),
                "activated_by": list(tile.ActivatedBy),
                "anomaly": getattr(tile.Anomaly, "name", str(tile.Anomaly)),
                "contains_alpha_wormhole": tile.ContainsAlpha,
                "contains_beta_wormhole": tile.ContainsBeta,
                "planets": [
                    {
                        "name": planet.PlanetName,
                        "resources": planet.Resources,
                        "influence": planet.Influence,
                        "type": getattr(planet.PlanetType, "name", str(planet.PlanetType)),
                        "tapped": planet.Tapped,
                        "owned_by": planet.OwnedBy,
                    }
                    for planet in tile.Planets
                ],
            }
            for tile in game.Map.tiles
        ],
    }


class _ClientHandler(socketserver.StreamRequestHandler):
    """Send the initial state and enqueue messages received from one client."""

    def handle(self) -> None:
        print(f"Client connected: {self.client_address[0]}:{self.client_address[1]}")
        self._send_state()

        for line in self.rfile:
            if line.strip() == b"get_state":
                self._send_state()
                continue

            try:
                message = json.loads(line)
            except (json.JSONDecodeError, UnicodeDecodeError):
                self._send_message({"type": "error", "error": "Invalid JSON message."})
                continue

            self.server.incoming_messages.put((self.client_address, message))
            self._send_message({"type": "message_received"})

        print(f"Client disconnected: {self.client_address[0]}:{self.client_address[1]}")

    def _send_state(self) -> None:
        message = {"type": "game_state", "data": _game_state(self.server.game)}
        self._send_message(message)

    def _send_message(self, message: dict[str, Any]) -> None:
        self.wfile.write(json.dumps(message).encode("utf-8") + b"\n")
        self.wfile.flush()


class GameServer(socketserver.ThreadingTCPServer):
    """Threaded TCP server that sends game state and collects client messages.

    Clients send one JSON value per line. Messages are available to the game
    loop through :meth:`receive_message` as ``(client_address, payload)``.
    """

    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, game: Any, host: str = "127.0.0.1", port: int = 8765):
        super().__init__((host, port), _ClientHandler)
        self.game = game
        self.incoming_messages: queue.Queue[tuple[Any, Any]] = queue.Queue()

    def receive_message(self, timeout: float | None = None) -> tuple[Any, Any]:
        """Wait for and return the next ``(client_address, payload)`` pair."""
        return self.incoming_messages.get(timeout=timeout)

    def process_message(self, client_address: Any, message: Any) -> None:
        """Process a client message using the currently supported commands."""
        if isinstance(message, dict) and message.get("type") == "test_message":
            print(f"Test message from {client_address}: {message.get('content', '')}")
            return

        print(f"Unhandled message from {client_address}: {message}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the TI4 game server.")
    parser.add_argument("--host", default="127.0.0.1", help="Interface to listen on.")
    parser.add_argument("--port", default=8765, type=int, help="TCP port to listen on.")
    args = parser.parse_args()

    game = start_game()
    server = GameServer(game, args.host, args.port)
    print(
        f"TI4 server started on {args.host}:{server.server_address[1]} "
        f"({game.GetNumberOfPlayers()} players, {len(game.Map.tiles)} systems, "
        f"{game.VPtoWin} VP to win)."
    )
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    try:
        while True:
            try:
                client_address, message = server.receive_message(timeout=0.5)
            except queue.Empty:
                continue
            server.process_message(client_address, message)
    except KeyboardInterrupt:
        print("\nStopping TI4 server...")
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()