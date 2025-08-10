from abc import ABC, abstractmethod
from typing import List
from app.models.conta import Conta
from app.models.fornecedor import Fornecedor

class IRepositorioConta(ABC):
    @abstractmethod
    def salvar(self, conta: Conta):
        pass
    @abstractmethod
    def listar(self, **filtros) -> List[Conta]:
        pass
    @abstractmethod
    def marcar_como_paga(self, conta_id: int):
        pass
    @abstractmethod
    def buscar_por_id(self, conta_id: int) -> Conta:
        pass

class IRepositorioFornecedor(ABC):
    @abstractmethod
    def salvar(self, fornecedor: Fornecedor):
        pass
    @abstractmethod
    def listar(self) -> List[Fornecedor]:
        pass
    @abstractmethod
    def buscar_por_id(self, fornecedor_id: int) -> Fornecedor:
        pass
    @abstractmethod
    def excluir(self, fornecedor_id: int):
        pass
