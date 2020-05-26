from flask import Flask, jsonify, request, session
import dbController

app = Flask(__name__)
app.config['SECRET_KEY'] = "TEST_KEY"

from server import *

if __name__ == "__main__":
    app.run()
    