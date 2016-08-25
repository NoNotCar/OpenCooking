import Img, pygame
from BaseClasses import Item
class Food(Item):
    utensil = False
    choppable=True
    grateable = True
    cookable=True
    def __init__(self,state="normal"):
        self.state=state
    @classmethod
    def init(cls):
        cls.name=cls.__name__
        name=cls.name
        cls.img=Img.img4(name)
        cls.raw_img=Img.imgsz(name,(32,32))
        try:
            cls.chopped_img=Img.img4("Chopped"+name)
        except pygame.error:
            cls.choppable=False
        try:
            cls.grated_img = Img.img4("Grated" + name)
        except pygame.error:
            cls.grateable = False
        try:
            cls.cooked_img = Img.img4("Cooked" + name)
        except pygame.error:
            cls.cookable = False
    def maketag(self):
        return self.state+self.__class__.name
    def get_img(self):
        return self.img if self.state=="normal" else self.chopped_img if self.state=="chopped" else self.grated_img if self.state=="grated" else self.cooked_img
class CookableFood(Food):
    cookingtime=600
    burningtime=300
    progress=None
    warn=None
    cookprog=0
    burnprog=0
    def heat(self):
        #Heat the food. Returns true if food changes state
        if self.cookprog<self.cookingtime:
            self.cookprog+=1
            self.progress=self.cookprog*14//self.cookingtime
            self.warn=False
            if self.cookprog==self.cookingtime:
                self.set_state("cooked")
                return True
        elif self.burnprog<self.burningtime:
            self.burnprog+=1
            self.warn=True
        else:
            return True
class Plate(Item):
    name="Plate"
    dirty=False
    dimg=Img.img4("DirtyPlate")
    def combine(self, food):
        if self.dirty:
            return False
        if food.utensil:
            if food.name=="Pot" and food.contents and food.contents.q==3 and food.contents.cooked>=540 and not food.contents.is_burnt:
                self.contents=food.contents
                food.contents=None
                self.re_img()
                food.re_img()
            elif food.name=="Pan" and food.contents:
                self.contents = food.contents
                food.contents = None
                self.re_img()
                food.re_img()
            return False
        if not self.contents:
            self.contents=food
            self.re_img()
            return True
        else:
            if self.contents.pcombine(food,self):
                self.re_img()
                return True
    def re_img(self):
        self.img = pygame.Surface((64, 64 + self.contents.o3d*4), pygame.SRCALPHA, 32).convert_alpha()
        self.img.blit(self.__class__.img,(0,self.contents.o3d*4))
        self.img.blit(self.contents.get_img(),(0,0))
        self.o3d=self.contents.o3d
    def maketag(self):
        if self.contents:
            return "Plate:"+self.contents.maketag()
        else:
            return "Plate"
    def get_img(self):
        return self.dimg if self.dirty else self.img
import Salad
import Sandwich
import Soup
import Breakfast
import Burger

items=[Plate]+Salad.items+Sandwich.items+Soup.items+Breakfast.items+Burger.items
for i in items:
    i.init()
