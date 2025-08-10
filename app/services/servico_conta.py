from typing import List, Optional
from app.repositories.interfaces import IRepositorioConta, IRepositorioFornecedor
from app.models.conta import Conta, Status
from app.schemas.conta_schema import ContaCreate, ContaUpdate
from loguru import logger
from datetime import date

class ServicoConta:
    def __init__(self, repositorio_conta: IRepositorioConta, repositorio_fornecedor: IRepositorioFornecedor):
        self.repositorio_conta = repositorio_conta
        self.repositorio_fornecedor = repositorio_fornecedor

    def criar_conta(self, dados_conta: ContaCreate) -> Conta:
        """Cria uma nova conta após validações"""
        # Verificar se o fornecedor existe
        fornecedor = self.repositorio_fornecedor.buscar_por_id(dados_conta.fornecedor_id)
        if not fornecedor:
            raise ValueError(f"Fornecedor com ID {dados_conta.fornecedor_id} não encontrado")
        
        # Validar valor positivo
        if dados_conta.valor <= 0:
            raise ValueError("O valor da conta deve ser positivo")
        
        conta = Conta(
            descricao=dados_conta.descricao,
            valor=dados_conta.valor,
            vencimento=dados_conta.vencimento,
            status=Status.ABERTA,
            fornecedor_id=dados_conta.fornecedor_id
        )
        
        conta_salva = self.repositorio_conta.salvar(conta)
        logger.info(f"Conta criada: {conta_salva.id} - {conta_salva.descricao} - R${conta_salva.valor}")
        return conta_salva

    def listar_contas(self, **filtros) -> List[Conta]:
        """Lista contas com filtros opcionais"""
        return self.repositorio_conta.listar(**filtros)

    def buscar_conta(self, conta_id: int) -> Optional[Conta]:
        """Busca conta por ID"""
        return self.repositorio_conta.buscar_por_id(conta_id)

    def marcar_como_paga(self, conta_id: int) -> bool:
        """Marca uma conta como paga"""
        sucesso = self.repositorio_conta.marcar_como_paga(conta_id)
        if sucesso:
            logger.info(f"Conta {conta_id} marcada como paga")
        else:
            logger.warning(f"Não foi possível marcar conta {conta_id} como paga")
        return sucesso

    def atualizar_status_atrasadas(self) -> int:
        """Atualiza automaticamente contas vencidas"""
        quantidade = self.repositorio_conta.atualizar_status_atrasadas()
        logger.info(f"{quantidade} contas marcadas como atrasadas")
        return quantidade

    def listar_contas_por_status(self, status: Status) -> List[Conta]:
        """Lista contas por status específico"""
        return self.listar_contas(status=status)

    def listar_contas_vencendo(self, dias: int = 7) -> List[Conta]:
        """Lista contas que vencem nos próximos X dias"""
        data_limite = date.today()
        from datetime import timedelta
        data_limite += timedelta(days=dias)
        
        return self.listar_contas(
            status=Status.ABERTA,
            data_inicio=date.today(),
            data_fim=data_limite
        )
