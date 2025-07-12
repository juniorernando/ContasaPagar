from sqlalchemy import Column, Integer, String, Float, Date, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

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
