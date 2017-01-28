#class Node:
#    def __init__ (self,artist):
#        self.edges = {}
#        self.artist = artist
#    
#    def get_artist(self):
#        return self.artist
#
#    def add_edge (self, artist):
#        self.edges[artist] = 
#
#    def has_edge (self, artist):
#        return self.edges.has_key(artist) 
        

#in_artist

nodes = []
edges = []

anchor = input_artist

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


