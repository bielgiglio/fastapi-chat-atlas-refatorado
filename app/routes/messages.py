# app/routes/messages.py
from fastapi import APIRouter, Query, HTTPException, WebSocket, WebSocketDisconnect
from bson import ObjectId
from datetime import datetime, timezone

from ..database import db, serialize
from ..models import MessageIn
from ..ws_manager import manager

router = APIRouter()

@router.get("/rooms/{room}/messages")
async def get_messages(
    room: str, limit: int = Query(20, ge=1, le=100), before_id: str | None = Query(None)
):
    """Obtém o histórico de mensagens de uma sala."""
    query = {"room": room}
    if before_id:
        try:
            query["_id"] = {"$lt": ObjectId(before_id)}
        except Exception:
            raise HTTPException(status_code=400, detail="O 'before_id' fornecido é inválido.")

    cursor = db()["messages"].find(query).sort("_id", -1).limit(limit)
    docs = [serialize(d) async for d in cursor]
    docs.reverse()
    return {"items": docs}

@router.post("/rooms/{room}/messages", status_code=201)
async def post_message(room: str, message: MessageIn):
    """Posta uma nova mensagem em uma sala via REST."""
    doc = {
        "room": room,
        "username": message.username,
        "content": message.content,
        "created_at": datetime.now(timezone.utc),
    }
    res = await db()["messages"].insert_one(doc)
    doc["_id"] = res.inserted_id
    
    # Notifica via WebSocket
    await manager.broadcast(room, {"type": "message", "item": serialize(doc)})
    
    return serialize(doc)

@router.websocket("/ws/{room}")
async def ws_room(ws: WebSocket, room: str):
    """Endpoint WebSocket para comunicação em tempo real."""
    await manager.connect(room, ws)
    try:
        # Envia histórico inicial
        cursor = db()["messages"].find({"room": room}).sort("_id", -1).limit(20)
        items = [serialize(d) async for d in cursor]
        items.reverse()
        await ws.send_json({"type": "history", "items": items})

        while True:
            payload = await ws.receive_json()
            username = str(payload.get("username", "anon"))[:50]
            content = str(payload.get("content", "")).strip()
            
            # Garante que mensagens vazias não sejam salvas
            if not content:
                continue

            doc = {
                "room": room,
                "username": username,
                "content": content,
                "created_at": datetime.now(timezone.utc),
            }
            res = await db()["messages"].insert_one(doc)
            doc["_id"] = res.inserted_id
            await manager.broadcast(room, {"type": "message", "item": serialize(doc)})
    except WebSocketDisconnect:
        manager.disconnect(room, ws)