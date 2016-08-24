from Food import Food
from BaseClasses import Item
import Img
saladitems = ["Lettuce", "Cucumber","Carrot","Potato","Tomato","SaladCream"]
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
class Potato(SaladItem):
    soupcolour = (224,192,111)
class SaladCream(Food):
    name="SaladCream"
    img=Img.img4("SaladCream")
    raw_img=Img.imgsz("SaladBottle",(32,32))
    def get_img(self):
        return self.img
class SaladBottle(Item):
    is_supply = True
    def supply(self):
        return SaladCream("liquid")
class Salad(Item):
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