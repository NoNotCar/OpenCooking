import Img
class Object(object):
    img=None
    speed=4
    xoff,yoff=(0,0)
    moving=False
    o3d=0
    name="Object"
    updates=False
    dx=0
    dy=0
    progress=0
    contents=None
    placeable=True
    progress=None
    locked=False
    warn=False
    fx=0
    fy=0
    contents_render_order_override=False
    def __init__(self,x,y):
        self.place(x,y)
    def place(self,x,y):
        self.x=x
        self.y=y
    def update(self,world,events):
        pass
    def get_img(self,world):
        return self.img
    def mupdate(self,world):
        if self.xoff>0:
            self.xoff-=self.speed
        elif self.xoff<0:
            self.xoff+=self.speed
        if self.yoff>0:
            self.yoff-=self.speed
        elif self.yoff<0:
            self.yoff+=self.speed
        if abs(self.xoff)<self.speed and abs(self.yoff)<self.speed:
            self.xoff=0
            self.yoff=0
            self.moving=False
    def move(self,dx,dy,world):
        tx=self.x+dx
        ty=self.y+dy
        if world.is_clear(tx,ty,self.name=="Player"):
            world.move(self,tx,ty)
            self.moving=True
            self.xoff= -dx*64
            self.yoff= -dy*64
            self.dx=dx
            self.dy=dy
            return True
        return False
    def interact(self,world,p):
        pass
    def on_place(self,world):
        pass
    def on_take(self,world):
        pass
    def can_place(self, item):
        return True
class Item(object):
    name="Item"
    choppable=False
    grateable=False
    contents=None
    is_supply=False
    utensil=True
    soupcolour=None
    scimg=None
    o3d=0
    state="normal"
    @classmethod
    def init(cls):
        cls.name = cls.__name__
        name=cls.__name__
        cls.img=Img.img4(name)
    def get_img(self):
        return self.img
    def combine(self, food):
        return False
    def maketag(self):
        return self.__class__.name
    def supply(self):
        return self
    def __eq__(self, other):
        try:
            return self.maketag()==other.maketag()
        except AttributeError:
            print "WARNING: comparing food to non-food!"
            return False

    def pcombine(self, food, plate):
        return self.combine(food)