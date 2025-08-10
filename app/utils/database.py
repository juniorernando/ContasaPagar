from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.models.base import Base
from app.utils.aws_config import get_database_url
from app.utils.logger import get_logger
from typing import Generator
import os

logger = get_logger(__name__)

class DatabaseConfig:
    def __init__(self):
        self.database_url = get_database_url()
        self.engine = None
        self.SessionLocal = None
        self._initialize()
    
    def _initialize(self):
        """Inicializa engine e sessão do SQLAlchemy"""
        try:
            # Configurações específicas para diferentes ambientes
            if 'aurora+awsrdsdata' in self.database_url:
                # Para Aurora Data API (instalação adicional necessária)
                # pip install sqlalchemy-aurora-data-api
                try:
                    from sqlalchemy_aurora_data_api import register_dialects
                    register_dialects()
                except ImportError:
                    logger.warning("sqlalchemy-aurora-data-api não instalado, usando PostgreSQL padrão")
                    self.database_url = self.database_url.replace('aurora+awsrdsdata', 'postgresql')
                
                self.engine = create_engine(
                    self.database_url,
                    echo=os.getenv('SQL_ECHO', 'false').lower() == 'true'
                )
            else:
                # Para PostgreSQL tradicional
                self.engine = create_engine(
                    self.database_url,
                    pool_size=5,
                    max_overflow=10,
                    echo=os.getenv('SQL_ECHO', 'false').lower() == 'true'
                )
            
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            logger.info("Configuração de banco de dados inicializada")
            
        except Exception as e:
            logger.error(f"Erro ao configurar banco de dados: {str(e)}")
            raise
    
    def create_tables(self):
        """Cria todas as tabelas do banco"""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Tabelas criadas no banco de dados")
        except Exception as e:
            logger.error(f"Erro ao criar tabelas: {str(e)}")
            raise
    
    def get_session(self) -> Session:
        """Retorna uma nova sessão do banco de dados"""
        return self.SessionLocal()

# Instância global da configuração
db_config = DatabaseConfig()

def get_db_session() -> Generator[Session, None, None]:
    """Dependency injection para sessão do banco"""
    session = db_config.get_session()
    try:
        yield session
    finally:
        session.close()

def init_database():
    """Inicializa o banco de dados criando as tabelas"""
    db_config.create_tables()
