from Food import Food
import Sandwich
import pygame
import Img
from BaseClasses import Item
burgeritems=["Steak"]+Sandwich.sandwichitems
class Burger(Food):
    topped=False
    simg=None
    state="normal"
    ordermultiplier = 1.5
    name="Burger"
    img=Img.img4("BunBase")
    raw_img = Img.imgsz("BunBase", (32, 32))
    def __init__(self):
        self.contents=[]
    def combine(self, food):
        if not any([self.topped,food.utensil]):
            if food.state != "normal" and food.name in burgeritems and food.name not in self.get_names():
                self.contents.append(food)
                self.re_img()
                return True
            elif food.name=="BunTop":
                self.topped=True
                self.re_img()
                return True
        elif not self.topped and food.name=="Pan" and food.contents and "cooked" in food.contents.state:
            self.contents.append(food.contents)
            food.contents=None
            food.re_img()
            self.re_img()
            return False
    def re_img(self):
        totoffset=(len(self.contents)+self.topped)*4
        self.simg = pygame.Surface((64,64+totoffset), pygame.SRCALPHA, 32).convert_alpha()
        self.simg.blit(self.img,(0,totoffset))
        yb=0
        for s in burgeritems:
            for c in self.contents:
                if c.name == s:
                    self.simg.blit(c.get_img(), (0, yb+totoffset))
                    yb-=4
        if self.topped:
            self.simg.blit(BunTop.img,(0,0))
        self.o3d=totoffset//4
    def get_img(self):
        return self.simg if self.contents else self.img
    def get_names(self):
        names = [c.name for c in self.contents]
        return [s for s in burgeritems if s in names]
    def maketag(self):
        return "Burger:" + ",".join([c.maketag() for c in sorted(self.contents)]) + ("T" if self.topped else "uT")
class BunTop(Food):
    pass
items=[BunTop]