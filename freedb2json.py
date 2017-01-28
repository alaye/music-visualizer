import re
import json
import os
freeDbDir = "/home/jr/share/python/music-visualizer/freeDB"

class Song:
    def __init__(self,Title,Artist,Album,Number,Genre,Year):
        self.Title = Title
        self.Artist = Artist
        self.Album = Album
        self.Number = Number
        self.Genre = Genre
        self.Year = Year

    def __str__(self):
     return "Artist:{}, Title:{}, Album:{}, Number:{}, Genre:{}, Year:{}".format(
     self.Artist,self.Title,self.Album,self.Number,self.Genre,self.Year)

    # def toJSON(self):
    #     return json.dumps(self, default=lambda o: o.__dict__,
    #         sort_keys=True, indent=4)

Artists = {}
# Albums = {}

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

            song = Song(songTitle,Artist,albumTitle,number,genre,year)
            info['AlbumSongs'].append(song)

        else:
            if value == '':
                value = None
            info[key] = value
    return info

for root, subFolders, files in os.walk(freeDbDir):
    for f in files:
        fullPath =os.path.join(root, f)
        # print("file:{}".format(fullPath)
        try:
            tmpInfo = parseFile(fullPath)
            for song in tmpInfo['AlbumSongs']:
                if song.Artist in Artists:
                    Artists[song.Artist]["Songs"].append(song)
                else:
                    Artists[song.Artist] = {}
                    Artists[song.Artist]["Songs"] = [song]
        except UnicodeDecodeError:
            pass



# print(str(Artists))

    #print "key:{}, val:{}".format(key,value)
    #print line

def dumper(obj):
    try:
        return obj.toJSON()
    except:
        return obj.__dict__
tmp = json.dumps(Artists, default=dumper, indent=4)
# tmp = json.dumps(info,default=lambda o: o.__dict__,indent = 4,ensure_ascii=False)
#print tmp
# with io.open('tmp.json', 'w', encoding='utf8') as json_file:
#     # data = json.dumps(unicode(tmp), ensure_ascii=False)
#     # unicode(data) auto-decodes data to unicode if str
#     json_file.write(unicode(tmp))
with open('Artists.json','w') as json_file:
    json_file.write(tmp)
