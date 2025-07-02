from motor.motor_asyncio import AsyncIOMotorClient
from config import settings
import logging

# Cria o cliente MongoDB (Motor)
client = AsyncIOMotorClient(settings.MONGO_URL)

# Seleciona o banco de dados
db = client[settings.DATABASE_NAME]

async def connect_to_mongo():
    """Verifica a conexão com MongoDB"""
    try:
        await client.admin.command('ping')
        logging.info("Conectado ao MongoDB com sucesso!")
    except Exception as e:
        logging.error(f"Erro ao conectar ao MongoDB: {e}")
        raise

async def close_mongo_connection():
    """Fecha a conexão MongoDB"""
    client.close()
    logging.info("Conexão com MongoDB fechada")