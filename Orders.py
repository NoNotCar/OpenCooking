import Img
import Food
import pygame
orderframes=[Img.img("Order"+str(n)) for n in range(1,3)]
states={s:Img.img("State"+s.capitalize()) for s in ["chopped","grated","liquid","cooked","grilled","rolled","hammered+cooked","cooked+chopped","grated+fried"]}
class Order(object):
    width=0
    double=False
    def __init__(self,components,double=False):
        self.c=[]
        for c in components:
            if c.contents:
                self.c.extend(c.contents)
            else:
                self.c.append(c)
        try:
            baseimg=orderframes[len(self.c)-1]
        except IndexError:
            while len(orderframes)<len(self.c):
                img=orderframes[-1]
                w=img.get_width()
                toblit=img.subsurface(pygame.Rect(w-36,0,36,106))
                new_img=pygame.Surface((w+34,106))
                new_img.blit(img,(0,0))
                new_img.blit(toblit,(w-2,0))
                orderframes.append(new_img)
            baseimg = orderframes[len(self.c) - 1]
        self.img = pygame.Surface((baseimg.get_width(), 138), pygame.SRCALPHA, 32).convert_alpha()
        self.img.blit(baseimg,(0,0))
        if len(self.c)==1:
            self.img.blit(self.c[0].raw_img,(19,74))
            if self.c[0].state!="normal":
                self.img.blit(states[self.c[0].state], (17, 104))
        else:
            for n,c in enumerate(self.c):
                self.img.blit(c.raw_img, (2+n*34, 74))
                if c.state != "normal":
                    self.img.blit(states[c.state], (n*34, 104))
        self.plate=Food.Plate()
        for c in components:
            assert self.plate.combine(c), "INVALID RECIPE: "+str(components)+" OFFENDING INGREDIENT: "+str(c)

        if len(self.c)<3:
            subsurf = self.img.subsurface(pygame.Rect(3,8,64,64))
        else:
            subsurf = self.img.subsurface(pygame.Rect(3+17*len(self.c)-34, 8,64,64))
        subsurf.blit(self.plate.get_img(),(0,-self.plate.o3d*4))
        self.time=int((900+len(self.c)*900)*self.plate.contents.ordermultiplier)
        if double:
            self.time*=1.5
            self.time=int(self.time)
        self.stime=self.time
        self.img=Img.xn(self.img,2)
        self.width=self.img.get_width()
    def render(self,screen,dest):
        rect=screen.blit(self.img,dest)
        pygame.draw.rect(screen,(255*(self.stime-self.time)//self.stime,255*self.time//self.stime,0),pygame.Rect(4+dest[0],4+dest[1],(132+68*((len(self.c) if len(self.c)>2 else 2)-2))*self.time//self.stime,8))
        return rect
    def retime(self,time):
        self.time=time
        self.stime=time
    def tick(self):
        self.time-=1
class DoubleOrder(Order):
    double=True
    img=Img.xn(Img.img("Plus"),2)
    def __init__(self,orders):
        time=int(orders[0].time*1.5)
        orders[1].retime(time)
        self.time=time
        orders[0].retime(time)
        self.os=orders
        self.width=sum([o.width for o in self.os])+64
    def render(self,screen,dest):
        fr=self.os[0].render(screen,dest)
        screen.blit(self.img,(dest[0]+fr.w,dest[1]))
        sr=self.os[1].render(screen,(dest[0]+fr.w+64,dest[1]))
        return fr.union(sr)
    def tick(self):
        for o in self.os:
            o.time-=1
        self.time=o.time