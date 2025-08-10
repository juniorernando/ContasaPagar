import json
from app.services.servico_conta import ServicoConta
from app.repositories.conta_repository import ContaRepository
from app.repositories.fornecedor_repository import FornecedorRepository
from app.schemas.conta_schema import ContaCreate
from app.utils.database import db_config
from app.utils.logger import get_logger
from app.utils.aws_config import send_sqs_message
from pydantic import ValidationError
import os

logger = get_logger(__name__)

def lambda_handler(event, context):
    """Handler Lambda para criar conta via API Gateway"""
    try:
        # Parse do body da requisição
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event.get('body', {})
        
        # Validação com Pydantic
        try:
            conta_data = ContaCreate(**body)
        except ValidationError as e:
            logger.error(f"Erro de validação: {e}")
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'error': 'Dados inválidos',
                    'details': e.errors()
                })
            }
        
        # Criar sessão do banco
        session = db_config.get_session()
        
        try:
            # Instanciar repositórios e serviços
            repo_conta = ContaRepository(session)
            repo_fornecedor = FornecedorRepository(session)
            servico_conta = ServicoConta(repo_conta, repo_fornecedor)
            
            # Criar conta
            conta = servico_conta.criar_conta(conta_data)
            
            # Enviar para fila SQS (processamento assíncrono)
            queue_url = os.getenv('SQS_CONTA_CRIADA_URL')
            if queue_url:
                message = {
                    'conta_id': conta.id,
                    'acao': 'conta_criada',
                    'valor': conta.valor,
                    'vencimento': conta.vencimento.isoformat()
                }
                send_sqs_message(queue_url, json.dumps(message))
            
            logger.info(f"Conta criada com sucesso: {conta.id}")
            
            return {
                'statusCode': 201,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'id': conta.id,
                    'descricao': conta.descricao,
                    'valor': conta.valor,
                    'vencimento': conta.vencimento.isoformat(),
                    'status': conta.status.value,
                    'fornecedor_id': conta.fornecedor_id
                })
            }
            
        finally:
            session.close()
            
    except ValueError as e:
        logger.error(f"Erro de negócio: {e}")
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
    except Exception as e:
        logger.error(f"Erro interno: {e}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Erro interno do servidor'})
        }
