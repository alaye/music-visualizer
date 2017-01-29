from flask import Flask
from flask import json, jsonify
import re
import os
import urllib
from pymongo import MongoClient
app = Flask(__name__)

client = MongoClient('mongodb://admin:admin123@localhost:27017/')
db = client.test

@app.route('/')
def hello_world():
    return "Watch out for your nuke codes :^)"

@app.route('/artist/<author>')
def get_file(author):
    real = urllib.unquote(author)
    print real
    res = db.songs.find({"Artist": author})
    fin = []
    for my_dict in res:
        tmp_dict = {}
        del my_dict[u'_id']
        for key in my_dict:
            newkey = key.encode('ascii', errors="backslashreplace")
            newval = my_dict[key].encode('ascii', errors=
                    "backslashreplace")
            tmp_dict[newkey] = newval
        fin.append(tmp_dict)
    return jsonify({"Songs": fin})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
