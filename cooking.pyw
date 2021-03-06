__author__ = 'NoNotCar'
import pygame, sys
pygame.init()
pygame.font.init()
screen=pygame.display.Info()
screen = pygame.display.set_mode((screen.current_w,screen.current_h),pygame.FULLSCREEN)
screen.convert()
import Img
import Controllers
import World
import Players
import Objects
import os
import pickle
import Levels
import random
import  FX
from math import sin, radians
tfont=Img.fload("cool",64)
sfont=Img.fload("cool",32)
clock = pygame.time.Clock()
tickimg=Img.img4("Tick")
crossimg=Img.img4("Null")
cols=((255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,0,255),(0,255,255),(255,128,0),(255,128,255))
men=Objects.men
pimgs=[[Img.new_man(mt,col)[2] for col in cols] for mt in men]
mimgs=[Img.new_man(random.choice(men),(random.randint(0,255),random.randint(0,255),random.randint(0,255)))[2] for _ in xrange(31)]
breaking = False
try:
    with open("HS.sav","rb") as hsfile:
        hss=pickle.load(hsfile)
except IOError:
    hss={}
dj=Img.DJ()
start=Img.button("PLAY",sfont)
srect=None
pmax=8
dt=0
beep=Img.sndget("bleep")
ldone=Img.sndget("ldone")
imgn=0
imgx=0
wavelength=360/31.0*random.randint(1,2)
wavespeed=random.randint(-4,4)
wavemovement=random.randint(-4,4)
def format_time(time):
    t=time+60
    secs=t%3600//60
    if secs<10:
        secs="0"+str(secs)
    else:
        secs=str(secs)
    return str(t//3600)+":"+secs
def check_exit(event,no_exit=False):
    if event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
        if no_exit:
            return True
        sys.exit()
while not breaking:
    for event in pygame.event.get():
        check_exit(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx,my=pygame.mouse.get_pos()
            if srect.collidepoint(mx,my):
                breaking = True
    screen.fill((255, 0, 0))
    brects=[]
    Img.bcentre(tfont,"OPENCOOKING",screen,-100)
    srect=Img.cxblit(start,screen,500)
    for n,i in enumerate(mimgs):
        screen.blit(i,((n*64+imgx+64)%1984-64,800+sin(radians(imgn+n*wavelength))*100))
    imgn+=wavespeed
    imgn%=360
    imgx+=wavemovement
    imgx%=1984
    pygame.display.flip()
    clock.tick(60)
    dj.update()
del mimgs
breaking=False
controllers=[Controllers.Keyboard1(),Controllers.Keyboard2()]+[Controllers.UniJoyController(n) for n in range(pygame.joystick.get_count())]
activecons=[]
acps=[]
mans=[]
ordermans=[]
rsps=[]
rsc=[]
while not breaking:
    gevents=pygame.event.get()
    for event in gevents:
        check_exit(event)
        if event.type == pygame.MOUSEBUTTONDOWN and len(rsps):
            breaking = True
    for n,c in enumerate(activecons):
        if c.get_buttons(gevents)[0]:
            if acps[n] not in rsps:
                rsps.append(acps[n])
                rsc.append(c)
                ordermans.append(mans[n])
    for c in controllers[:]:
        if c.get_buttons(gevents)[0]:
            activecons.append(c)
            acps.append(0)
            mans.append(0)
            controllers.remove(c)
    screen.fill((0, 0, 0))
    Img.bcentrex(tfont,"PLAYER SELECT",screen,0,(255,255,255))
    n=-1
    for n,c in enumerate(activecons):
        if c not in rsc:
            cdir=c.get_dir_pressed(gevents)
            if cdir:
                acps[n]=(acps[n]+cdir[0])%len(pimgs[0])
                mans[n]=(mans[n]+cdir[1])%len(pimgs)
            Img.cxblit(pimgs[mans[n]][acps[n]],screen,n*64+94)
            if acps[n] in rsps:
                Img.cxblit(crossimg,screen,n*64+94,64)
        else:
            Img.cxblit(pimgs[mans[n]][acps[n]],screen,n*64+94)
            Img.cxblit(tickimg,screen,n*64+94,64)
    if len(rsps)<pmax:
        Img.bcentrex(sfont,"Press <pickup> to join",screen,n*64+160,(255,255,255))
    else:
        break
    pygame.display.flip()
    clock.tick(60)
    dj.update()
maxlevel=len(os.listdir(Img.np(Img.loc+"saves/")))
while True:
    dj.switch("Cooking")
    breaking=False
    limgs = []
    for n in range(maxlevel):
        img = Img.img("LevelBox")
        try:
            hs = hss[(n//10+1, n%10+1)]
            Img.bcentre(sfont, "%s-%s" % (str(n//10+1),str(n%10+1)), img, -16)
            Img.bcentre(sfont, str(hs), img, 10, (200, 200, 0))
        except KeyError:
            Img.bcentre(sfont, "%s-%s" % (str(n//10+1),str(n%10+1)), img, -5)
        limgs.append(img)
    rects = []
    while not breaking:
        for e in pygame.event.get():
            check_exit(e)
            if e.type==pygame.MOUSEBUTTONDOWN:
                mx,my=pygame.mouse.get_pos()
                for r,n in rects:
                    if r.collidepoint((mx,my)):
                        level=n+1
                        breaking=True
                        break
        screen.fill((255,255,0))
        Img.bcentrex(tfont,"SELECT LEVEL",screen,64)
        recting=not rects
        for n,l in enumerate(limgs):
            r=Img.cxblit(l,screen,400+n//10*96,n%10*96-464)
            if recting:
                rects.append((r,n))
        pygame.display.flip()
    players=[Players.Player(0,0, cols[rsps[n]],men[ordermans[n]], rsc[n]) for n in range(len(rsc))]
    w=World.World(players,level)
    n=level-1
    backcolour=(100, 100, 100)
    alevel=(n//10+1, n%10+1)
    tutorial=None
    if alevel in Levels.haunted:
        dj.switch("Haunted")
        backcolour=(10,10,10)
    if alevel in Levels.outdoors:
        dj.switch("Outdoor")
        backcolour=(105,211,211)
    if alevel in Levels.snowy:
        dj.switch("Snow")
        backcolour=(105,211,211)
        w.fxg=FX.snowgen
    if alevel in Levels.tutorials.keys():
        tutorial=Img.img4("Tutorial/Tut"+Levels.tutorials[alevel])
    superrect=pygame.Rect(0,0,w.size[0]*64,w.size[1]*64+64)
    superrect.centerx = screen.get_rect().centerx
    superrect.centery = screen.get_rect().centery
    subsurf=screen.subsurface(superrect)
    timerect=pygame.Rect(881,968,159,112)
    timesurf=screen.subsurface(timerect)
    screen.fill(backcolour)
    pygame.display.flip()
    time=14400
    olduprects=[]
    breaking=False
    pausing=False
    while not breaking:
        for rect in olduprects:
            screen.fill(backcolour,rect)
        uprects=[superrect,timerect]
        es=pygame.event.get()
        for e in es:
            if check_exit(e,True):
                breaking=True
            elif e.type==pygame.KEYDOWN and e.key==pygame.K_p:
                pausing=True
        w.update(es)
        w.render(subsurf)
        if time<0:
            break
        else:
            time-=1
            if time//60<=10 and not time%60:
                if time==0:
                    ldone.play()
                else:
                    beep.play()
        timesurf.fill((255,255,255))
        Img.bcentrex(tfont,format_time(time),screen,944,xoffset=4)
        Img.bcentrex(tfont, str(w.cash), screen, 1000, xoffset=4,col=(150,150,0))
        if tutorial:
            uprects.append(Img.cxblit(tutorial,screen,4))
        ox=2
        for o in w.orders:
            uprects.append(o.render(screen,(ox,2)))
            ox+=2+o.width
        if pausing:
            Img.bcentre(tfont,"PAUSED",screen)
            pygame.display.flip()
            while pausing:
                es = pygame.event.get()
                for e in es:
                    if check_exit(e, True):
                        breaking = True
                        pausing=False
                    elif e.type == pygame.KEYDOWN and e.key == pygame.K_p:
                        pausing = False
                clock.tick(60)
        pygame.display.update(olduprects+uprects)
        """if dt < 60:
            dt += 1
        else:
            dt = 0
            print clock.get_fps()"""
        if clock.get_rawtime()<=3:
            pygame.time.wait(8)
        clock.tick(60)
        dj.update()
        olduprects=uprects
    if not breaking:
        nhs=True
        try:
            maxscore=hss[(w.world,w.level)]
            if maxscore>=w.cash:
                nhs=False
            else:
                hss[(w.world, w.level)]=w.cash
        except KeyError:
            hss[(w.world, w.level)] = w.cash
        finally:
            with open("HS.sav","wb") as hsfile:
                pickle.dump(hss,hsfile)
        if nhs:
            screen.fill((255,255,0))
            Img.bcentre(tfont,"NEW HIGH SCORE: "+str(w.cash),screen)
        else:
            screen.fill((0,0,0))
            Img.bcentre(tfont,"NO NEW HIGH SCORE",screen,col=(255,255,255))
            Img.bcentre(sfont, "HIGH SCORE: "+str(hss[(w.world,w.level)]), screen,100,(255,255,255))
            Img.bcentre(sfont, "YOUR SCORE: " + str(w.cash), screen, 150, (255, 255, 255))
        pygame.display.flip()
        pygame.time.wait(5000)

