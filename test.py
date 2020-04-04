"""from pymongo import MongoClient
def conn():
    # Create MONGO_SUPERUSER and MONGO_SUPERPASS global varaible in local environment for MongoDB

    connection = MongoClient(
        f"mongodb://localhost:27017/?authSource=admin&readPreference=primary&ssl=false",
        socketTimeoutMS=900000)
    return connection
client =conn()
db = client.Database.User_data
db.update_one({'_id': 665}, {'$push': {'count': {"$each":[1,2]}}},upsert=True)
db.update_one({'_id': 665}, {'$push': {'mera': "pqrs"}},upsert=True)
db.update_one({'_id': 665},{ '$set': {'done': 1}},upsert=True)
db.update_one({'_id':'shikharshoray'},{'$push':{'lis':{"$each":['pass','shikh','sho']}}},upsert=True)

p=db.find_one({'_id':'shikharshoray'})
print(p['lis'])
for i in p['lis']:
    print(i)
client.close()"""
from pymongo import MongoClient
import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import pymongo
"""def conn():
    # Create MONGO_SUPERUSER and MONGO_SUPERPASS global varaible in local environment for MongoDB
    connection = MongoClient(
        f"mongodb://localhost:27017/?authSource=admin&readPreference=primary&ssl=false",
        socketTimeoutMS=900000)
    return connection

password_provided = "password" # This is input in the form of a string
password = password_provided.encode() # Convert to type bytes
salt = b'salt_' # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
)
key = base64.urlsafe_b64encode(kdf.derive(password)) # Can only use kdf once

print(key)


message = "my deep dark secret".encode()
"""
"""f = Fernet(key)
encrypted = f.encrypt(message)
print(message)
print(encrypted)
encrypted=str(encrypted)
key=str(key)
client =conn()
db = client.Database.User_data
db.insert_one({key:encrypted})


ksalt=os.urandom(16)
print(ksalt,"ksalt")
"""


def keygen (i,j): 
    # Here i is the string for which key is being genrated(password)
    # j is the string using which key for i is generated(username)
    i=i.encode()
    salt=j.encode()
    kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(i)) # Can only use kdf once
    return key

f=Fernet(keygen('abcd','efg'))
message='abcdefghijkl'
print(type(f.encrypt(message.encode())))