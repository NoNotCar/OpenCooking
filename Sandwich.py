from Food import Food
import Salad
import pygame
import Img
from BaseClasses import Item
sandwichitems=Salad.saladitems+["Ketchup","Mustard","Cheese"]
class Bread(Food):
    topped=False
    simg=None
    state="normal"
    ordermultiplier = 0.6
    def __init__(self):
        self.contents=[]
    def combine(self, food):
        if not any([self.topped,food.utensil]):
            if food.state != "normal" and food.name in sandwichitems and food.name not in self.get_names():
                self.contents.append(food)
                self.re_img()
                return True
            elif food.name=="Bread" and self.contents:
                self.topped=True
                self.re_img()
                return True
    def re_img(self):
        totoffset=(len(self.contents)+self.topped)*4
        self.simg = pygame.Surface((64,64+totoffset), pygame.SRCALPHA, 32).convert_alpha()
        self.simg.blit(self.img,(0,totoffset))
        yb=0
        for s in sandwichitems:
            for c in self.contents:
                if c.name == s:
                    self.simg.blit(c.get_img(), (0, yb+totoffset))
                    yb-=4
        if self.topped:
            self.simg.blit(self.img,(0,0))
        self.o3d=totoffset//4
    def get_img(self):
        return self.simg if self.contents else self.img
    def get_names(self):
        names = [c.name for c in self.contents]
        return [s for s in sandwichitems if s in names]
    def maketag(self):
        return "Bread:" + ",".join(self.get_names()) + ("T" if self.topped else "uT")
class Ketchup(Food):
    name="Ketchup"
    img=Img.img4("Ketchup")
    raw_img=Img.imgsz("KetchupBottle",(32,32))
    soupcolour = (255,0,0)
    def get_img(self):
        return self.img
class KetchupBottle(Item):
    is_supply = True
    def supply(self):
        return Ketchup("liquid")
class Mustard(Food):
    name="Mustard"
    img=Img.img4("Mustard")
    raw_img=Img.imgsz("MustardBottle",(32,32))
    soupcolour = (255,216,0)
    def get_img(self):
        return self.img
class MustardBottle(Item):
    is_supply = True
    def supply(self):
        return Mustard("liquid")
class Cheese(Food):
    pass
items=[Bread,KetchupBottle,MustardBottle,Cheese]