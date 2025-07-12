from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Fornecedor(Base):
    __tablename__ = "fornecedores"
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    documento = Column(String)  # CNPJ/CPF
    email = Column(String)
    telefone = Column(String)
