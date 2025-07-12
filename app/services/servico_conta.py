from app.repositories.interfaces import IRepositorioConta
from app.models.conta import Conta

class ServicoConta:
    def __init__(self, repositorio: IRepositorioConta):
        self.repositorio = repositorio

    def criar_conta(self, conta: Conta):
        # Lógica de validação e regras de negócio
        self.repositorio.salvar(conta)

    def listar_contas(self, **filtros):
        return self.repositorio.listar(**filtros)

    def marcar_como_paga(self, conta_id: int):
        self.repositorio.marcar_como_paga(conta_id)
