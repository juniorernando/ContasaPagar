from pydantic import BaseModel, EmailStr
from typing import Optional

class FornecedorBase(BaseModel):
    nome: str
    documento: str  # CNPJ/CPF
    email: EmailStr
    telefone: str

class FornecedorCreate(FornecedorBase):
    pass

class FornecedorUpdate(BaseModel):
    nome: Optional[str] = None
    documento: Optional[str] = None
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None

class FornecedorResponse(FornecedorBase):
    id: int
    
    class Config:
        from_attributes = True
