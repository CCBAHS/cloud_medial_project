import pymongo


client = pymongo.MongoClient("mongodb+srv://bths:BThSProject1.0@testcluster.f7oii.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db = client.test

db.users.insert_one({'username':'bths','password':'BThSProject1.0'})