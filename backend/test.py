import requests
from flask import Flask, request
app = Flask(__name__)

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
    phone = request.form['number']

if __name__ == "__main__":
     print('test')
     app.run()

