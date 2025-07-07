from motor.motor_asyncio import AsyncIOMotorClient
from ..core.config import settings

class Database:
    client: AsyncIOMotorClient = None
    db = None

    @classmethod
    async def connect_to_mongo(cls):
        cls.client = AsyncIOMotorClient(settings.MONGODB_URL)
        cls.db = cls.client[settings.DATABASE_NAME]
        # Test the connection
        await cls.db.command('ping')
        print("Connected to MongoDB!")

    @classmethod
    async def close_mongo_connection(cls):
        if cls.client:
            cls.client.close()
            print("MongoDB connection closed.")

    @classmethod
    def get_collection(cls, collection_name: str):
        if not cls.db:
            raise RuntimeError("Database is not initialized. Call connect_to_mongo() first.")
        return cls.db[collection_name]

# Initialize database connection
async def init_db():
    await Database.connect_to_mongo()

# Close database connection
async def close_db():
    await Database.close_mongo_connection()

# Dependency to get database collection
def get_collection(collection_name: str):
    return Database.get_collection(collection_name)
