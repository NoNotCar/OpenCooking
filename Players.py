from Img import img4, colswap, sndget, new_man, xn
from BaseClasses import Object
import Direction as D
import Objects
pick=sndget("pickup")
class Player(Object):
    d=2
    updates = True
    name = "Player"
    o3d = 3
    placeable = False
    task=None
    inv=None
    himg=None
    def __init__(self, x, y, col, mt, c):
        self.place(x, y)
        self.imgs=new_man(mt,col)
        self.c=c
        self.col=col
    def update(self, world, events):
        bpress = self.c.get_buttons(events)
        sinv=self.inv
        soverride=False
        if not self.moving and not self.task:
            bpressc = self.c.get_pressed()
            o = world.get_o(*D.offset(self.d, self))
            for d in self.c.get_dirs():
                self.d=D.index(d)
                if not bpressc[1] and self.move(d[0], d[1], world):
                    break
            if bpress[0]:
                if o and o.placeable and not o.locked:
                    if self.inv and not o.contents:
                        if o.can_place(self.inv):
                            o.contents=self.inv
                            self.inv=None
                            soverride=o.on_place(world)
                    elif not self.inv and o.contents:
                        self.inv = o.contents
                        o.contents = None
                        o.on_take(world)
                    elif self.inv and o.contents:
                        if self.inv.is_supply:
                            if o.contents.combine(self.inv.supply()):
                                pick.play()
                        else:
                            if o.contents.combine(self.inv):
                                self.inv=None
            if bpress[1]:
                if o and not o.locked:
                    o.interact(world,self)
            if sinv is not self.inv and not soverride:
                pick.play()
            if sinv is not self.inv:
                self.re_himg()
        elif self.task:
            self.task.tupdate(self)
    def get_img(self,world):
        return self.imgs[self.d]
    def re_himg(self):
        if self.inv:
            self.himg=xn(self.inv.get_img(),0.5)
        else:
            self.himg=None