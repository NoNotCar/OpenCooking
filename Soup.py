from BaseClasses import Item
from Food import Food
import Img
toppings=["Cheese"]
class Soup(Item):
    colour=None
    q=0
    cooked=0
    burnt=0
    warn=False
    progress=0
    utensil = False
    is_burnt=False
    topping=None
    chunks=None
    def __init__(self,food=None):
        self.colours=[]
        self.contents=[]
        if food:
            self.add(food)
    @classmethod
    def order_init(cls,foods):
        soup=Soup()
        for f in foods:
            soup.add(f)
        soup.cooked=540
        return soup
    def add(self,food):
        self.contents.append(food)
        self.colours.append(food.soupcolour)
        if not self.chunks and food.scimg:
            self.chunks=food.scimg
        self.colour=tuple([sum([c[n] for c in self.colours])//len(self.colours) for n in range(3)])
        self.q+=1
        if self.q==3:
            self.img=Img.img4("Soup")
            if self.chunks:
                self.img.blit(self.chunks,(0,0))
            Img.colswap(self.img,(255,0,255),self.colour)
    def maketag(self):
        return "Soup:"+",".join(sorted([f.maketag() for f in self.contents]))
    def heat(self):
        if self.cooked<self.q*180:
            self.cooked+=1
            self.progress=self.cooked*14//540
            self.warn=False
        elif self.burnt<361:
            self.burnt+=1
            self.warn=True
            if self.burnt==360:
                self.contents=[]
                self.is_burnt=True
                self.colour=(10,10,10)
    def combine(self, food):
        if not self.topping and food.state!="normal" and food.name in toppings:
            self.topping=food
            self.img.blit(food.get_img(),(0,0))
            return True
class Pot(Item):
    imgs=[Img.img4("PotSoup"+str(n)) for n in range(3)]
    def combine(self, food):
        if not food.utensil and food.state!="normal" and food.soupcolour:
            if not self.contents:
                self.contents=Soup(food)
                self.re_img()
                return True
            elif self.contents.q<3:
                self.contents.add(food)
                self.re_img()
                return True
    def re_img(self):
        if self.contents:
            self.img=self.imgs[self.contents.q-1].copy()
            Img.colswap(self.img,(255,0,255),self.contents.colour)
            if self.contents.chunks:
                self.img.blit(self.contents.chunks, (0, self.contents.q*-4+4))
        else:
            self.img=self.__class__.img
    def heat(self):
        if self.contents:
            self.contents.heat()
            if self.contents.burnt==360:
                self.re_img()
items=[Pot]