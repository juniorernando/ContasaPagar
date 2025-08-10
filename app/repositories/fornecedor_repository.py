from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.fornecedor import Fornecedor
from app.repositories.interfaces import IRepositorioFornecedor

class FornecedorRepository(IRepositorioFornecedor):
    def __init__(self, session: Session):
        self.session = session

    def salvar(self, fornecedor: Fornecedor) -> Fornecedor:
        self.session.add(fornecedor)
        self.session.commit()
        self.session.refresh(fornecedor)
        return fornecedor

    def listar(self) -> List[Fornecedor]:
        return self.session.query(Fornecedor).all()

    def buscar_por_id(self, fornecedor_id: int) -> Optional[Fornecedor]:
        return self.session.query(Fornecedor).filter(Fornecedor.id == fornecedor_id).first()

    def buscar_por_documento(self, documento: str) -> Optional[Fornecedor]:
        return self.session.query(Fornecedor).filter(Fornecedor.documento == documento).first()

    def excluir(self, fornecedor_id: int) -> bool:
        fornecedor = self.buscar_por_id(fornecedor_id)
        if fornecedor:
            self.session.delete(fornecedor)
            self.session.commit()
            return True
        return False

    def atualizar(self, fornecedor_id: int, dados: dict) -> Optional[Fornecedor]:
        fornecedor = self.buscar_por_id(fornecedor_id)
        if fornecedor:
            for key, value in dados.items():
                if hasattr(fornecedor, key) and value is not None:
                    setattr(fornecedor, key, value)
            self.session.commit()
            return fornecedor
        return None
