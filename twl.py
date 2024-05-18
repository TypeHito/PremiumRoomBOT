from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = "ACa1f3a9a70f5c1edd1e94c4f37dab4824"
auth_token = "f543c3deae238382261ed23700808a92"
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="TEST TEXT FROM ALGO SIGNAL CHANNEL time 20:22",
                     from_='+17576563033',
                     to='+998993265548'
                 )

print(message.sid)