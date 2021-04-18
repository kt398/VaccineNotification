import requests
import pymongo, os
from dotenv import load_dotenv
#from twilio import twiml
from twilio.twiml.messaging_response import MessagingResponse

from flask import Flask, request
app = Flask(__name__)
load_dotenv()
client = str(os.getenv('MONGO_CLIENT'))
myclient = pymongo.MongoClient(client)
mydb=myclient['myDatabase']
myCol=mydb['PhoneNum']
city_list = []
def get_available():
     response = requests.get("https://www.cvs.com/immunizations/covid-19-vaccine/immunizations/covid-19-vaccine.vaccine-status.NJ.json?vaccineinfo")
     x = response.json()

     available = list()
     for city in x['responsePayloadData']['data']['NJ']:
          if city['status'] == 'Available':
               available.append(city['city'])
          city_list.append(city['city'])

     print(available)
@app.route('/sms', methods=['GET', 'POST'])
def response():
     number = request.form['From'][2:]
     message_body = request.form['Body'].upper().strip()
     resp = MessagingResponse()
     print(number, message_body)

     if message_body == 'STOP':
          print('STOP')
     elif message_body == 'START':
          pass
     else:
          if message_body in city_list:
               
               cities_to_track = myCol.find({'_id':number})[0]
               print(cities_to_track)
               track_list = cities_to_track['cities']
               if message_body not in track_list:
                    track_list.append(message_body)
                    myCol.update_one({'_id':number},{'$set':{'_id':number,'cities':track_list}},upsert=True)
                    resp.message(f'Successfully signed up to receive updates for vaccine appointments in {message_body}.')
               
               else:
                    resp.message(f'Already signed up for updates in {message_body}.')
               

          else:
               resp.message('This city does not exist or has no vaccines.')
    

     # Add a message
     
     return str(resp)


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
     get_available()
     print(city_list)
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