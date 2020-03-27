import pymongo

my_client=pymongo.MongoClient("mongodb://localhost:27017/")
mydb=my_client["Database"]

mycol=mydb["customers"]

my_dict={"name":"James Bond","address":"Gzb"} 

x=mycol.insert_one(my_dict)

print(x.inserted_id)