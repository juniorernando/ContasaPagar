from typing import List, Optional
from app.repositories.interfaces import IRepositorioFornecedor
from app.models.fornecedor import Fornecedor
from app.schemas.fornecedor_schema import FornecedorCreate, FornecedorUpdate
from loguru import logger

class ServicoFornecedor:
    def __init__(self, repositorio: IRepositorioFornecedor):
        self.repositorio = repositorio

    def criar_fornecedor(self, dados_fornecedor: FornecedorCreate) -> Fornecedor:
        """Cria um novo fornecedor após validações"""
        # Verificar se já existe fornecedor com o mesmo documento
        fornecedor_existente = self.repositorio.buscar_por_documento(dados_fornecedor.documento)
        if fornecedor_existente:
            raise ValueError(f"Já existe um fornecedor com o documento {dados_fornecedor.documento}")
        
        fornecedor = Fornecedor(
            nome=dados_fornecedor.nome,
            documento=dados_fornecedor.documento,
            email=dados_fornecedor.email,
            telefone=dados_fornecedor.telefone
        )
        
        fornecedor_salvo = self.repositorio.salvar(fornecedor)
        logger.info(f"Fornecedor criado: {fornecedor_salvo.id} - {fornecedor_salvo.nome}")
        return fornecedor_salvo

    def listar_fornecedores(self) -> List[Fornecedor]:
        """Lista todos os fornecedores"""
        return self.repositorio.listar()

    def buscar_fornecedor(self, fornecedor_id: int) -> Optional[Fornecedor]:
        """Busca fornecedor por ID"""
        return self.repositorio.buscar_por_id(fornecedor_id)

    def atualizar_fornecedor(self, fornecedor_id: int, dados: FornecedorUpdate) -> Optional[Fornecedor]:
        """Atualiza dados do fornecedor"""
        dados_dict = dados.dict(exclude_unset=True)
        
        # Se está atualizando documento, verificar se não existe outro com o mesmo
        if 'documento' in dados_dict:
            fornecedor_existente = self.repositorio.buscar_por_documento(dados_dict['documento'])
            if fornecedor_existente and fornecedor_existente.id != fornecedor_id:
                raise ValueError(f"Já existe outro fornecedor com o documento {dados_dict['documento']}")
        
        fornecedor_atualizado = self.repositorio.atualizar(fornecedor_id, dados_dict)
        if fornecedor_atualizado:
            logger.info(f"Fornecedor atualizado: {fornecedor_atualizado.id} - {fornecedor_atualizado.nome}")
        
        return fornecedor_atualizado

    def excluir_fornecedor(self, fornecedor_id: int) -> bool:
        """Exclui um fornecedor"""
        sucesso = self.repositorio.excluir(fornecedor_id)
        if sucesso:
            logger.info(f"Fornecedor excluído: {fornecedor_id}")
        return sucesso
