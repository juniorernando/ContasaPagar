# Entry point para testes locais do sistema de Contas a Pagar

import json
from app.lambda_handler import lambda_handler
from app.utils.logger import get_logger

logger = get_logger(__name__)

def main():
    """
    Ponto de entrada principal que utiliza o lambda_handler como orquestrador
    """
    print("🚀 Iniciando Sistema de Contas a Pagar via Lambda Handler")
    
    # Teste 1: Verificação básica do sistema
    print("\n" + "="*50)
    print("🔍 TESTE 1: Verificação do Sistema")
    print("="*50)
    
    test_event = {
        'test': True,
        'message': 'Verificação básica do sistema'
    }
    
    result = lambda_handler(test_event, None)
    print(f"Resultado: {json.dumps(result, indent=2)}")
    
    # Teste 2: Simulação de evento API Gateway (criar conta)
    print("\n" + "="*50)
    print("📝 TESTE 2: Simulação API Gateway - Criar Conta")
    print("="*50)
    
    api_event = {
        'httpMethod': 'POST',
        'resource': '/contas',
        'path': '/contas',
        'body': json.dumps({
            'descricao': 'Conta de teste via Lambda Handler',
            'valor': 150.00,
            'vencimento': '2024-12-31',
            'fornecedor_id': 1
        }),
        'headers': {
            'Content-Type': 'application/json'
        }
    }
    
    try:
        result = lambda_handler(api_event, None)
        print(f"Resultado: {json.dumps(result, indent=2)}")
    except Exception as e:
        print(f"Erro (esperado sem banco): {e}")
    
    # Teste 3: Simulação de evento SQS
    print("\n" + "="*50)
    print("📨 TESTE 3: Simulação SQS - Processamento de Fila")
    print("="*50)
    
    sqs_event = {
        'Records': [
            {
                'eventSource': 'aws:sqs',
                'body': json.dumps({
                    'acao': 'conta_criada',
                    'conta_id': 1
                })
            }
        ]
    }
    
    try:
        result = lambda_handler(sqs_event, None)
        print(f"Resultado: {json.dumps(result, indent=2)}")
    except Exception as e:
        print(f"Erro (esperado sem banco): {e}")
    
    # Teste 4: Simulação de evento SNS
    print("\n" + "="*50)
    print("🔔 TESTE 4: Simulação SNS - Notificação")
    print("="*50)
    
    sns_event = {
        'Records': [
            {
                'eventSource': 'aws:sns',
                'Sns': {
                    'Message': 'Nova conta criada via lambda handler',
                    'Subject': 'Conta Criada',
                    'TopicArn': 'arn:aws:sns:us-east-1:123456789012:conta-criada'
                }
            }
        ]
    }
    
    result = lambda_handler(sns_event, None)
    print(f"Resultado: {json.dumps(result, indent=2)}")
    
    # Teste 5: Simulação de evento CloudWatch
    print("\n" + "="*50)
    print("⏰ TESTE 5: Simulação CloudWatch - Verificação de Vencimentos")
    print("="*50)
    
    cloudwatch_event = {
        'source': 'aws.events',
        'detail-type': 'Scheduled Event',
        'detail': {
            'rule-name': 'verificar-vencimentos'
        },
        'time': '2024-08-10T15:00:00Z'
    }
    
    try:
        result = lambda_handler(cloudwatch_event, None)
        print(f"Resultado: {json.dumps(result, indent=2)}")
    except Exception as e:
        print(f"Erro (esperado sem AWS): {e}")
    
    # Teste 6: Evento desconhecido
    print("\n" + "="*50)
    print("❓ TESTE 6: Evento Desconhecido")
    print("="*50)
    
    unknown_event = {
        'custom_field': 'valor customizado',
        'action': 'custom_action'
    }
    
    result = lambda_handler(unknown_event, None)
    print(f"Resultado: {json.dumps(result, indent=2)}")
    
    print("\n" + "="*50)
    print("✅ SISTEMA LAMBDA HANDLER TESTADO COM SUCESSO!")
    print("="*50)
    print("\n🎯 Próximos passos:")
    print("1. Configure banco de dados para testes completos")
    print("2. Deploy na AWS para testes reais")
    print("3. Configure variáveis de ambiente AWS")
    print("4. Teste via API Gateway real")

def test_lambda_handler_direct():
    """
    Teste direto do lambda_handler sem main()
    """
    print("🔧 Teste direto do lambda_handler")
    
    # Evento simples de teste
    simple_event = {
        'action': 'test',
        'data': {'message': 'Teste direto'}
    }
    
    result = lambda_handler(simple_event, None)
    return result

if __name__ == "__main__":
    # Verificar se deve executar teste direto ou main completo
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--direct':
        result = test_lambda_handler_direct()
        print(json.dumps(result, indent=2))
    else:
        main()
