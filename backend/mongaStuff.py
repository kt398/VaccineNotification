import pymongo, os
from dotenv import load_dotenv

load_dotenv()

client = str(os.getenv('MONGO_CLIENT'))
myclient = pymongo.MongoClient(client)
print(myclient.list_database_names())
mydb=myclient['myDatabase']

# mydb.collection.create_index("PhoneNum",unique=True)

myCol=mydb['PhoneNum']
myDict={'_id':'9086440211',"test":456}

try:
     x=myCol.update_one({'_id':myDict['_id']},{'$set':myDict},upsert=True)
     # print(x)
except pymongo.errors.DuplicateKeyError:
     print('Duplicate Key Error')
     #update city list
