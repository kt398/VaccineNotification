from twilio.rest import Client

# Your Account SID from twilio.com/console
account_sid = "AC827fcb589763a18213957e3e4022e659"
# Your Auth Token from twilio.com/console
auth_token  = "edf4a626e6fcffba32ee8786fd2d2027"

client = Client(account_sid, auth_token)

message = client.messages.create(
    to="7327544486", 
    from_="7043502751",
    body="Hi\n-Anonymous")

print(message.sid)