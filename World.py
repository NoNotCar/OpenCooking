import Tiles
import pygame
import Img
import Levels
import pickle
from random import randint
cashfont=Img.fload("cool",32)
bcfont=Img.fload("cool",64)
backwall=Img.img4("BackWall")
fail=Img.sndget("fail")
button=Img.sndget("button")
class World(object):
    reordertime=1200
    cash=0
    washing=False
    button=False
    anitick=0
    def __init__(self,ps,n):
        self.ps=ps
        self.uos=[]
        self.ucs=[]
        self.level=(n-1)%10+1
        self.world=(n-1)//10+1
        manualspawn=False
        self.load("%s-%s"%(str((n-1)//10+1),str((n-1)%10+1)))
        for r in self.w:
            for obj in r:
                if obj and obj.updates:
                    self.uos.append(obj)
                elif obj and obj.name=="Sink":
                    self.washing=True
                elif obj and obj.name=="Spawn":
                    try:
                        ps[obj.d].place(obj.x,obj.y)
                        self.dest(obj)
                        self.spawn(ps[obj.d])
                    except IndexError:
                        self.dest(obj)
                    manualspawn=True
                if obj and obj.ticks and obj.__class__ not in self.ucs:
                    self.ucs.append(obj.__class__)
        self.size=len(self.w),len(self.w[0])
        if not manualspawn:
            for n,p in enumerate(ps):
                self.spawn_p(p)
        self.orders=[Levels.new_order(self.level,self.world)]
        self.tonextorder=1200
        self.returned=[]
    def update(self,events):
        self.anitick+=1
        self.anitick%=60
        for uc in self.ucs:
            uc.tick()
        for o in self.uos[:]:
            o.update(self,events)
        for r in self.w:
            for o in r:
                if o and o.moving:
                    o.mupdate(self)
        for o in self.orders[:]:
            o.time-=1
            if o.time==0:
                self.orders.remove(o)
                self.cash-=5
                self.reordertime+=60
                fail.play()
                if len(self.orders)==0:
                    self.orders.append(Levels.new_order(self.level,self.world))
                    self.tonextorder = self.reordertime + self.orders[-1].time - 1800
        self.tonextorder-=1
        if self.tonextorder==0:
            self.orders.append(Levels.new_order(self.level,self.world))
            self.tonextorder = self.reordertime + self.orders[-1].time - 1800
        for r in self.returned:
            if r[1]:
                r[1]-=1
    def load(self,file):
        with open(Img.loc + "saves/%s.lvl" % file, "rb") as sf:
            savobj = pickle.load(sf)
            self.t = savobj.t
            self.w = savobj.w
            self.size = len(self.w), len(self.w[0])
    def render(self,screen):
        for x in range(self.size[0]):
            screen.blit(backwall,(x*64,0))
            for y in range(self.size[1]):
                screen.blit(self.get_t(x,y).img,(x*64,y*64+64))
        crenders=[]
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                o=self.get_o(x,y)
                if o:
                    if o in self.ps and o.himg and not o.d:
                        screen.blit(o.himg, (x * 64 + o.xoff + 16, y * 64 + o.yoff + 64 - o.o3d * 4 + 24))
                    screen.blit(o.get_img(self),(x*64+o.xoff,y*64+o.yoff+64-o.o3d*4))
                    if o.contents and not o.contents_render_order_override:
                        crenders.append(o)
                    elif o.contents:
                        screen.blit(o.contents.get_img(),(x*64+o.xoff+o.fx,y*64+o.yoff+64-o.o3d*4+o.fy-o.contents.o3d*4))
                    if o in self.ps and o.himg and o.d:
                        screen.blit(o.himg,(x*64+o.xoff+16+(16*(2-o.d)),y*64+o.yoff+64-o.o3d*4+24))
        for o in crenders:
            screen.blit(o.contents.get_img(),(o.x * 64 + o.xoff + o.fx, o.y * 64 + o.yoff + 64 - o.o3d * 4 + o.fy - o.contents.o3d * 4))
            if o.progress is not None:
                screen.blit(
                    (Img.progresses, Img.wprogresses)[o.warn][0 if o.warn and self.anitick // 15 % 2 else o.progress],
                    (o.x * 64 + o.xoff, o.y * 64 + o.yoff + 40 - o.o3d * 4))
    def get_t(self,x,y):
        return Tiles.tiles[self.t[x][y]]
    def get_o(self,x,y):
        if self.in_world(x,y):
            return self.w[x][y]
        return None
    def in_world(self,x,y):
        return 0<=x<self.size[0] and 0<=y<self.size[1]
    def is_clear(self,x,y,p=False):
        return self.in_world(x,y) and not self.w[x][y] and not (p and not self.get_t(x,y).ppassable)
    def spawn(self,o):
        self.w[o.x][o.y]=o
        if o.updates:
            self.uos.append(o)
    def spawn_p(self,p):
        while True:
            rx=randint(0,self.size[0]-1)
            ry = randint(0, self.size[1] - 1)
            if self.is_clear(rx,ry) and not self.get_t(rx,ry).no_spawn:
                p.place(rx,ry)
                break
        self.spawn(p)
    def dest(self,o):
        self.w[o.x][o.y] = None
        if o.updates:
            self.uos.remove(o)
    def move(self,o,tx,ty):
        self.dest(o)
        o.place(tx,ty)
        self.spawn(o)
    def change_t(self,x,y,t):
        self.t[x][y]=t
    def reg_updates(self,o):
        o.updates=True
        if o not in self.uos:
            self.uos.append(o)
    def del_updates(self,o):
        o.updates=False
        if o in self.uos:
            self.uos.remove(o)
    def remove_order(self,o):
        self.orders.remove(o)
        self.cash+=len(o.c)*5
        if not self.orders:
            self.orders.append(Levels.new_order(self.level,self.world))
            self.reordertime-=60
            self.tonextorder=self.reordertime+self.orders[-1].time-1800
    def p_button(self):
        self.button=not self.button
        button.play()
class SaveObject(object):
    def __init__(self,t,w):
        self.t=t
        self.w=w
class EditWorld(World):
    def __init__(self,size,load=None):
        self.size=size
        if load:
            self.load(load)
        else:
            self.w = [[None] * self.size[1] for _ in range(self.size[0])]
            self.t = [[0] * self.size[1] for _ in range(self.size[0])]
        self.ps=[]
        self.uos=[]
    def save(self):
        sav=SaveObject(self.t,self.w)
        sf=open(Img.loc+"saves/save.lvl","wb")
        pickle.dump(sav,sf)
        sf.close()

