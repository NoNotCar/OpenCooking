from Food import Food, CookableFood
import pygame
import Img
from BaseClasses import Item
class Pan(Item):
    img=Img.img4("Pan")
    burnt=False
    bimg=Img.img4("BurntPan")
    def combine(self, food):
        if food.cookable and "cooked" not in food.state and not self.contents and not self.burnt:
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
class Steak(CookableFood):
    ordermultiplier = 1.5
    pimg = Img.img4("Patty")
    cpimg = Img.img4("CookedPatty")
    hammerable = True
    def set_state(self,state):
        if self.state=="hammered" and state=="cooked":
            self.state="hammered+cooked"
        else:
            self.state=state
    def get_img(self):
        return {"normal":self.img,"hammered":self.pimg,"cooked":self.cooked_img,"hammered+cooked":self.cpimg}[self.state]
items=[Pan,Steak]