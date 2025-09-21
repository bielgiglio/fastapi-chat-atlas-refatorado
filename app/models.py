# app/models.py
from pydantic import BaseModel, Field
from datetime import datetime

class MessageIn(BaseModel):
    """Modelo de entrada para uma nova mensagem."""
    username: str = Field(..., min_length=1, max_length=50)
    content: str = Field(..., min_length=1, max_length=1000)

class MessageOut(BaseModel):
    """Modelo de saída para uma mensagem, incluindo dados gerados pelo servidor."""
    id: str = Field(..., alias="_id")
    room: str
    username: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True  # Renomeado de orm_mode
        populate_by_name = True # Renomeado de allow_population_by_field_name