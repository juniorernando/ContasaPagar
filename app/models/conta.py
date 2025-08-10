from sqlalchemy import Column, Integer, String, Float, Date, Enum, ForeignKey
from .base import Base
import enum

class Status(enum.Enum):
    ABERTA = 'Aberta'
    PAGA = 'Paga'
    ATRASADA = 'Atrasada'

class Conta(Base):
    __tablename__ = "contas"
    id = Column(Integer, primary_key=True)
    descricao = Column(String)
    valor = Column(Float)
    vencimento = Column(Date)
    status = Column(Enum(Status))
    fornecedor_id = Column(Integer, ForeignKey("fornecedores.id"))
