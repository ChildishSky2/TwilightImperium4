from __future__ import annotations

import json
import socket
from typing import Any, Iterator


SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8765


class ServerConnection:
    """Persistent newline-delimited JSON connection to the main game server."""

    def __init__(self, host: str = SERVER_HOST, port: int = SERVER_PORT) -> None:
        self.socket = socket.create_connection((host, port))
        self.stream = self.socket.makefile("r", encoding="utf-8")

    def send(self, message: dict[str, Any]) -> None:
        """Send a client command over the same connection used for updates."""
        payload = json.dumps(message).encode("utf-8") + b"\n"
        self.socket.sendall(payload)

    def receive(self) -> Iterator[dict[str, Any]]:
        """Yield game data from each server game_state message."""
        for line in self.stream:
            message = json.loads(line)
            if message.get("type") == "game_state":
                yield message.get("data", {})

    def close(self) -> None:
        self.stream.close()
        self.socket.close()

    def __enter__(self) -> ServerConnection:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()



class Model:
    """Client-side view of the JSON game state sent by the server."""

    def __init__(self, server_data: dict[str, Any] | None = None) -> None:
        self.game: dict[str, Any] = {}
        self.players: list[dict[str, Any]] = []
        self.tiles: list[dict[str, Any]] = []
        self.public_objectives: list[Any] = []
        self.vp_to_win = 10
        self.active_system = None
        self.active_player = 0
        self.turn = 0
        self.selected_system = None
        self.selected_strategy_card = None
        self.selected_objective = None
        self.speaker = None
        self.phase = None

        if server_data is not None:
            self.receive(server_data)

    def receive(self, message: dict[str, Any]) -> Model:
        """Update the view from game data or a complete game_state message."""
        if message.get("type") == "game_state":
            message = message.get("data", {})

        self.game = message
        self.active_player = message.get("active_player", 0)
        self.turn = message.get("turn", self.active_player)
        self.vp_to_win = message.get("victory_points_to_win", 10)
        self.active_system = message.get("active_system")
        self.selected_system = message.get("selected_system")
        self.selected_strategy_card = message.get("selected_strategy_card")
        self.selected_objective = message.get("selected_objective")
        self.speaker = message.get("speaker")
        self.players = [self._normalize_player(player) for player in message.get("players", [])]
        self.tiles = [self._normalize_tile(tile) for tile in message.get("map", message.get("tiles", []))]
        self.public_objectives = message.get("public_objectives", [])
        self.phase = message.get("phase")
        return self

    @staticmethod
    def _normalize_player(player: dict[str, Any]) -> dict[str, Any]:
        get = player.get
        return {
            "id": get("id"),
            "name": get("name", ""),
            "colour": tuple(get("colour", (0, 0, 0))),
            "race": get("race"),
            "vp": get("victory_points", get("vp", 0)),
            "strategy_card": get("strategy_card"),
            "passed": get("passed", False),
            "eliminated": get("eliminated", False),
            "resources": get("resources", 0),
            "influence": get("influence", 0),
            "commodities": get("commodities", 0),
            "trade_goods": get("trade_goods", 0),
            "tactics_tokens": get("tactics_tokens", 0),
            "fleet_tokens": get("fleet_tokens", 0),
            "strategy_tokens": get("strategy_tokens", 0),
            "propulsion_techs": get("propulsion_techs", 0),
            "biological_techs": get("biological_techs", 0),
            "cybernetic_techs": get("cybernetic_techs", 0),
            "warfare_techs": get("warfare_techs", 0),
        }

    @staticmethod
    def _normalize_tile(tile: dict[str, Any]) -> dict[str, Any]:
        get = tile.get
        return {
            "system_id": get("system_id"),
            "tile_number": get("tile_number"),
            "hex_coords": tuple(get("hex_coords", ())),
            "activated_by": get("activated_by", []),
            "ships_in_space": get("ships_in_space", []),
            "planets": get("planets", []),
            "anomaly": get("anomaly"),
            "contains_alpha": get("contains_alpha_wormhole", get("contains_alpha", False)),
            "contains_beta": get("contains_beta_wormhole", get("contains_beta", False)),
        }

    @classmethod
    def from_server(cls, server_data: dict[str, Any]) -> Model:
        """Construct a model from received server game data."""
        return cls(server_data)

    def to_dict(self) -> dict[str, Any]:
        return {
            "active_player": self.active_player,
            "turn": self.turn,
            "vp_to_win": self.vp_to_win,
            "active_system": self.active_system,
            "selected_system": self.selected_system,
            "selected_strategy_card": self.selected_strategy_card,
            "selected_objective": self.selected_objective,
            "speaker": self.speaker,
            "phase": self.phase,
            "players": self.players,
            "tiles": self.tiles,
            "public_objectives": self.public_objectives,
        }

    def __repr__(self) -> str:
        return f"Model(turn={self.turn}, players={len(self.players)}, tiles={len(self.tiles)})"
