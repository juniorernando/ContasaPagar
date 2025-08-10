from pydantic import BaseModel
from datetime import date
from typing import Optional
from enum import Enum

class StatusEnum(str, Enum):
    ABERTA = "Aberta"
    PAGA = "Paga"
    ATRASADA = "Atrasada"

class ContaBase(BaseModel):
    descricao: str
    valor: float
    vencimento: date
    fornecedor_id: int

class ContaCreate(ContaBase):
    pass

class ContaUpdate(BaseModel):
    descricao: Optional[str] = None
    valor: Optional[float] = None
    vencimento: Optional[date] = None
    status: Optional[StatusEnum] = None
    fornecedor_id: Optional[int] = None

class ContaResponse(ContaBase):
    id: int
    status: StatusEnum
    
    class Config:
        from_attributes = True
