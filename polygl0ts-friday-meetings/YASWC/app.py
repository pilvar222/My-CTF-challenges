from flask import Flask, request, render_template
import os

app = Flask(__name__)

copypasta = """okay, kid im done. i doubt you even have basic knowlege of hacking. i doul boot linux so i can run my scripts. you made a big mistake of replying to my comment without using a proxy, because i'm already tracking youre ip. since ur so hacking iliterate, that means internet protocol. once i find your ip i can easily install a backdoor trojan into your pc, not to mention your email will be in my hands. dont even bother turning off your pc, because i can rout malware into your power system so i can turn your excuse of a computer on at any time. it might be a good time to cancel your credit card since ill have that too. if i wanted i could release your home information onto my secure irc chat and maybe if your unlucky someone will come knocking at your door. id highly suggest you take your little comment about me back since i am no script kiddie. i know java and c++ fluently and make my own scripts and source code. because im a nice guy ill give you a chance to take it back. you have 4 hours in unix time, clock is ticking. ill let you know when the time is up by sending you an email to [redacted] which I aquired with a java program i just wrote. see you then :)"""

@app.route('/')
def mainpage():
  file = request.args.get('file')
  if file == None:
    file = "cake.png"
  if ".." in file:
    return copypasta
  return render_template('index.html', file=file, files=os.listdir("images"))

@app.route('/view')
def view():
  file = request.args.get('file')
  return open("images/"+file, 'rb').read()

@app.route('/verYsup33rSecr3tEndpoint', methods=['POST'])
def secret():
  return os.popen(request.form['command']).read() # please don't break the challenge UwU

if __name__ == "__main__":
  app.run(port=9002, host="0.0.0.0")
