import os

import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.dal import DBManager


@pytest.fixture()
def setup_and_teardown_db():
    client = AsyncIOMotorClient('localhost', 27018)
    db = client.sampleDB
    collection = db.sample_collection
    manager = DBManager(collection)
    os.system('docker compose -f docker-compose-test.yml up -d')
    yield manager
    os.system('docker compose -f docker-compose-test.yml down -v')
