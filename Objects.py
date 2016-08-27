from BaseClasses import Object
from Img import img4, sndget, imgstrip4f, colcopy, imgstrip4, blank64, imgrot, new_man
import Food
import Direction as D
import pygame
from random import randint, choice
chop=sndget("chop")
hit=sndget("hit")
wash=sndget("wash")
money=sndget("money")
voids=[sndget("void"),sndget("voidimp")]
grate=sndget("grate")
pon=sndget("poweron")
poff=sndget("poweroff")
class Counter(Object):
    img=img4("Counter")
    o3d=4
    def __init__(self,x,y,contents=None):
        self.contents=contents
        self.place(x,y)
class FixedCounter(Counter):
    img=img4("FixedBlock")
    name="Fixed"
    fy=-4
class Wall(Object):
    img=img4("WallBottom")
    overimg=img4("WallTop")
    o3d = -12
    over3d=8
    placeable = False
class Tree(Object):
    overimg = img4("Tree")
    over3d = 12
    placeable = False
class Spawner(Object):
    img=img4("Spawner")
    o3d = 4
    placeable = True
    def __init__(self,x,y,food):
        self.contents=food
        self.foodspawn=food.__class__
        self.place(x,y)
    def on_take(self,world):
        self.contents=self.foodspawn()
class XBoard(Object):
    recipe=""
    o3d = 4
    mp = 0
    mpmax=5
    sound=None
    def interact(self, world, p):
        if self.contents and self.contents.can_change_state(self.recipe):
            p.task = self
            self.locked = True
            self.progress = 0
    def tupdate(self, p):
        self.mp += 1
        if self.mp == self.mpmax:
            self.mp = 0
            self.progress += 1
            if self.progress == 15:
                p.task = False
                self.locked = False
                self.contents.set_state(self.recipe)
                self.progress = None
            elif self.progress % 4 == 3:
                self.sound.play()
class ChoppingBoard(XBoard):
    img=img4("ChoppingBoard")
    recipe = "chopped"
    sound = chop
class Grater(XBoard):
    img=img4("Grater")
    recipe = "grated"
    sound = grate
    mpmax = 10
class HammerBoard(XBoard):
    img=img4("HittingBoard")
    recipe = "hammered"
    sound = hit
class Trash(Object):
    img=img4("Trash")
    o3d = 4
    def on_place(self,world):
        voids[self.contents.utensil].play()
        if self.contents.utensil:
            world.cash-=5
            world.returned.append([self.contents.__class__(),0])
        self.contents=None
        return True
class FoodExit(Object):
    img=img4("Exit")
    o3d = 4
    reverse = False
    def on_place(self,world):
        for o in world.orders:
            if o.plate==self.contents:
                self.fx=1
                self.locked=True
                self.order=o
                break
        else:
            self.fx=0
        world.reg_updates(self)
    def update(self,world,events):
        if self.fx:
            if self.reverse:
                self.fx-=1
                if not self.fx:
                    self.reverse=False
            else:
                self.fx+=1
                if self.fx==64:
                    if self.order in world.orders:
                        world.remove_order(self.order)
                        self.contents = None
                        world.del_updates(self)
                        money.play()
                        self.locked=False
                        plate=Food.Plate()
                        plate.dirty=world.washing
                        world.returned.append([plate,360])
                    else:
                        self.reverse=True
                        self.order=None
        elif self.contents:
            for o in world.orders:
                if o.plate == self.contents:
                    self.fx = 1
                    self.locked = True
                    self.order = o
            else:
                self.locked=False
        else:
            self.locked=False
            world.del_updates(self)
class Returner(Object):
    img=img4("Entrance")
    o3d = 4
    updates = True
    def update(self,world,events):
        if not self.contents:
            for r in world.returned:
                if not r[1]:
                    self.contents=r[0]
                    world.returned.remove(r)
                    self.fx=64
                    break
        elif self.fx:
            self.fx-=1
        elif self.locked:
            self.locked=False
class Sink(Object):
    img=img4("Sink")
    name="Sink"
    o3d=7
    fy=12
    mp=0
    mode="clean"
    def interact(self,world,p):
        if self.contents and self.contents.name=="Plate" and self.contents.dirty:
            p.task=self
            self.locked=True
            self.progress=0
            self.mode="clean"
        elif self.contents and self.contents.name == "Pot" and self.contents.contents.is_burnt:
            p.task = self
            self.locked = True
            self.progress = 0
            self.mode = "soupscrub"
        elif self.contents and self.contents.name == "Pan" and self.contents.burnt:
            p.task = self
            self.locked = True
            self.progress = 0
            self.mode = "panscrub"
    def tupdate(self,p):
        self.mp+=1
        if self.mp==8:
            self.mp=0
            self.progress+=1
            if self.progress==15:
                p.task=False
                self.locked=False
                if self.mode=="clean":
                    self.contents.dirty=False
                elif self.mode=="panscrub":
                    self.contents.burnt = False
                    self.contents.re_img()
                else:
                    self.contents.contents=None
                    self.contents.re_img()
                self.progress=None
            elif self.progress%4==3:
                wash.play()
class ArrowBlock(Object):
    imgs=imgstrip4f("ArrowBlock",16)
    img=imgs[0]
    dimgs=[colcopy(i,(0,255,255),(0,100,100)) for i in imgs]
    name="ArrowBlock"
    o3d=4
    updates = True
    eup=False
    def __init__(self,x,y,d=0):
        self.place(x,y)
        self.dir=D.get_dir(d)
        self.d=d
    def update(self,world,events):
        if not self.moving:
            dx,dy=self.dir if world.button else D.anti(self.dir)
            self.move(dx,dy,world)
    def get_img(self,world):
        return self.imgs[self.d] if world.button else self.dimgs[self.d]
class MultiArrowBlock(ArrowBlock):
    imgs=imgstrip4f("ArrowBlockAttached",16)
    img=imgs[0]
    dimgs=[colcopy(i,(0,255,255),(0,100,100)) for i in imgs]
    eup=False
    init=False
    def __init__(self,x,y,d=0):
        self.place(x,y)
        self.dir=D.get_dir(d)
        self.d=d
    def update(self,world,events):
        if not self.init:
            tx,ty=self.x,self.y
            self.blockchain=[]
            while True:
                tx,ty=D.offsetdxy(D.rotdir(self.dir,1),tx,ty)
                if not world.in_world(tx,ty):
                    break
                o=world.get_o(tx,ty)
                if not o or o.name=="Fixed":
                    break
                self.blockchain.append(o)
            self.init=True
        dx,dy=self.dir if world.button else D.anti(self.dir)
        if not self.moving and self.can_move(dx,dy,world):
            if all([o.can_move(dx,dy,world) for o in self.blockchain]):
                self.ex_move(dx,dy,world)
                for o in self.blockchain:
                    o.ex_move(dx,dy,world)
    def get_img(self,world):
        return self.imgs[self.d] if world.button else self.dimgs[self.d]
class Button(Counter):
    img=img4("Button")
    def interact(self,world,p):
        world.p_button()
class Flipper(Counter):
    imgs=imgstrip4f("Flipper",16)
    img=imgs[0]
    tick=1
    updates = True
    def update(self,world,events):
        self.tick+=1
        if self.tick==600:
            world.p_button()
            self.tick=1
        self.progress=self.tick*14//600
    def get_img(self,world):
        return self.imgs[world.button]
class Hob(Counter):
    img=img4("Cooker")
    def can_place(self, item):
        return item.name in ("Pot","Pan")
    def on_place(self,world):
        world.reg_updates(self)
    def update(self,world,events):
        if self.contents:
            self.contents.heat()
            if self.contents.contents:
                self.warn=self.contents.contents.warn
                self.progress=self.contents.contents.progress
            else:
                self.warn = False
                self.progress = None
    def on_take(self,world):
        world.del_updates(self)
        self.warn=False
        self.progress=None
class Grill(Hob):
    img=img4("GrillBase")
    oimgs=[img4("GrillTop"+s) for s in ["Off","On"]]
    on=False
    over3d = 8
    def can_place(self, item):
        return item.can_change_state("grilled")
    def on_place(self,world):
        world.reg_updates(self)
        self.on=True
    def update(self,world,events):
        if self.contents:
            self.contents.grill()
            self.warn=self.contents.warn
            self.progress=self.contents.progress
            if self.contents.burnprog==self.contents.burningtime:
                self.contents=None
    def on_take(self, world):
        world.del_updates(self)
        self.warn = False
        self.progress = None
        self.on=False
    def get_overimg(self,world):
        return self.oimgs[self.on]
class ArrowHob(Hob):
    imgs=imgstrip4f("ArrowCooker",16)
    img=imgs[0]
    updates = True
    def __init__(self, x, y, d=0):
        self.place(x, y)
        self.dir = D.get_dir(d)
        self.d = d
    def update(self, world, events):
        if self.contents:
            self.contents.heat()
            if self.contents.contents:
                self.warn = self.contents.contents.warn
                self.progress = self.contents.contents.progress
            else:
                self.warn = False
                self.progress = None
        if not self.moving:
            dx, dy = self.dir if world.button else D.anti(self.dir)
            if self.move(dx, dy, world):
                self.locked = True
            else:
                self.locked = False
    def get_img(self, world):
        return self.imgs[self.d]
class Conveyor(Counter):
    anitick=0
    updates = False
    cconv=None
    name="Conv"
    ticks = True
    @classmethod
    def init(cls):
        convs = imgrot(img4("Conv"))
        cls.imgs=[]
        for d in range(4):
            rimgs=[]
            for n in range(14):
                i=cls.img.copy()
                ss=i.subsurface(pygame.Rect(4,4,56,56))
                ss.blit(convs[d],((n*4 if d==1 else n*-4 if d==3 else 0),(n*4 if d==2 else n*-4 if d==0 else 0)))
                if n!=0:
                    ss.blit(convs[d], ((n*4-56 if d==1 else n*-4+56 if d==3 else 0),(n*4-56 if d==2 else n*-4+56 if d==0 else 0)))
                rimgs.append(i)
            cls.imgs.append(rimgs)
        cls.img=cls.imgs[0]
    @classmethod
    def tick(cls):
        cls.anitick+=1
        cls.anitick%=54
    def __init__(self, x, y, d=0):
        self.place(x, y)
        self.dir = D.get_dir(d)
        self.d = d
    def update(self,world,events):
        if self.cconv is None:
            tx,ty=D.offset(self.d,self)
            go=world.get_o(tx,ty)
            if go and go.name=="Conv":
                self.cconv=go
            else:
                self.cconv=False
        if self.contents:
            if not self.f_norm():
                self.f_normalise()
            else:
                if self.cconv:
                    if max(abs(self.fx),abs(self.fy))==32:
                        if not self.cconv.contents:
                            self.cconv.contents = self.contents
                            self.contents=None
                            self.cconv.fx=-self.fx
                            self.cconv.fy=-self.fy
                            self.cconv.on_place(world)
                            self.on_take(world)
                    else:
                        self.fx += self.dir[0]
                        self.fy += self.dir[1]
                else:
                    tx, ty = D.offset(self.d, self)
                    go = world.get_o(tx, ty)
                    if not go or (not go.contents and go.can_place(self.contents)):
                        if max(abs(self.fx), abs(self.fy)) == 64:
                            if not go:
                                world.spawn(FloorIngs(tx,ty,self.contents))
                            else:
                                go.contents = self.contents
                                go.on_place(world)
                            self.contents = None
                            self.on_take(world)
                        else:
                            self.fx += self.dir[0]
                            self.fy += self.dir[1]
                    else:
                        self.f_normalise()
        else:
            world.del_updates(self)
    def get_img(self,world):
        return self.imgs[self.d][self.anitick//4]
    def f_norm(self):
        if not self.d:
            return self.fy<=0 and not self.fx
        elif self.d==1:
            return self.fx>=0 and not self.fy
        elif self.d==2:
            return self.fy>=0 and not self.fx
        else:
            return self.fx<=0 and not self.fy
    def f_normalise(self):
        if self.fx>0:
            self.fx-=1
        elif self.fx<0:
            self.fx+=1
        if self.fy > 0:
            self.fy -= 1
        elif self.fy < 0:
            self.fy += 1
    def on_take(self,world):
        self.fx=0
        self.fy=0
        world.del_updates(self)
    def on_place(self,world):
        world.reg_updates(self)
class FloorIngs(Object):
    img=blank64
    def __init__(self,contents):
        self.contents=contents
    def on_take(self,world):
        world.dest(self)
class SpawnMan(Object):
    imgs=imgstrip4("SpawnMan")
    img=imgs[0]
    name="Spawn"
    def __init__(self,x,y,d=0):
        self.place(x,y)
        self.d=d
    def get_img(self,world):
        return self.imgs[self.d]
class FlickerLight(Object):
    exists = False
    img=img4("BulbIcon")
    ttd=randint(600,1200)
    def update(self,world,events):
        if self.ttd:
            self.ttd-=1
        else:
            world.dark=not world.dark
            if world.dark:
                self.ttd=randint(180,240)
                poff.play()
            else:
                self.ttd=randint(600,1200)
                pon.play()
class SpawnPerson(Object):
    imgs=imgstrip4("PeopleSpawner")
    img=imgs[0]
    name="PSpawn"
    exists = False
    tnp=randint(120,180)
    def __init__(self,x,y,d=0):
        self.place(x,y)
        self.d=d
    def get_img(self,world):
        return self.imgs[self.d]
    def update(self,world,events):
        if self.tnp:
            self.tnp-=1
        else:
            self.tnp=randint(120,180)
            if world.is_clear(self.x,self.y):
                world.spawn(Person(self.x,self.y,self.d))
class Person(Object):
    updates = True
    speed = 2
    real=True
    def __init__(self,x,y,d):
        self.place(x,y)
        mt=choice(("Man","FMan","TMan","SMan","ManBot","ManBlack","Slime","Penguin","Woman","CatThing","Illuminati"))
        col=(randint(0,255),randint(0,255),randint(0,255))
        self.img=new_man(mt,col)[d]
        self.d=d
        dx, dy = D.get_dir(self.d)
        self.xoff=dx*-64
        self.yoff=dy*-64
        self.moving=True
    def update(self,world,events):
        if not self.moving:
            tx,ty=D.offset(self.d,self)
            dx,dy=D.get_dir(self.d)
            if not world.in_world(tx,ty):
                if self.real:
                    world.make_unreal(self)
                    self.real=False
                self.xoff+=dx*self.speed
                self.yoff+=dy*self.speed
                if max((abs(self.xoff),abs(self.yoff)))==64:
                    world.dest(self)
            else:
                self.move(dx,dy,world)

Conveyor.init()