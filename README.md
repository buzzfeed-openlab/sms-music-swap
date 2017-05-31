# sms-music-swap
A simple sms bot for mediating music recs between strangers

## About
This is a flask app that handles text message exchanges with strangers. It uses Twilio to send/receive SMS.

In a nutshell, the app:
-  texts a prompt (currently the topic is music recs, but this can be adapted to fit other topics)
- stores responses
- texts randomly selected responses from strangers
- texts notifications when responses have been seen
- allows admins to moderate responses

#### Try it out by texting 1-415-851-7927
