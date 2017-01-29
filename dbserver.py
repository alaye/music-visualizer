from flask import Flask
from flask import json, jsonify
import re
import os
import urllib
app = Flask(__name__)

jdata = json.load(open("merged2/Artists1.json"))

@app.route('/')
def hello_world():
    return "Watch out for your nuke codes :^)"

@app.route('/artist/<author>')
def get_file(author):
    real = urllib.unquote(author)
    print real
    return jsonify(jdata[author])

if __name__ == '__main__':
    app.run(host='0.0.0.0')
