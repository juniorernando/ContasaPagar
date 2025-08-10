import pytest
from unittest.mock import Mock, patch
import json
from app.handlers.handler_create_conta import lambda_handler

class TestHandlerCreateConta:
    @patch('app.handlers.handler_create_conta.db_config')
    @patch('app.handlers.handler_create_conta.ContaRepository')
    @patch('app.handlers.handler_create_conta.FornecedorRepository')
    @patch('app.handlers.handler_create_conta.ServicoConta')
    def test_lambda_handler_sucesso(self, mock_servico, mock_repo_fornecedor, mock_repo_conta, mock_db_config):
        """Teste do handler Lambda com sucesso"""
        # Arrange
        mock_session = Mock()
        mock_db_config.get_session.return_value = mock_session
        
        mock_conta = Mock()
        mock_conta.id = 1
        mock_conta.descricao = "Conta teste"
        mock_conta.valor = 100.0
        mock_conta.vencimento.isoformat.return_value = "2024-12-31"
        mock_conta.status.value = "Aberta"
        mock_conta.fornecedor_id = 1
        
        mock_servico_instance = mock_servico.return_value
        mock_servico_instance.criar_conta.return_value = mock_conta
        
        event = {
            'body': json.dumps({
                'descricao': 'Conta teste',
                'valor': 100.0,
                'vencimento': '2024-12-31',
                'fornecedor_id': 1
            })
        }
        context = {}
        
        # Act
        response = lambda_handler(event, context)
        
        # Assert
        assert response['statusCode'] == 201
        body = json.loads(response['body'])
        assert body['id'] == 1
        assert body['descricao'] == "Conta teste"
        mock_session.close.assert_called_once()
    
    @patch('app.handlers.handler_create_conta.db_config')
    def test_lambda_handler_dados_invalidos(self, mock_db_config):
        """Teste do handler Lambda com dados inválidos"""
        # Arrange
        event = {
            'body': json.dumps({
                'descricao': '',  # Descrição vazia
                'valor': 'não é número',  # Valor inválido
                'vencimento': 'data inválida',
                'fornecedor_id': 'não é número'
            })
        }
        context = {}
        
        # Act
        response = lambda_handler(event, context)
        
        # Assert
        assert response['statusCode'] == 400
        body = json.loads(response['body'])
        assert 'error' in body
        assert body['error'] == 'Dados inválidos'
