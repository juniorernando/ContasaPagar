import pytest
from datetime import date
from pydantic import ValidationError
from app.schemas.conta_schema import ContaCreate, ContaUpdate, StatusEnum
from app.schemas.fornecedor_schema import FornecedorCreate, FornecedorUpdate

class TestContaSchema:
    def test_conta_create_valida(self):
        """Teste de criação de schema válido para conta"""
        conta_data = ContaCreate(
            descricao="Conta de energia",
            valor=150.50,
            vencimento=date(2024, 12, 31),
            fornecedor_id=1
        )
        
        assert conta_data.descricao == "Conta de energia"
        assert conta_data.valor == 150.50
        assert conta_data.vencimento == date(2024, 12, 31)
        assert conta_data.fornecedor_id == 1
    
    def test_conta_create_valor_negativo(self):
        """Teste com valor negativo (deve ser validado no serviço)"""
        # O schema aceita valores negativos, a validação é feita no serviço
        conta_data = ContaCreate(
            descricao="Conta teste",
            valor=-100.0,
            vencimento=date(2024, 12, 31),
            fornecedor_id=1
        )
        
        assert conta_data.valor == -100.0
    
    def test_conta_update_parcial(self):
        """Teste de atualização parcial de conta"""
        conta_update = ContaUpdate(
            valor=200.0,
            status=StatusEnum.PAGA
        )
        
        assert conta_update.valor == 200.0
        assert conta_update.status == StatusEnum.PAGA
        assert conta_update.descricao is None
        assert conta_update.vencimento is None

class TestFornecedorSchema:
    def test_fornecedor_create_valido(self):
        """Teste de criação de schema válido para fornecedor"""
        fornecedor_data = FornecedorCreate(
            nome="Empresa XYZ",
            documento="12.345.678/0001-90",
            email="contato@empresaxyz.com",
            telefone="(11) 1234-5678"
        )
        
        assert fornecedor_data.nome == "Empresa XYZ"
        assert fornecedor_data.documento == "12.345.678/0001-90"
        assert fornecedor_data.email == "contato@empresaxyz.com"
        assert fornecedor_data.telefone == "(11) 1234-5678"
    
    def test_fornecedor_email_invalido(self):
        """Teste com email inválido"""
        with pytest.raises(ValidationError):
            FornecedorCreate(
                nome="Empresa XYZ",
                documento="12.345.678/0001-90",
                email="email_invalido",
                telefone="(11) 1234-5678"
            )
    
    def test_fornecedor_update_parcial(self):
        """Teste de atualização parcial de fornecedor"""
        fornecedor_update = FornecedorUpdate(
            nome="Novo Nome",
            telefone="(11) 9999-9999"
        )
        
        assert fornecedor_update.nome == "Novo Nome"
        assert fornecedor_update.telefone == "(11) 9999-9999"
        assert fornecedor_update.documento is None
        assert fornecedor_update.email is None
