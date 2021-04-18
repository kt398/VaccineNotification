from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()



# Your Account SID from twilio.com/console
account_sid = os.getenv('TWILIO_SID')
# Your Auth Token from twilio.com/console
auth_token  = os.getenv('AUTH_TOKEN')

client = Client(account_sid, auth_token)

message = client.messages.create(
    to="9086440211", 
    from_="7043502751",
    body="Hi\n-Anonymous")

print(message.sid)