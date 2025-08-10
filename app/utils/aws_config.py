import boto3
import os
from typing import Optional
from loguru import logger

def get_aws_client(service_name: str, region: Optional[str] = None):
    """Cria cliente AWS para o serviço especificado"""
    region = region or os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    
    try:
        client = boto3.client(service_name, region_name=region)
        logger.info(f"Cliente AWS criado para {service_name} na região {region}")
        return client
    except Exception as e:
        logger.error(f"Erro ao criar cliente AWS para {service_name}: {str(e)}")
        raise

def get_database_url() -> str:
    """Retorna URL de conexão com o banco de dados"""
    # Para Aurora Serverless com Data API
    cluster_arn = os.getenv('AURORA_CLUSTER_ARN')
    secret_arn = os.getenv('AURORA_SECRET_ARN')
    database_name = os.getenv('DATABASE_NAME', 'contas_a_pagar')
    
    if cluster_arn and secret_arn:
        # Usar Data API do Aurora
        return f"aurora+awsrdsdata://{cluster_arn}/{database_name}?secret_arn={secret_arn}"
    else:
        # Fallback para PostgreSQL tradicional
        host = os.getenv('DB_HOST', 'localhost')
        port = os.getenv('DB_PORT', '5432')
        user = os.getenv('DB_USER', 'postgres')
        password = os.getenv('DB_PASSWORD', '')
        database = os.getenv('DB_NAME', 'contas_a_pagar')
        
        return f"postgresql://{user}:{password}@{host}:{port}/{database}"

def send_sqs_message(queue_url: str, message_body: str, message_attributes: Optional[dict] = None):
    """Envia mensagem para fila SQS"""
    try:
        sqs = get_aws_client('sqs')
        
        params = {
            'QueueUrl': queue_url,
            'MessageBody': message_body
        }
        
        if message_attributes:
            params['MessageAttributes'] = message_attributes
        
        response = sqs.send_message(**params)
        logger.info(f"Mensagem enviada para SQS: {response['MessageId']}")
        return response
    except Exception as e:
        logger.error(f"Erro ao enviar mensagem SQS: {str(e)}")
        raise

def publish_sns_message(topic_arn: str, message: str, subject: Optional[str] = None):
    """Publica mensagem no tópico SNS"""
    try:
        sns = get_aws_client('sns')
        
        params = {
            'TopicArn': topic_arn,
            'Message': message
        }
        
        if subject:
            params['Subject'] = subject
        
        response = sns.publish(**params)
        logger.info(f"Mensagem publicada no SNS: {response['MessageId']}")
        return response
    except Exception as e:
        logger.error(f"Erro ao publicar no SNS: {str(e)}")
        raise
