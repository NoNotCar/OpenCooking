from Food import Food, FryableFood
from BaseClasses import Item
import Img
saladitems = ["Lettuce", "Cucumber","Carrot","Tomato","SaladCream"]
class SaladItem(Food):
    def pcombine(self, food, plate):
        if food.name in saladitems and self.state in ("chopped","liquid") and food.state in ("chopped","liquid"):
            plate.contents=Salad([self,food])
            return True
class Lettuce(SaladItem):
    pass
class Cucumber(SaladItem):
    soupcolour = (142,255,157)
class Tomato(SaladItem):
    soupcolour = (236,0,0)
class Carrot(SaladItem):
    soupcolour = (255,101,0)
    scimg = Img.img4("SoupCarrot")
class Potato(FryableFood):
    soupcolour = (224,192,111)
    ordermultiplier = 1.5
    def combine(self, food):
        if food.state=="liquid" and self.state=="grated+fried":
            if not self.contents:
                self.contents=[self,food]
            elif food.name not in [f.name for f in self.contents]:
                self.contents.append(food)
            else:
                return False
            self.re_img()
            return True
    def re_img(self):
        self.img=self.stateimgs[self.state].copy()
        if self.contents:
            for f in sorted(self.contents):
                if f is not self:
                    self.img.blit(f.get_img(),(0,0))
    def get_img(self):
        if self.state=="grated+fried" and self.contents:
            return self.img
        else:
            return FryableFood.get_img(self)
    def maketag(self):
        if self.state=="grated+fried" and self.contents:
            return "Chips:"+",".join([f.maketag() for f in sorted(self.contents) if f is not self])
        else:
            return "Potato"+self.state
class SaladCream(Food):
    name="SaladCream"
    img=Img.img4("SaladCream")
    raw_img=Img.imgsz("SaladBottle",(32,32))
    removable = False
    def get_img(self):
        return self.img
class SaladBottle(Item):
    is_supply = True
    def supply(self):
        return SaladCream("liquid")
class Salad(Item):
    removable = False
    def __init__(self,salad):
        self.contents=salad
    def pcombine(self, food, plate):
        if food.state in ("chopped","liquid") and food.name in saladitems and food.name not in self.get_names():
            self.contents.append(food)
            return True
    def get_img(self):
        img=Img.blank64.copy()
        for s in saladitems:
            for c in self.contents:
                if c.name==s:
                    img.blit(c.get_img(),(0,0))
        return img
    def get_names(self):
        names=[c.name for c in self.contents]
        return [s for s in saladitems if s in names]
    def maketag(self):
        return "Salad:"+",".join(self.get_names())
items=[Tomato,Lettuce,Cucumber,Carrot,Potato,SaladBottle]