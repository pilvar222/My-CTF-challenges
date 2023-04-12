from flask import Flask, request
import base64
import math
import time

app = Flask(__name__)

@app.route('/')
def mainpage():
  token = request.headers.get('X-Secret-Token')
  if token == None:
    return "Error: Missing X-Secret-Token"
  try:
    token = base64.b64decode(token)
  except:
    return "Error: Invalid base64"
  try:
    token = token.decode('utf-8')
  except:
    return "Error: Invalid utf-8"
  if not token.isnumeric():
    return "Error: The decoded token is not a number"
  secret = math.floor(time.time())
  if int(token) < secret:
    return "Error: The decoded token is too small, make sure your computer's clock is correct"
  elif int(token) > secret:
    return "Error: The decoded token is too big, make sure your computer's clock is correct"
  elif int(token) == secret:
    return "Congratz, you accessed the very secure admin panel! web{I already saw things more stupid than this in real life}"
  else:
    return "I don't know how you got here, but you shouldn't be here"

if __name__ == "__main__":
  app.run(port=9001, host="0.0.0.0")
