from Img import img4, blank64
class Tile(object):
    img=None
    ppassable=True
    passable=True
    slippery=False
    no_spawn=False
    backwall=img4("Tiles/BackWall")
    def get_img(self):
        return self.img
class Floor(Tile):
    def __init__(self,imgname,backwall=None):
        self.img=img4("Tiles/"+imgname)
        if backwall:
            self.backwall=img4("Tiles/"+backwall)
class NS_Floor(Floor):
    no_spawn = True
class Pit(Tile):
    img=img4("Tiles/Void")
    ppassable = False
    no_spawn = True
class Wasser(Tile):
    img = img4("Tiles/Wasser")
    passable = False
    no_spawn = True
    backwall = blank64
class OutdoorFloor(Floor):
    backwall = blank64
tiles=[Floor("Floor"),NS_Floor("NoSpawnFloor"),Pit(),Floor("HauntedFloor","HauntedBackWall"),Wasser(),OutdoorFloor("Grass"),OutdoorFloor("Sand")]