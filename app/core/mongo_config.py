from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from app.core.settings import settings

host: str = settings.MONGO_HOST
port: int = settings.MONGO_PORT
client: AsyncIOMotorClient = AsyncIOMotorClient(host=host, port=port)
db: AsyncIOMotorDatabase = client.sampleDB
collection: AsyncIOMotorCollection = db.sample_collection
