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

@app.route('/relations/', methods=['POST'])
def relations():
    artist=request.form['artist']
    nodes = []
    edges = []

    anchor = artist

    q = [anchor]
    art = None

    while len(q) > 0:
        art = q.pop(0)
        #get song list
        for song in songlist:
            #get string of featured artists
            m = re.match('feat. ([^)]+)')
            if m:
                s = m.group()
                #split into artists
                lst = s.split(",")
                if len(lst) > 1:
                    lstend = (lst.pop()).split("&")
                    lst = lst.extend(lstend)
                for a in lst:
                    a = a.strip()
                    edges.append((art,a))
                    if nodes.count(a) == 0:
                        q.append(a)
                    for b in lst:
                        if a != b:
                            edges.append((a,b))

        nodes.append(art)

    i = 0
    j = 0
    while i < len(edges):
        j = i+1
        t1 = edges[i]
        while j < len(edges):
            t2 = edges[j]
            if t1[1] == t2[1] and t1[2] == t2[2]:
                edges.remove(t2)
            elif t1[2] == t2[1] and t1[1] == t2[1]:
                edges
            else:
                j = j + 1
        i = i + 1
    

if __name__ == '__main__':
    app.run(host='0.0.0.0')
