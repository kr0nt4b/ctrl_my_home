#!/usr/bin/python
import httplib, urllib
import paho.mqtt.client as mqtt #import the client1
from pushbullet import Pushbullet, PushError

def pushover1():
  conn = httplib.HTTPSConnection("api.pushover.net:443")
  conn.request("POST", "/1/messages.json",
    urllib.urlencode({
      "token": "an4pyg3vc4pmuh1m4drj2io49ah6dn",
      "user": "gov15r2ibcwnbfcpyfuu9ri5265iv5",
      "message": "hello world",
      "sound": "echo",
    }), { "Content-type": "application/x-www-form-urlencoded" })
  conn.getresponse()

def pushover2():
  conn = httplib.HTTPSConnection("api.pushover.net:443")
  conn.request("POST", "/1/messages.json",
    urllib.urlencode({
      "token": "an4pyg3vc4pmuh1m4drj2io49ah6dn",
      "user": "uMFofWC6mz5iY1o2KX7haqYFUfxpGo",
      "message": "hello world",
      "sound": "echo",
    }), { "Content-type": "application/x-www-form-urlencoded" })
  conn.getresponse()

def send_msg3():
  try:
      print("sending pushbullet message")
      pb2 = Pushbullet("o.KiGxRpe4437cUzgbmWNnXb21ezkGBJRQ")
      push2 = pb2.push_note("Deurbel gaat", "De deurbell gaat. Ga naar de deur")
      pb = Pushbullet("o.MIi478XapGdgK9fm58gEnLiCZykPRdHH")
      push = pb.push_note("Deurbel gaat", "De deurbell gaat. Ga naar de deur")
  except Exception as e:
      print(e)
    

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
    if message.topic == 'doorbell/in':
      send_msg3()


def mqtt_connect():
  broker_address = "127.0.0.1"
  client = mqtt.Client("P1")
  client.on_message=on_message
  client.connect(broker_address)
  client.subscribe("doorbell/in")
  return client

if __name__ == "__main__":
  client = mqtt_connect()
  client.loop_forever() 
