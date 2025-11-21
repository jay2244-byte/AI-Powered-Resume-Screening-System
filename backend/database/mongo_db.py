from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from bson import ObjectId
from typing import Dict, Optional

class MongoDB:
    def __init__(self, uri: str, db_name: str):
        self.uri = uri
        self.db_name = db_name
        self.client = None
        self.db = None

    async def connect(self):
        self.client = AsyncIOMotorClient(self.uri)
        self.db = self.client[self.db_name]
        print("✅ Connected to MongoDB")

    async def disconnect(self):
        if self.client:
            self.client.close()
            print("👋 Disconnected from MongoDB")

    async def store_resume(self, resume_data: Dict) -> ObjectId:
        collection = self.db['resumes']
        result = await collection.insert_one(resume_data)
        return result.inserted_id

    async def get_resume(self, resume_id: str) -> Optional[Dict]:
        collection = self.db['resumes']
        resume = await collection.find_one({'_id': ObjectId(resume_id)})
        if resume:
            resume['_id'] = str(resume['_id'])
        return resume

    async def search_resumes(self, query: Dict) -> list:
        collection = self.db['resumes']
        cursor = collection.find(query).limit(100)
        resumes = await cursor.to_list(length=100)
        for resume in resumes:
            resume['_id'] = str(resume['_id'])
        return resumes
