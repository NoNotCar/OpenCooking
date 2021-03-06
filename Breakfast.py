from Food import Food, CookableFood
import pygame
import Img
from BaseClasses import Item
class Pan(Item):
    img=Img.img4("Pan")
    burnt=False
    bimg=Img.img4("BurntPan")
    def combine(self, food):
        if food.can_change_state("cooked") and not self.contents and not self.burnt:
            self.contents=food
            self.re_img()
            return True
    def re_img(self):
        if self.burnt:
            self.img=self.bimg
        elif self.contents:
            self.img=self.__class__.img.copy()
            self.img.blit(self.contents.get_img(),(0,0))
        else:
            self.img=self.__class__.img
    def heat(self):
        if self.contents:
            if self.contents.heat():
                if self.contents.burnprog:
                    self.contents=None
                    self.burnt=True
                    self.re_img()
                else:
                    self.re_img()
    def maketag(self):
        return "Pan:"+self.contents.maketag() if self.contents else "empty"
class Basket(Item):
    img=Img.img4("Basket")
    o3d=4
    name="Basket"
    def combine(self, food):
        if food.can_change_state("fried") and not self.contents:
            self.contents=food
            self.re_img()
            return True
    def re_img(self):
        if self.contents:
            self.img=self.__class__.img.copy()
            self.img.blit(self.contents.get_img(),(0,0))
        else:
            self.img=self.__class__.img
    def heat(self):
        if self.contents:
            if self.contents.fry():
                if self.contents.burnprog:
                    self.contents=None
                    self.re_img()
                else:
                    self.re_img()
    def maketag(self):
        return "Basket:"+self.contents.maketag() if self.contents else "empty"
class Steak(CookableFood):
    ordermultiplier = 1.5
    hammerable = True
    soupcolour = (96, 61, 26)
items=[Pan,Steak]