from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.conta import Conta, Status
from app.repositories.interfaces import IRepositorioConta
from datetime import date

class ContaRepository(IRepositorioConta):
    def __init__(self, session: Session):
        self.session = session

    def salvar(self, conta: Conta) -> Conta:
        if not conta.status:
            conta.status = Status.ABERTA
        
        self.session.add(conta)
        self.session.commit()
        self.session.refresh(conta)
        return conta

    def listar(self, **filtros) -> List[Conta]:
        query = self.session.query(Conta)
        
        if filtros.get('status'):
            query = query.filter(Conta.status == filtros['status'])
        
        if filtros.get('fornecedor_id'):
            query = query.filter(Conta.fornecedor_id == filtros['fornecedor_id'])
        
        if filtros.get('data_inicio'):
            query = query.filter(Conta.vencimento >= filtros['data_inicio'])
        
        if filtros.get('data_fim'):
            query = query.filter(Conta.vencimento <= filtros['data_fim'])
        
        return query.all()

    def buscar_por_id(self, conta_id: int) -> Optional[Conta]:
        return self.session.query(Conta).filter(Conta.id == conta_id).first()

    def marcar_como_paga(self, conta_id: int) -> bool:
        conta = self.buscar_por_id(conta_id)
        if conta:
            conta.status = Status.PAGA
            self.session.commit()
            return True
        return False

    def atualizar_status_atrasadas(self):
        """Atualiza automaticamente contas vencidas para status ATRASADA"""
        hoje = date.today()
        contas_vencidas = self.session.query(Conta).filter(
            Conta.vencimento < hoje,
            Conta.status == Status.ABERTA
        ).all()
        
        for conta in contas_vencidas:
            conta.status = Status.ATRASADA
        
        self.session.commit()
        return len(contas_vencidas)
