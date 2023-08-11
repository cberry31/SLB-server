import logging
from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.WARNING)
app.logger.addHandler(stream_handler)
CORS(app)


@app.route('/')
def hello_world():
    return 'Hello, World!'
