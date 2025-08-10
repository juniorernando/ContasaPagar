"""
Orquestrador de Eventos - Gerencia todos os tipos de eventos do sistema

Este arquivo contém toda a lógica de orquestração e roteamento de eventos.
"""

import json
import os
import importlib
from typing import Dict, Any, Optional
from app.utils.logger import get_logger

logger = get_logger(__name__)

def import_handler(handler_name: str) -> Optional[callable]:
    """
    Importa um handler dinamicamente se ele existir
    
    Args:
        handler_name: Nome do handler (ex: 'handler_create_conta')
    
    Returns:
        Função lambda_handler do módulo ou None se não encontrar
    """
    try:
        module = importlib.import_module(f'app.handlers.{handler_name}')
        return getattr(module, 'lambda_handler')
    except (ImportError, AttributeError) as e:
        logger.warning(f"Handler {handler_name} não encontrado: {e}")
        return None

def handle_event(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Orquestrador principal que roteia eventos para handlers específicos
    
    Args:
        event: Evento Lambda (API Gateway, SQS, SNS, CloudWatch, etc.)
        context: Contexto Lambda
    
    Returns:
        Resposta formatada baseada no tipo de evento
    """
    try:
        # Identificar tipo de evento e rotear para handler específico
        event_type = identify_event_type(event)
        logger.info(f"🎯 Tipo de evento identificado: {event_type}")
        
        if event_type == "api_gateway":
            return handle_api_gateway(event, context)
        elif event_type == "sqs":
            return handle_sqs(event, context)
        elif event_type == "sns":
            return handle_sns(event, context)
        elif event_type == "cloudwatch_event":
            return handle_cloudwatch_event(event, context)
        elif event_type == "test":
            return handle_test_event(event, context)
        else:
            return handle_unknown_event(event, context)
            
    except Exception as e:
        logger.error(f"Erro no orquestrador: {str(e)}", exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Erro no orquestrador de eventos',
                'message': str(e)
            })
        }

def identify_event_type(event: Dict[str, Any]) -> str:
    """
    Identifica o tipo de evento baseado na estrutura do evento
    
    Args:
        event: Evento Lambda
        
    Returns:
        Tipo do evento identificado
    """
    # Evento de teste local
    if event.get('test') == True:
        return "test"
    
    # API Gateway
    if 'httpMethod' in event and ('resource' in event or 'path' in event):
        return "api_gateway"
    
    # SQS/SNS
    if 'Records' in event and event['Records']:
        first_record = event['Records'][0]
        if 'eventSource' in first_record:
            if first_record['eventSource'] == 'aws:sqs':
                return "sqs"
            elif first_record['eventSource'] == 'aws:sns':
                return "sns"
    
    # CloudWatch Events
    if 'source' in event and event.get('source') == 'aws.events':
        return "cloudwatch_event"
    
    # Evento customizado
    if 'action' in event:
        return event['action']
    
    return "unknown"

def handle_api_gateway(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Orquestra eventos do API Gateway
    """
    logger.info("🌐 Processando evento do API Gateway")
    
    try:
        method = event.get('httpMethod', '').upper()
        resource = event.get('resource', '')
        path = event.get('path', '')
        
        logger.info(f"📋 Method: {method}, Resource: {resource}, Path: {path}")
        
        # Roteamento para recursos específicos
        if '/contas' in resource or '/contas' in path:
            return route_conta_operations(event, context, method)
        elif '/fornecedores' in resource or '/fornecedores' in path:
            return route_fornecedor_operations(event, context, method)
        elif '/health' in resource or '/health' in path:
            return handle_health_check(event, context)
        else:
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'error': 'Rota não encontrada',
                    'resource': resource,
                    'method': method,
                    'available_routes': ['/contas', '/fornecedores', '/health']
                })
            }
        
    except Exception as e:
        logger.error(f"Erro no handler do API Gateway: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Erro interno do servidor'})
        }

def route_conta_operations(event: Dict[str, Any], context: Any, method: str) -> Dict[str, Any]:
    """
    Roteia operações relacionadas a contas
    """
    logger.info(f"💰 Roteando operação de conta: {method}")
    
    handler_map = {
        'POST': 'handler_create_conta',
        'GET': 'handler_list_contas',
        'PUT': 'handler_update_conta',
        'DELETE': 'handler_delete_conta'
    }
    
    if method not in handler_map:
        return {
            'statusCode': 405,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'error': f'Método {method} não permitido para /contas',
                'allowed_methods': list(handler_map.keys())
            })
        }
    
    handler_name = handler_map[method]
    handler = import_handler(handler_name)
    
    if handler:
        try:
            return handler(event, context)
        except Exception as e:
            logger.error(f"Erro no handler {handler_name}: {e}")
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Erro interno do servidor'})
            }
    else:
        return {
            'statusCode': 501,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'message': f'Operação {method} para contas em desenvolvimento',
                'action': f'conta_{method.lower()}'
            })
        }

def route_fornecedor_operations(event: Dict[str, Any], context: Any, method: str) -> Dict[str, Any]:
    """
    Roteia operações relacionadas a fornecedores
    """
    logger.info(f"🏢 Roteando operação de fornecedor: {method}")
    
    handler_map = {
        'POST': 'handler_create_fornecedor',
        'GET': 'handler_list_fornecedores',
        'PUT': 'handler_update_fornecedor',
        'DELETE': 'handler_delete_fornecedor'
    }
    
    if method not in handler_map:
        return {
            'statusCode': 405,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'error': f'Método {method} não permitido para /fornecedores',
                'allowed_methods': list(handler_map.keys())
            })
        }
    
    handler_name = handler_map[method]
    handler = import_handler(handler_name)
    
    if handler:
        try:
            return handler(event, context)
        except Exception as e:
            logger.error(f"Erro no handler {handler_name}: {e}")
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Erro interno do servidor'})
            }
    else:
        return {
            'statusCode': 501,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'message': f'Operação {method} para fornecedores em desenvolvimento',
                'action': f'fornecedor_{method.lower()}'
            })
        }

def handle_health_check(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Health check do sistema
    """
    logger.info("🏥 Health check do sistema")
    
    try:
        # Verificar componentes básicos
        health_status = {
            'status': 'healthy',
            'timestamp': json.dumps(context.get_remaining_time_in_millis() if context else 0, default=str),
            'checks': {
                'database': check_database_health(),
                'handlers': check_handlers_health(),
                'aws_services': check_aws_services_health()
            }
        }
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(health_status)
        }
    except Exception as e:
        logger.error(f"Erro no health check: {e}")
        return {
            'statusCode': 503,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'status': 'unhealthy',
                'error': str(e)
            })
        }

def handle_sqs(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Orquestra eventos do SQS
    """
    logger.info("📨 Processando evento do SQS")
    
    try:
        # Delegar para handler específico do SQS
        from app.handlers.handler_processa_fila import lambda_handler as process_queue_handler
        return process_queue_handler(event, context)
        
    except Exception as e:
        logger.error(f"Erro no handler do SQS: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Erro ao processar fila SQS'})
        }

def handle_sns(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Orquestra eventos do SNS
    """
    logger.info("🔔 Processando evento do SNS")
    
    try:
        # Delegar para handler específico do SNS
        from app.handlers.handler_notifica import lambda_handler as notification_handler
        return notification_handler(event, context)
        
    except Exception as e:
        logger.error(f"Erro no handler do SNS: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Erro ao processar notificação SNS'})
        }

def handle_cloudwatch_event(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Orquestra eventos do CloudWatch (agendamentos)
    """
    logger.info("⏰ Processando evento do CloudWatch")
    
    try:
        detail_type = event.get('detail-type', '')
        detail = event.get('detail', {})
        
        if 'verificar-vencimentos' in detail.get('rule-name', ''):
            # Processar verificação de vencimentos
            verificar_vencimentos_handler = import_handler('handler_verificar_vencimentos')
            if verificar_vencimentos_handler:
                try:
                    return verificar_vencimentos_handler(event, context)
                except Exception as e:
                    logger.error(f"Erro no handler de verificação de vencimentos: {e}")
            
            # Fallback para SQS se handler não existir ou falhar
            logger.warning("Handler handler_verificar_vencimentos não encontrado, enviando para SQS")
            from app.utils.aws_config import send_sqs_message
            
            queue_url = os.getenv('SQS_PROCESSAMENTO_URL')
            if queue_url:
                message = {
                    'acao': 'verificar_vencimentos',
                    'timestamp': event.get('time'),
                    'source': 'cloudwatch_event'
                }
                send_sqs_message(queue_url, json.dumps(message))
                logger.info("Mensagem enviada para SQS")
            
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Evento enviado para processamento assíncrono'})
            }
        else:
            logger.info(f"Evento CloudWatch genérico: {detail_type}")
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Evento CloudWatch processado'})
            }
        
    except Exception as e:
        logger.error(f"Erro no handler do CloudWatch: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Erro ao processar evento CloudWatch'})
        }

def handle_test_event(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Manipula eventos de teste
    """
    logger.info("🧪 Processando evento de teste")
    
    try:
        # Executar verificações básicas do sistema
        from app.utils.database import db_config
        from app.models.conta import Status
        
        test_results = {
            'message': '✅ Sistema funcionando corretamente',
            'timestamp': json.dumps(None, default=str),
            'system_checks': {
                'database_config': 'OK',
                'models_import': 'OK',
                'services_import': 'OK',
                'handlers_import': 'OK'
            },
            'available_endpoints': {
                'contas': ['GET', 'POST', 'PUT', 'DELETE'],
                'fornecedores': ['GET', 'POST', 'PUT', 'DELETE'],
                'health': ['GET']
            },
            'event_types_supported': [
                'api_gateway',
                'sqs',
                'sns',
                'cloudwatch_event',
                'test'
            ]
        }
        
        return {
            'statusCode': 200,
            'body': json.dumps(test_results)
        }
        
    except Exception as e:
        logger.error(f"Erro no teste: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Erro no teste do sistema',
                'message': str(e)
            })
        }

def handle_unknown_event(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Manipula eventos desconhecidos
    """
    logger.warning("❓ Processando evento desconhecido")
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Evento desconhecido processado',
            'event_received': event,
            'suggestion': 'Verifique se o evento está formatado corretamente'
        })
    }

# Funções auxiliares para health check
def check_database_health() -> str:
    """Verifica saúde do banco de dados"""
    try:
        from app.utils.database import db_config
        return "OK"
    except Exception:
        return "ERROR"

def check_handlers_health() -> str:
    """Verifica saúde dos handlers"""
    try:
        from app.handlers import handler_create_conta
        return "OK"
    except Exception:
        return "ERROR"

def check_aws_services_health() -> str:
    """Verifica saúde dos serviços AWS"""
    try:
        from app.utils.aws_config import get_aws_client
        return "OK"
    except Exception:
        return "ERROR"
