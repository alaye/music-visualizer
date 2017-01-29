import re
import json
import os
import gc
freeDbDir = "/home/think/Code/music-visualizer/data"
#freeDbDir = "/home/jr/share/python/music-visualizer/freeDB"

class Song:
    def __init__(self,Title,Artist,Album,Number,Genre,Year,DISCID):
        self.Title = Title
        self.Artist = Artist
        self.Album = Album
        self.Number = Number
        self.Genre = Genre
        self.Year = Year
        self.DiscId = DISCID

    def __str__(self):
     return "Artist:{}, Title:{}, Album:{}, Number:{}, Genre:{}, Year:{}".format(
     self.Artist,self.Title,self.Album,self.Number,self.Genre,self.Year)

    # def toJSON(self):
    #     return json.dumps(self, default=lambda o: o.__dict__,
    #         sort_keys=True, indent=4)


def parseFile(freeDbFile):
    info = {}
    info['AlbumSongs'] = []
    isVarious = False
    lineRe = re.compile('(.*)=(.*)')
    albumTitleRegex = re.compile ('(.*) \/ (.*)')
    trackNumberRegex = re.compile('TTITLE(\d+)')
    for line in open(freeDbFile):
        if line.startswith("#"):
            continue
        match = lineRe.match(line)
        if not match:
            continue
        key = match.group(1)
        value = match.group(2)
        if key == "DTITLE":
            match = albumTitleRegex.match(value)
            if not match:
                continue
            info['AlbumArtist'] = match.group(1)
            if info['AlbumArtist'] == "Various":
                isVarious = True
            info['AlbumTitle'] = match.group(2)
        elif key == "DYEAR":
            info['AlbumYear'] = value
        elif key == "DGENRE":
            info['AlbumGenre'] = value
        elif key.startswith("TTITLE"):
            match = trackNumberRegex.match(key)
            if not match:
                continue
            number = match.group(1)
            songTitle = value
            Artist = None
            if 'AlbumArtist' in info:
                if not isVarious:
                    Artist = info['AlbumArtist']
                else:
                    #When its a various artist album, song titles are in the same format
                    #as album names '<artist> / <song title>'
                    match = albumTitleRegex.match(value)
                    if not match:
                        continue
                    Artist = match.group(1)
                    songTitle = match.group(2)
            albumTitle = None
            if 'AlbumTitle' in info:
                albumTitle = info['AlbumTitle']

            genre = None
            if 'AlbumGenre' in info:
                genre = info['AlbumGenre']

            year = None
            if 'AlbumYear' in info:
                year = info['AlbumYear']

            discId = None
            if 'DISCID' in info:
                discId = info['DISCID']

            # song = Song(songTitle,Artist,albumTitle,number,genre,year,discId)
            song = {}
            song['Title'] = songTitle
            song['Artist'] = Artist
            song['Album'] = albumTitle
            song['Number'] = number
            song['Genre'] = genre
            song['Year'] = year
            song['DiscId'] = discId

            info['AlbumSongs'].append(song)

        else:
            if value == '':
                value = None
            info[key] = value
    return info


def dumper(obj):
    try:
        return obj.toJSON()
    except:
        return obj.__dict__

i = 0
num = 0
# Albums = {}
for root, subFolders, files in os.walk(freeDbDir):
    Artists = {}
    gc.collect()
    print("in {}".format(root))
    for f in files:
        fullPath =os.path.join(root, f)
        #print("file:{}".format(fullPath))
        try:
            tmpInfo = parseFile(fullPath)
            for song in tmpInfo['AlbumSongs']:
                if song['Artist'] in Artists:
                    Artists[song['Artist']]["Songs"].append(song)
                    num+=1
                else:
                    Artists[song['Artist']] = {}
                    Artists[song['Artist']]["Songs"] = [song]
                    num+=1
        except UnicodeDecodeError:
            continue
        if num >1000000:
            tmp = json.dumps(Artists, default=dumper, indent=4)
            with open("json/Artists{}.json".format(i),'w') as json_file:
                json_file.write(tmp)
            i+=1
            num = 0
            Artists = {}
            gc.collect()

    tmp = json.dumps(Artists, default=dumper, indent=4)
    with open("json/Artists{}.json".format(i),'w') as json_file:
        json_file.write(tmp)
    i+=1

# print(str(Artists))

    #print "key:{}, val:{}".format(key,value)
    #print line



# tmp = json.dumps(info,default=lambda o: o.__dict__,indent = 4,ensure_ascii=False)
#print tmp
# with io.open('tmp.json', 'w', encoding='utf8') as json_file:
#     # data = json.dumps(unicode(tmp), ensure_ascii=False)
#     # unicode(data) auto-decodes data to unicode if str
#     json_file.write(unicode(tmp))
