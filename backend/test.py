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
     elif message_body == 'STOP':
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
     
     cities_formatted = ', '.join(cities)

     try:
          res = myCol.find({'_id':phone})[0]
          track_list = res['cities']
     except pymongo.errors.InvalidOperation:
          message = client.messages.create(
               to=phone, 
               from_='7043502751',
               body = 'Thank you for subscribing to RU Vaxxed, standard message and data rates may apply.'
          )
     else:
          for city in cities:
               track_list.append(city)
          cities = track_list
     
     
     myDict={'_id':phone,'cities':cities,'sendList':True}
     x=myCol.update_one({'_id':myDict['_id']},{'$set':myDict},upsert=True)

     client.messages.create(
          to=phone,
          from_='7043502751',
          body = f'You have successfully subscribed to notifications for {cities_formatted}'
     )
     print(x)
     return 'OK'

def send(phone_num,locations):
     converted=my_string = ','.join(locations)
     message = client.messages.create(
          to=phone_num, 
          from_='7043502751',
          body = f'There are vaccination appointments available in {converted}. Click the link to sign up:\nhttps://www.cvs.com/vaccine/intake/store/covid-screener/covid-qns'
     )
     message = client.messages.create(
          to=phone_num, 
          from_='7043502751',
          body = 'If you would like to continue recieving messages, please type CONTINUE'
     )
     # print(message.sid)

def send_texts():
     available=get_available()
     if(len(available)==0):
          return
     for crt_num in myCol.find():
          locations=list()
          if crt_num['sendList']==True:
               for userLoc in crt_num['cities']:
                    if userLoc in available:
                         locations.append(userLoc)
               if(len(locations)!=0):
                    send(crt_num['_id'],locations)
                    crt_num['sendList']=False
                    myCol.update_one({'_id':crt_num['_id']},{'$set':crt_num},upsert=True)

if __name__ == "__main__":
     scheduler = BackgroundScheduler()
     send_texts()
     scheduler.add_job(func=send_texts, trigger="interval", minutes=1)
     scheduler.start()
     atexit.register(lambda: scheduler.shutdown())
     app.run()
