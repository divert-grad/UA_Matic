import time
from twilio.rest import Client

account_sid = '' # FIND ACCOUNT SID FROM TWILIO DASHBOARD
auth_key = '' # FIND AUTH KEY FROM TWILIO DASHBOARD
toPhone = '+18005551234' # THIS IS THE PHONE NUMBER FOR THE UA LINE YOU HAVE TO CALL. HAS THE FOLLOWING FORMAT: +18005559999
fromPhone = '+12145551234' # THIS IS THE TWILIO NUMBER YOU OWN AND CAN BE FOUND UNDER THE 'Phone Numbers' SECTION ON TWILIO DASHBOARD

# In the myTwiml section below, you need to enter the 7 digit ID code in the first "<Play digits="#">" section BEFORE the # sign
# Next, you have to enter the first FOUR DIGITS that spell out your last name in the next "<Play digits="#">" section before the # sign
myTwiml = '<Response><Pause length="10"/><Play digits="#"></Play><Pause length="5"/><Play digits="#"></Play><Record transcribe="true"/></Response>'
myPhone = '+12145550000' # THIS IS YOUR CELL PHONE NUMBER THAT THE RESULTS WILL BE TEXTED TO

client = Client(account_sid, auth_key)

myCall = client.calls.create(
    twiml = myTwiml,
    to = toPhone,
    from_ = fromPhone
)

print(myCall.sid)

counter = 0
while counter <= 30:
    myCall = myCall.fetch()
    print(myCall.status)
    time.sleep(1)
    counter = counter + 1

time.sleep(30)

myRecs = myCall.recordings.list()[0]
myRecSID = myRecs.sid

myTrans = client.transcriptions.list()[0]
myMessage = ''
if myTrans.recording_sid == myRecSID:
    myMessage = myTrans.transcription_text
else:
    myMessage = 'There was a problem completing the call. CALL IN TO CHECK UA STATUS'

outMessage = client.messages.create(
    body = myMessage,
    to = myPhone,
    from_ = fromPhone
)
