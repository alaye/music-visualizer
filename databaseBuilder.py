import dataset
import json
import gc
import os

jsonDir = "/home/jr/share/python/music-visualizer/merged"

db = dataset.connect('sqlite:///test.db')
table = db['Songs']

for root, subFolders, files in os.walk(jsonDir):
    for f in files:
        print("file:{}".format(f))
        gc.collect()
        tmpJson = json.load(open(os.path.join(root, f)))
        for Artist in tmpJson:
            for song in tmpJson[Artist]["Songs"]:
                table.insert(song)
import urllib2
import json
import re
#in_artist
def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

nodes = []
edges = []

anchor = "Rihanna"

q = [anchor]

while len(q) > 0:
    art = q.pop(0)
    #get song list
    url = "http://10.104.246.185:5000/artist/"+art.replace(" ", "%20")
    response = urllib2.urlopen(url)
    dictionary = byteify(json.loads(response.read()))
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
print nodes
print edges
