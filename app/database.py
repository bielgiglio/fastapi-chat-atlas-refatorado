# app/database.py
from typing import Optional, Dict, Any
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
from .config import MONGO_URL, MONGO_DB

_client: Optional[AsyncIOMotorClient] = None

def db() -> AsyncIOMotorClient:
    """
    Retorna uma instância do cliente do banco de dados MongoDB.
    A conexão é estabelecida na primeira chamada e reutilizada nas subsequentes.
    """
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(MONGO_URL)
    return _client[MONGO_DB]

def serialize(doc: Dict[str, Any]) -> Dict[str, Any]:
    """
    Serializa um documento do MongoDB para um dicionário JSON compatível.
    Converte ObjectId para string e formata datas para o padrão ISO.

    Args:
        doc: O documento do MongoDB.

    Returns:
        O documento serializado.
    """
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
    if "created_at" in doc and isinstance(doc["created_at"], datetime):
        doc["created_at"] = doc["created_at"].replace(tzinfo=timezone.utc).isoformat()
    return doc