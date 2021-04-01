import json
from pymongo import MongoClient
MONGO_URI = "mongodb://catalog:123456@127.0.0.1:27017,127.0.0.1:27018,127.0.0.1:27019,127.0.0.1:27020/?replicaSet=rs0"
client = MongoClient(MONGO_URI)
db = client['english_db']
collection_currency = db['english_in_levels']

with open('data/newsData.json') as f:
    file_data = json.load(f)

# if pymongo < 3.0, use insert()
# collection_currency.insert(file_data)
# # if pymongo >= 3.0 use insert_one() for inserting one document
# collection_currency.insert_one(file_data)
# if pymongo >= 3.0 use insert_many() for inserting many documents
collection_currency.insert_many(file_data["news"])

client.close()