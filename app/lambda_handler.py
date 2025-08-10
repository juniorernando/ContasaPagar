"""
Lambda Handler Principal - Ponto de entrada do sistema de Contas a Pagar

Este arquivo serve apenas como inicializador do sistema.
A orquestração fica nos handlers específicos.
"""

import json
from typing import Dict, Any
from app.utils.logger import get_logger
from app.handlers.orchestrator import handle_event

logger = get_logger(__name__)

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Ponto de entrada principal do sistema
    
    Args:
        event: Evento Lambda
        context: Contexto Lambda
    
    Returns:
        Resposta do handler específico
    """
    try:
        logger.info("🚀 Iniciando sistema de Contas a Pagar")
        logger.info(f"Evento recebido: {json.dumps(event, default=str)}")
        
        # Delegar para o orquestrador nos handlers
        return handle_event(event, context)
        
    except Exception as e:
        logger.error(f"Erro crítico no sistema: {str(e)}", exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Erro crítico do sistema',
                'message': str(e)
            })
        }

# Para execução local/teste
if __name__ == "__main__":
    # Evento de teste local
    test_event = {
        'test': True,
        'message': 'Teste local do sistema'
    }
    
    result = lambda_handler(test_event, None)
    print("🎯 Resultado do teste:")
    print(json.dumps(result, indent=2))
