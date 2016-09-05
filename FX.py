import Img
from random import randint
class FX(object):
    img=None
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def update(self,world):
        pass
class Snow(FX):
    img=Img.img4("SnowFX")
    def update(self,world):
        self.y+=2
        self.x+=randint(-1,1)
def snowgen(world):
    if randint(0,1):
        world.fx.append(Snow(randint(0,world.size[0]*64-24),-24))