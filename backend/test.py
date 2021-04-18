import requests
import pymongo, os
from dotenv import load_dotenv
#from twilio import twiml
from twilio.twiml.messaging_response import MessagingResponse

import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request
from twilio.rest import Client
app = Flask(__name__)
load_dotenv()
client = str(os.getenv('MONGO_CLIENT'))
myclient = pymongo.MongoClient(client)
mydb=myclient['myDatabase']
myCol=mydb['PhoneNum']
city_list = []
prevTime=''
account_sid = os.getenv('TWILIO_SID')
auth_token  = os.getenv('AUTH_TOKEN')
client = Client(account_sid, auth_token)

def get_available():
     global prevTime
     response = requests.get("https://www.cvs.com/immunizations/covid-19-vaccine/immunizations/covid-19-vaccine.vaccine-status.NJ.json?vaccineinfo")
     x = response.json()
     available = list()
     if prevTime==x['responsePayloadData']['currentTime']:
          print("Not updated")
          return available
     prevTime=x['responsePayloadData']['currentTime']
     for city in x['responsePayloadData']['data']['NJ']:
          if city['status'] == 'Available':
               available.append(city['city'])
          city_list.append(city['city'])

     print(available)
     return available

@app.route('/sms', methods=['GET', 'POST'])
def response():
     number = request.form['From'][2:]
     message_body = request.form['Body'].upper().strip()
     resp = MessagingResponse()
     print(number, message_body)

     if message_body == 'CONTINUE':
          print("working")
          number= myCol.find({'_id':number})[0]
          number['sendList']=True
          myCol.update_one({'_id':number['_id']},{'$set':number},upsert=True)
     if message_body == 'STOP':
          print('STOP')
          myCol.remove({'_id':number})
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
     myDict={'_id':phone,'cities':cities,'sendList':True}
     x=myCol.update_one({'_id':myDict['_id']},{'$set':myDict},upsert=True)
     print(x)
     return 'OK'

def send(phoneNum,locations):
     converted=my_string = ','.join(locations)
     message = client.messages.create(
          to='9086440211', 
          from_="7043502751",
          body = 'There are vaccination appointments available in {}. Click the link to sign up:\nhttps://www.cvs.com/vaccine/intake/store/covid-screener/covid-qns'.format(converted)
     )
     message = client.messages.create(
          to='9086440211', 
          from_="7043502751",
          body = 'If you would like to continue recieving messages, please type CONTINUE'
     )
     # print(message.sid)

def sendTexts():
     print("Running sendTexts")
     available=get_available()
     if(len(available)==0):
          return
     for crtNum in myCol.find():
          print("Printing current number")
          print(crtNum)
          locations=list()
          if crtNum['sendList']==True:
               for userLoc in crtNum['cities']:
                    if userLoc in available:
                         locations.append(userLoc)
               if(len(locations)!=0):
                    send(crtNum,locations)
                    crtNum['sendList']=False
                    myCol.update_one({'_id':crtNum['_id']},{'$set':crtNum},upsert=True)

if __name__ == "__main__":
     print('test')
     scheduler = BackgroundScheduler()
     sendTexts()
     scheduler.add_job(func=sendTexts, trigger="interval", minutes=1)
     scheduler.start()
     atexit.register(lambda: scheduler.shutdown())
     app.run()
