from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017")
db = client["nyse_tracker"]
col = db["most_active"]

doc = {"Symbol":"TEST","Name":"Smoke Test","Price":"0.00","Change":"0%","Volume":"0","timestamp":datetime.utcnow()}
col.insert_one(doc)
print("Inserted 1 doc")
print("Count:", col.count_documents({}))
