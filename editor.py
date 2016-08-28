import pygame, sys
size=13,9
loadfile="3-10"
pygame.init()
screen = pygame.display.set_mode((max([size[0],18])*64, size[1]*64+192))
import World
import Objects
import Food
import Salad
import Sandwich
import Burger
import Breakfast
import Soup
import Tiles
import Img
dj=Img.DJ()
dj.switch("Outdoor")
class EditorIter(object):
    pointer=0
    maxp=1
    def __init__(self,obj):
        self.obj=obj
    def spawn(self,x,y):
        return self.obj(x,y)
    def revolve(self,x):
        self.pointer+=x
        self.pointer%=self.maxp
    def get_img(self,world):
        return self.obj.img,self.obj.o3d
class MultiIter(EditorIter):
    def __init__(self,*objs):
        self.objs=objs
        self.maxp=len(self.objs)
    def spawn(self,x,y):
        return self.objs[self.pointer](x,y)
    def get_img(self, world):
        obj=self.objs[self.pointer]
        return obj.img, obj.o3d
class FoodIter(EditorIter):
    def __init__(self,obj,foods,allow_lone_obj=True):
        self.obj=obj
        self.foods=foods
        self.alo=allow_lone_obj
        self.maxp=len(foods)+self.alo
    def spawn(self,x,y):
        if self.alo and not self.pointer:
            return self.obj(x, y)
        else:
            return self.obj(x,y,self.foods[self.pointer-1-self.alo]())
    def get_img(self,world):
        if self.alo and not self.pointer:
            return self.obj.img,self.obj.o3d
        else:
            return self.foods[self.pointer-1-self.alo].img,0
class SpinIter(EditorIter):
    maxp=4
    def __init__(self,obj,rot_max=4):
        self.obj=obj
        self.orender=self.obj(0,0)
        self.maxp=rot_max
    def revolve(self,x):
        EditorIter.revolve(self,x)
        self.orender.d=self.pointer
    def spawn(self,x,y):
        return self.obj(x,y,self.pointer)
    def get_img(self,world):
        return self.orender.get_img(world),self.obj.o3d
w=World.EditWorld(size,loadfile)
if loadfile:
    size=w.size
clock = pygame.time.Clock()
selmenu=0
tilemenus=[[0,1,2,3],[4,5,6]]
objmenus=[FoodIter(Objects.Counter,[Food.Plate,Salad.SaladBottle,Sandwich.MustardBottle,Sandwich.KetchupBottle,Soup.Pot,Breakfast.Pan]),
          MultiIter(Objects.FoodExit,Objects.Returner),
          FoodIter(Objects.Spawner,[Salad.Cucumber,Salad.Lettuce,Salad.Tomato,Salad.Carrot,Salad.Potato],False),
          FoodIter(Objects.Spawner,[Sandwich.Bread,Sandwich.Cheese,Burger.Burger,Burger.BunTop,Breakfast.Steak,Burger.Chicken,Burger.Dough],False),
          EditorIter(Objects.Trash),MultiIter(Objects.ChoppingBoard,Objects.Grater,Objects.HammerBoard,Objects.Hob,Objects.Grill,Objects.RollingBoard),
          EditorIter(Objects.Sink),MultiIter(Objects.Button,Objects.Flipper),SpinIter(Objects.ArrowBlock),SpinIter(Objects.ArrowHob),
          SpinIter(Objects.SpawnMan,8),MultiIter(Objects.Wall,Objects.Tree),SpinIter(Objects.Conveyor),SpinIter(Objects.MultiArrowBlock),MultiIter(Objects.FixedCounter,Objects.FlickerLight),
          SpinIter(Objects.SpawnPerson)]
seltiles=[0 for _ in tilemenus]
while True:
    kmods=pygame.key.get_mods()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type==pygame.KEYDOWN and event.key==pygame.K_s and kmods&pygame.KMOD_LCTRL:
            w.save()
            print "SAVED"
        elif event.type==pygame.KEYDOWN:
            objmenu=selmenu>=len(tilemenus)
            menus=tilemenus+objmenus
            menu=menus[selmenu]
            if event.key in (pygame.K_w,pygame.K_s):
                if objmenu:
                    menus[selmenu].revolve(1 if event.key==pygame.K_w else -1)
                else:
                    seltiles[selmenu]=(seltiles[selmenu]-1)%len(menu)
            elif event.key==pygame.K_a:
                selmenu=(selmenu-1)%len(menus)
            elif event.key==pygame.K_d:
                selmenu=(selmenu+1)%len(menus)
    seltype=selmenu<len(tilemenus)
    if pygame.mouse.get_pressed()[0]:
        mpos=pygame.mouse.get_pos()
        if mpos[0]<size[0]*64 and 64<mpos[1]<size[1]*64+64:
            if seltype:
                w.t[mpos[0]//64][mpos[1]//64-1]=tilemenus[selmenu][seltiles[selmenu]]
            else:
                if kmods&pygame.KMOD_LSHIFT:
                    w.w[mpos[0]//64][mpos[1]//64-1]=None
                else:
                    w.spawn(objmenus[selmenu - len(tilemenus)].spawn(mpos[0] // 64, mpos[1] // 64 - 1))
    screen.fill((100, 100, 100))
    w.render(screen)
    for n,tm in enumerate(tilemenus):
        screen.blit(Tiles.tiles[tm[seltiles[n]]].img,(n*64,size[1]*64+80))
    for on,om in enumerate(objmenus):
        gi=om.get_img(w)
        screen.blit(gi[0],(n*64+64+on*64,size[1]*64+80-gi[1]*4))
    off=selmenu*64
    pygame.draw.polygon(screen,(0,0,0),[(off+32,size[1]*64+160),(off,size[1]*64+192),(off+64,size[1]*64+192)])
    pygame.display.flip()
    clock.tick(60)
    dj.update()