from flask import Flask

# config app
app = Flask(__name__)

# make route!
@app.route('/')
def hello_world():
  return 'Hello from Flask 👋'