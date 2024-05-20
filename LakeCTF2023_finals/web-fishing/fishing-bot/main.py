from rq import Queue
from redis import Redis
from flask import Flask, render_template, request
from bot import visit
import re

q = Queue(connection=Redis.from_url('redis://redis:6379'))

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/submit', methods=['POST'])
def visit_post():
  postId = request.form['postId']
  if (re.match('^[a-f0-9]{32}$', postId)):
    q.enqueue(visit, postId)
    return 'post ID added to the queue'
  else:
    return 'Invalid post ID'

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=4000)