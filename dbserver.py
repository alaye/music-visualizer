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

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

@app.route('/relations/', methods=['POST'])
def relations():
    anchor=request.form['artist']
    nodes = []
    edges = []

    q = [anchor]

    while len(q) > 0:
        art = q.pop(0)
        #get song list
        dictionary = get_file(art)
        #dictionary = byteify(json.loads(response.read()))
        songlist = []
        if (dictionary):
            lst = dictionary["Songs"]
            for song in lst:
                songlist.append(song["Title"])
            for song in songlist:
                #get string of featured artists
                m = re.match('.+[fF]eat. ([^)(/]+)', song) 
                if m:
                    s = m.group(1)
                    #split into artists
                    lst = s.split(",")
                    lstend = (lst.pop()).split("&")
                    lst.extend(lstend)
                    for a in lst:
                        a = a.strip()
                        edges.append((art.strip(),a))
                        if nodes.count(a) == 0:
                            q.append(a)
                        for b in lst:
                            b = b.strip()
                            if a != b:
                                edges.append((a,b))

        if nodes.count(art) == 0:
            nodes.append(art.strip())

    i = 0
    j = 0
    while i < len(edges)-1:
        j = i+1
        t1 = edges[i]
        while j < len(edges):
            t2 = edges[j]
            if t1[0] == t2[0] and t1[1] == t2[1]:
                edges.pop(j)
            elif t1[1] == t2[0] and t1[0] == t2[1]:
                edges.pop(j)
            elif t2[0] == t2[1]:
                edges.pop(j)
            else:
                j = j + 1        
        i = i + 1
    
    adj_hash = {}
    for n in nodes:
        elst = []
        for e in edges:
            if n == e[0]:
                elist.append(e[1])
            elif n == e[1]:
                elist.append(e[0])
        adj_hash[n] = elst

                

    

if __name__ == '__main__':
    app.run(host='0.0.0.0')
