import pymongo, os
from dotenv import load_dotenv

load_dotenv()

client = str(os.getenv('MONGO_CLIENT'))
myclient = pymongo.MongoClient(client)
print(myclient.list_database_names())
mydb=myclient['myDatabase']
myCol=mydb['PhoneNum']
myDict={'Number':'9086440211'}
x=myCol.insert_one(myDict)
print(x)
