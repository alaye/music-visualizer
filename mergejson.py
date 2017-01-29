import json
import os
import gc
#jsonDir = "/home/think/Code/music-visualizer/json"
jsonDir = "/home/jr/share/python/music-visualizer/json"

def mergeFile(json1,json2):
    for key in json2:
        if key in json1:
            #same Artist
            json1[key]["Songs"]+= json2[key]["Songs"]
        else:
            json1[key] = json2[key]
    return json1

def dumper(obj):
    try:
        return obj.toJSON()
    except:
        return obj.__dict__

tmp = []
i = 0
for root, subFolders, files in os.walk(jsonDir):
    for f in files:
        gc.collect()
        tmpJson = json.load(open(os.path.join(root, f)))
        if len(tmp) < 1:
            tmp.append(tmpJson)
        else:
            merged = mergeFile(tmp.pop(),tmpJson)
            with open("merged/Artists{}.json".format(i),'w') as json_file:
                tmpFile = json.dumps(merged, default=dumper, indent=4)
                json_file.write(tmpFile)
                i+=1

if len(tmp) >0:
    tmpJson = tmp.pop()
    with open("merged/Artists{}.json".format(i),'w') as json_file:
        tmpFile = json.dumps(tmpJson, default=dumper, indent=4)
        json_file.write(tmpFile)
        i+=1
