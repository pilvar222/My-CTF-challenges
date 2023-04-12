import ipaddress
import dns.resolver
import re
from urllib.parse import urlparse
from flask import Flask, request, render_template
import ipaddress
import requests
import time

app = Flask(__name__)

def is_valid_ip(ip_string):
   try:
       ip_object = ipaddress.ip_address(ip_string)
       return True
   except ValueError:
       return False

def is_valid_url(url):
  try:
    result = urlparse(url)
    return True
  except ValueError:
    return False

def validate_website(website):
  if website is None:
    return "Please specify a website"
  if not is_valid_url(website):
    return "Please specify a valid website"
  domain = urlparse(website).hostname
  ip = dns.resolver.query(domain, 'A')[0].to_text()
  if not is_valid_ip(ip):
    return "Couldn't resolve IP address"
  if ipaddress.ip_address(ip).is_private:
    return "Nice try kiddo, but we're protected against SSRFs"
  if "flag" in urlparse(website).path:
    return "For security reasons, you can not access a website containing 'flag'"
  return "ok"

@app.route('/')
def mainpage():
  website = request.args.get('website')
  validation = validate_website(website)
  if validation != "ok":
    return validation
  else:
    time.sleep(3) # rate limiting
    return requests.get(website, allow_redirects=False).content

@app.route('/flag')
def flag():
  ip = request.remote_addr
  if ip == "127.0.0.1":
    return "web{FAKE_FLAG}"
  else:
    return "This is an internal endpoint"

if __name__ == "__main__":
  app.run(port=9003, host="0.0.0.0")