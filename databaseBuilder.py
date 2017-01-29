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
