import sys
from loguru import logger
import os

def configure_logger():
    """Configura o logger com formato estruturado"""
    # Remove o logger padrão
    logger.remove()
    
    # Formato para desenvolvimento local
    format_local = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    
    # Formato para produção (Lambda)
    format_lambda = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}"
    
    # Determinar se está rodando em Lambda
    is_lambda = os.getenv('AWS_LAMBDA_FUNCTION_NAME') is not None
    
    if is_lambda:
        # Em Lambda, usar stdout com formato simples
        logger.add(
            sys.stdout,
            format=format_lambda,
            level="INFO",
            serialize=False
        )
    else:
        # Desenvolvimento local
        logger.add(
            sys.stdout,
            format=format_local,
            level="DEBUG",
            colorize=True
        )
        
        # Arquivo de log para desenvolvimento
        logger.add(
            "logs/app.log",
            format=format_lambda,
            level="INFO",
            rotation="1 day",
            retention="7 days",
            compression="zip"
        )

def get_logger(name: str = __name__):
    """Retorna logger configurado"""
    configure_logger()
    return logger.bind(service=name)
