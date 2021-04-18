import pymongo
myclient = pymongo.MongoClient("mongodb+srv://kt:vaccine!23@cluster0.apgud.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
print(myclient.list_database_names())
mydb=myclient['myDatabase']
myCol=mydb["PhoneNum"]
myDict={"Number":"9086440211"}
x=myCol.insert_one(myDict)
print(x)
