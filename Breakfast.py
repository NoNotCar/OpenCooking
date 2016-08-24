from Food import Food, CookableFood
import pygame
import Img
from BaseClasses import Item
class Pan(Item):
    img=Img.img4("Pan")
    burnt=False
    bimg=Img.img4("BurntPan")
    def combine(self, food):
        if food.cookable and food.state=="normal" and not self.contents:
            self.contents=food
            self.re_img()
            return True
    def re_img(self):
        if self.burnt:
            self.img=self.bimg
        if self.contents:
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
class Steak(CookableFood):
    pass
items=[Pan,Steak]