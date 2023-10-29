from motor.motor_asyncio import AsyncIOMotorCollection
from app.core.mongo_config import collection


class DBManager:

    def __init__(self, db_collection: AsyncIOMotorCollection = collection):
        self._collection: AsyncIOMotorCollection = db_collection

    async def aggregate(self, pipeline: list) -> dict:
        cursor = self._collection.aggregate(pipeline)
        return await anext(cursor)


db = DBManager()
