from twilio.rest import TwilioRestClient
import os
client = TwilioRestClient(os.environ.get("TWILIO_ACCOUNT"), os.environ.get("TWILIO_AUTH_TOKEN"))

messages = client.sms.messages.list(to="+5145001100")
for message in messages:
    print message.body

for message in messages:
    print "%s: %s" % (message.from_, message.body)


for number in [m.from_ for m in messages]:
    call = client.calls.create(to=number, from_="+5145001100", url="http://twimlbin.com/external/88a838c11e1c2b04")


