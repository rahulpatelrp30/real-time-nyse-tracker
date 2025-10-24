from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017")
col = client["nyse_tracker"]["most_active"]

print("Total docs:", col.count_documents({}))
for doc in col.find().sort("timestamp", -1).limit(5):
    print({k: doc.get(k) for k in ["Symbol","Name","Price","Change","Volume","timestamp"]})
