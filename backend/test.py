import requests
import pymongo,os
from dotenv import load_dotenv

from flask import Flask, request
app = Flask(__name__)
load_dotenv()
client = str(os.getenv('MONGO_CLIENT'))
myclient = pymongo.MongoClient(client)
mydb=myclient['myDatabase']
myCol=mydb['PhoneNum']
def get_available():
     response = requests.get("https://www.cvs.com/immunizations/covid-19-vaccine/immunizations/covid-19-vaccine.vaccine-status.NJ.json?vaccineinfo")
     x = response.json()

     available = list()
     for city in x['responsePayloadData']['data']['NJ']:
          if city['status'] == 'Available':
               available.append(city['city'])

     print(available)

@app.route('/newnumber', methods=['POST'])
def add_number():
     phone = request.get_json()['phone']
     cities = request.get_json()['cities']
     print(phone)
     print(cities)
     myDict={'_id':phone,"cities":cities}
     x=myCol.update_one({'_id':myDict['_id']},{'$set':myDict},upsert=True)
     print(x)
     return 'OK'

if __name__ == "__main__":
     print('test')
     app.run()

# class User:
#      def __init__(self,number,cities):
#           self.cities = []=cities
#           self.number=number
#      def getMatchingCities(availApptCities):
#           output=list[]
#           for appt in availApptCities:
#                for c in cities:
#                     if c==appt:
#                          output.append(c)
#                          break
#           return output