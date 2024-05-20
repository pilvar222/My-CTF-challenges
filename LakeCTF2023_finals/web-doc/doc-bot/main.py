from rq import Queue
from redis import Redis
from flask import Flask, render_template, request
from bot import visit

q = Queue(connection=Redis.from_url('redis://redis:6379'))

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/submit', methods=['POST'])
def visit_url():
  url = request.form['url']
  if url.startswith('http'):
    q.enqueue(visit, url)
    return 'URL added to the queue'
  else:
    return 'Invalid URL'

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=4000)