from Img import img4
class Tile(object):
    img=None
    ppassable=True
    slippery=False
    no_spawn=False
    def get_img(self):
        return self.img
class Floor(Tile):
    def __init__(self,imgname):
        self.img=img4(imgname)
class NS_Floor(Floor):
    no_spawn = True
class Pit(Tile):
    img=img4("Void")
    ppassable = False
    no_spawn = True
tiles=[Floor("Floor"),NS_Floor("NoSpawnFloor"),Pit()]