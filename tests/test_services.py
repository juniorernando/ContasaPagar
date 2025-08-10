import pytest
from datetime import date, timedelta
from app.models.conta import Conta, Status
from app.models.fornecedor import Fornecedor
from app.schemas.conta_schema import ContaCreate
from app.schemas.fornecedor_schema import FornecedorCreate
from app.services.servico_conta import ServicoConta
from app.services.servico_fornecedor import ServicoFornecedor
from unittest.mock import Mock

class TestServicoConta:
    def setup_method(self):
        """Setup para cada teste"""
        self.repo_conta_mock = Mock()
        self.repo_fornecedor_mock = Mock()
        self.servico_conta = ServicoConta(self.repo_conta_mock, self.repo_fornecedor_mock)
    
    def test_criar_conta_sucesso(self):
        """Teste de criação de conta com sucesso"""
        # Arrange
        fornecedor = Fornecedor(id=1, nome="Teste", documento="123", email="test@test.com", telefone="123")
        self.repo_fornecedor_mock.buscar_por_id.return_value = fornecedor
        
        conta_criada = Conta(
            id=1,
            descricao="Conta teste",
            valor=100.0,
            vencimento=date.today(),
            status=Status.ABERTA,
            fornecedor_id=1
        )
        self.repo_conta_mock.salvar.return_value = conta_criada
        
        conta_data = ContaCreate(
            descricao="Conta teste",
            valor=100.0,
            vencimento=date.today(),
            fornecedor_id=1
        )
        
        # Act
        resultado = self.servico_conta.criar_conta(conta_data)
        
        # Assert
        assert resultado.descricao == "Conta teste"
        assert resultado.valor == 100.0
        assert resultado.status == Status.ABERTA
        self.repo_fornecedor_mock.buscar_por_id.assert_called_once_with(1)
        self.repo_conta_mock.salvar.assert_called_once()
    
    def test_criar_conta_fornecedor_inexistente(self):
        """Teste de criação de conta com fornecedor inexistente"""
        # Arrange
        self.repo_fornecedor_mock.buscar_por_id.return_value = None
        
        conta_data = ContaCreate(
            descricao="Conta teste",
            valor=100.0,
            vencimento=date.today(),
            fornecedor_id=999
        )
        
        # Act & Assert
        with pytest.raises(ValueError, match="Fornecedor com ID 999 não encontrado"):
            self.servico_conta.criar_conta(conta_data)
    
    def test_criar_conta_valor_negativo(self):
        """Teste de criação de conta com valor negativo"""
        # Arrange
        fornecedor = Fornecedor(id=1, nome="Teste", documento="123", email="test@test.com", telefone="123")
        self.repo_fornecedor_mock.buscar_por_id.return_value = fornecedor
        
        conta_data = ContaCreate(
            descricao="Conta teste",
            valor=-100.0,
            vencimento=date.today(),
            fornecedor_id=1
        )
        
        # Act & Assert
        with pytest.raises(ValueError, match="O valor da conta deve ser positivo"):
            self.servico_conta.criar_conta(conta_data)
    
    def test_marcar_como_paga(self):
        """Teste de marcação de conta como paga"""
        # Arrange
        self.repo_conta_mock.marcar_como_paga.return_value = True
        
        # Act
        resultado = self.servico_conta.marcar_como_paga(1)
        
        # Assert
        assert resultado is True
        self.repo_conta_mock.marcar_como_paga.assert_called_once_with(1)

class TestServicoFornecedor:
    def setup_method(self):
        """Setup para cada teste"""
        self.repo_fornecedor_mock = Mock()
        self.servico_fornecedor = ServicoFornecedor(self.repo_fornecedor_mock)
    
    def test_criar_fornecedor_sucesso(self):
        """Teste de criação de fornecedor com sucesso"""
        # Arrange
        self.repo_fornecedor_mock.buscar_por_documento.return_value = None
        
        fornecedor_criado = Fornecedor(
            id=1,
            nome="Empresa Teste",
            documento="12345678000190",
            email="teste@empresa.com",
            telefone="11999999999"
        )
        self.repo_fornecedor_mock.salvar.return_value = fornecedor_criado
        
        fornecedor_data = FornecedorCreate(
            nome="Empresa Teste",
            documento="12345678000190",
            email="teste@empresa.com",
            telefone="11999999999"
        )
        
        # Act
        resultado = self.servico_fornecedor.criar_fornecedor(fornecedor_data)
        
        # Assert
        assert resultado.nome == "Empresa Teste"
        assert resultado.documento == "12345678000190"
        self.repo_fornecedor_mock.buscar_por_documento.assert_called_once_with("12345678000190")
        self.repo_fornecedor_mock.salvar.assert_called_once()
    
    def test_criar_fornecedor_documento_duplicado(self):
        """Teste de criação de fornecedor com documento duplicado"""
        # Arrange
        fornecedor_existente = Fornecedor(id=1, nome="Outro", documento="12345678000190", email="outro@test.com", telefone="123")
        self.repo_fornecedor_mock.buscar_por_documento.return_value = fornecedor_existente
        
        fornecedor_data = FornecedorCreate(
            nome="Empresa Teste",
            documento="12345678000190",
            email="teste@empresa.com",
            telefone="11999999999"
        )
        
        # Act & Assert
        with pytest.raises(ValueError, match="Já existe um fornecedor com o documento"):
            self.servico_fornecedor.criar_fornecedor(fornecedor_data)
