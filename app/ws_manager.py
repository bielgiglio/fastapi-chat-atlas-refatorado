# app/ws_manager.py
from typing import Dict, Set
from fastapi import WebSocket

class WSManager:
    """Gerencia as conexões WebSocket ativas em diferentes salas."""
    def __init__(self):
        self.rooms: Dict[str, Set[WebSocket]] = {}

    async def connect(self, room: str, ws: WebSocket):
        """
        Conecta um novo WebSocket a uma sala.
        """
        await ws.accept()
        self.rooms.setdefault(room, set()).add(ws)

    def disconnect(self, room: str, ws: WebSocket):
        """
        Desconecta um WebSocket de uma sala e remove a sala se estiver vazia.
        """
        connections = self.rooms.get(room)
        if connections and ws in connections:
            connections.remove(ws)
            if not connections:
                self.rooms.pop(room, None)

    async def broadcast(self, room: str, payload: dict):
        """
        Envia uma mensagem (payload) para todos os WebSockets em uma sala.
        Remove conexões inativas se a comunicação falhar.
        """
        active_connections = list(self.rooms.get(room, []))
        for ws in active_connections:
            try:
                await ws.send_json(payload)
            except Exception:
                self.disconnect(room, ws)

manager = WSManager()