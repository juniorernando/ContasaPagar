from abc import ABC, abstractmethod
from typing import List
from app.models.conta import Conta

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
