import Img, pygame
from BaseClasses import Item
class Food(Item):
    utensil = False
    def __init__(self,state="normal"):
        self.state=state
    @classmethod
    def init(cls):
        cls.name=cls.__name__
        cls.validstates=[]
        name=cls.name
        cls.img=Img.img4(name)
        cls.stateimgs={"normal":cls.img}
        cls.raw_img=Img.imgsz(name,(32,32))
        for s in ["chopped","grated","cooked","hammered","grilled","hammered+cooked","cooked+chopped"]:
            try:
                cls.stateimgs[s]=Img.img4("".join([ss.capitalize() for ss in s.split("+")])+name)
                cls.validstates.append(s)
            except pygame.error:
                pass
        cls.einit()
    @classmethod
    def einit(cls):
        pass
    def maketag(self):
        return self.state+self.__class__.name
    def get_img(self):
        return self.stateimgs[self.state]
    def can_change_state(self,tstate):
        if self.state=="normal":
            return tstate in self.validstates
        else:
            return self.state+"+"+tstate in self.validstates
    def set_state(self,state):
        if self.state=="normal":
            self.state=state
        else:
            self.state+="+"+state
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
class GrillableFood(Food):
    cookingtime=600
    burningtime=300
    progress=None
    warn=None
    cookprog=0
    burnprog=0
    def grill(self):
        #Heat the food. Returns true if food changes state
        if self.cookprog<self.cookingtime:
            self.cookprog+=1
            self.progress=self.cookprog*14//self.cookingtime
            self.warn=False
            if self.cookprog==self.cookingtime:
                self.set_state("grilled")
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
        if food.utensil and not self.contents:
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
            self.re_img()
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
