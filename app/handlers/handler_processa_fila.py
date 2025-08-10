import json
from app.services.servico_conta import ServicoConta
from app.repositories.conta_repository import ContaRepository
from app.repositories.fornecedor_repository import FornecedorRepository
from app.utils.database import db_config
from app.utils.logger import get_logger
from app.utils.aws_config import publish_sns_message
import os

logger = get_logger(__name__)

def lambda_handler(event, context):
    """Handler Lambda para processar mensagens SQS"""
    try:
        # Processar cada mensagem da fila
        for record in event.get('Records', []):
            try:
                # Parse da mensagem SQS
                message_body = json.loads(record['body'])
                
                logger.info(f"Processando mensagem: {message_body}")
                
                # Criar sessão do banco
                session = db_config.get_session()
                
                try:
                    # Instanciar serviços
                    repo_conta = ContaRepository(session)
                    repo_fornecedor = FornecedorRepository(session)
                    servico_conta = ServicoConta(repo_conta, repo_fornecedor)
                    
                    # Processar diferentes tipos de ação
                    acao = message_body.get('acao')
                    
                    if acao == 'conta_criada':
                        processar_conta_criada(servico_conta, message_body)
                    elif acao == 'verificar_vencimentos':
                        processar_verificacao_vencimentos(servico_conta)
                    elif acao == 'marcar_como_paga':
                        processar_pagamento(servico_conta, message_body)
                    else:
                        logger.warning(f"Ação não reconhecida: {acao}")
                
                finally:
                    session.close()
                    
            except Exception as e:
                logger.error(f"Erro ao processar mensagem: {e}")
                # Em produção, você pode decidir se rejeita a mensagem ou não
                continue
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Mensagens processadas com sucesso'})
        }
        
    except Exception as e:
        logger.error(f"Erro no handler SQS: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Erro ao processar mensagens'})
        }

def processar_conta_criada(servico_conta, message_body):
    """Processa notificação de conta criada"""
    conta_id = message_body.get('conta_id')
    conta = servico_conta.buscar_conta(conta_id)
    
    if conta:
        # Enviar notificação SNS
        topic_arn = os.getenv('SNS_CONTA_CRIADA_TOPIC')
        if topic_arn:
            mensagem = f"Nova conta criada: {conta.descricao} - R${conta.valor} - Vencimento: {conta.vencimento}"
            publish_sns_message(topic_arn, mensagem, "Nova Conta a Pagar")
        
        logger.info(f"Processamento pós-criação concluído para conta {conta_id}")

def processar_verificacao_vencimentos(servico_conta):
    """Verifica e notifica sobre contas vencendo"""
    # Atualizar status de contas atrasadas
    contas_atrasadas = servico_conta.atualizar_status_atrasadas()
    
    # Buscar contas vencendo nos próximos 3 dias
    contas_vencendo = servico_conta.listar_contas_vencendo(dias=3)
    
    if contas_vencendo:
        topic_arn = os.getenv('SNS_VENCIMENTOS_TOPIC')
        if topic_arn:
            mensagem = f"Atenção! {len(contas_vencendo)} contas vencem nos próximos 3 dias"
            publish_sns_message(topic_arn, mensagem, "Alerta de Vencimentos")
    
    logger.info(f"Verificação de vencimentos: {contas_atrasadas} atrasadas, {len(contas_vencendo)} vencendo")

def processar_pagamento(servico_conta, message_body):
    """Processa marcação de conta como paga"""
    conta_id = message_body.get('conta_id')
    sucesso = servico_conta.marcar_como_paga(conta_id)
    
    if sucesso:
        # Notificar pagamento
        topic_arn = os.getenv('SNS_PAGAMENTO_TOPIC')
        if topic_arn:
            conta = servico_conta.buscar_conta(conta_id)
            mensagem = f"Conta paga: {conta.descricao} - R${conta.valor}"
            publish_sns_message(topic_arn, mensagem, "Conta Paga")
        
        logger.info(f"Pagamento processado para conta {conta_id}")
    else:
        logger.error(f"Falha ao processar pagamento da conta {conta_id}")
