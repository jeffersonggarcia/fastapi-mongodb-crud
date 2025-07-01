from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings
import logging

class Database:
    client: AsyncIOMotorClient = None
    
db_instance = Database()

async def get_database() -> AsyncIOMotorClient:
    return db_instance.client

async def connect_to_mongo():
    """Conectar ao MongoDB"""
    try:
        db_instance.client = AsyncIOMotorClient(settings.MONGO_URL)
        # Testar a conexão
        await db_instance.client.admin.command('ping')
        logging.info("Conectado ao MongoDB com sucesso!")
    except Exception as e:
        logging.error(f"Erro ao conectar ao MongoDB: {e}")
        raise

async def close_mongo_connection():
    """Fechar conexão com MongoDB"""
    if db_instance.client:
        db_instance.client.close()
        logging.info("Conexão com MongoDB fechada")

# Para compatibilidade com o código existente
client = AsyncIOMotorClient(settings.MONGO_URL)
db = client[settings.DATABASE_NAME]