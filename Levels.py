from Orders import Order
from random import randint, choice
import Salad
import Sandwich
import Soup
import Breakfast
import Burger
def new_order(level,world):
    return Order(orderers[world-1](level))
def world_1(level):
    oc = []
    breading=randint(0, 2) and level>5
    if randint(0, 1):
        oc.append(Salad.Cucumber("chopped"))
    if randint(0, 1):
        oc.append(Salad.Tomato("chopped"))
    if level==10 and randint(0,1) and breading:
        oc.append(Sandwich.Cheese("grated"))
    if not oc or randint(0, 1):
        oc.append(Salad.Lettuce("chopped"))
    if randint(0, 1) and level>1:
        if level<=8 or not breading:
            oc.append(Salad.SaladCream("liquid"))
        else:
            if randint(0,1):
                oc.append(Salad.SaladCream("liquid"))
            if randint(0,1):
                oc.append(Sandwich.Ketchup("liquid"))
            if randint(0, 1):
                oc.append(Sandwich.Mustard("liquid"))
    if breading:
        oc.insert(0,Sandwich.Bread())
        oc.append(Sandwich.Bread())
    return oc
def world_2(level):
    if level in [3,4]:
        return world_2(2) if randint(0,1) else world_1(10)
    if level==9:
        return world_2(2) if randint(0,2) else [Breakfast.Steak("cooked")]
    if level==10:
        return world_2(9) if randint(0,1) else world_1(10)
    soupitems=[]
    soupings=[Salad.Cucumber,Salad.Tomato]
    if level>1:
        soupings.append(Salad.Carrot)
    if level>4:
        soupings.append(Salad.Potato)
    if level>6:
        soupings.append(Sandwich.Ketchup)
        soupings.append(Sandwich.Mustard)
    for _ in range(3):
        if level>4 and not randint(0,2):
            soupitems.append(Salad.Carrot("grated"))
        else:
            ch=choice(soupings)
            if ch.name in ["Ketchup","Mustard"]:
                soupitems.append(ch("liquid"))
            else:
                soupitems.append(ch("chopped"))
    return [Soup.Soup.order_init(soupitems)]+([Sandwich.Cheese("grated")] if level>1 and randint(0,1) else [])
def world_3(level):
    oc=[]
    oc.append(Burger.Burger())
    if level==1 or randint(0,1):
        oc.append(Breakfast.Steak("hammered+cooked"))
    else:
        oc.append(Burger.Chicken("hammered+cooked"))
    extras=[Salad.Lettuce,Salad.Tomato,Sandwich.Cheese,Sandwich.Ketchup]
    if level>1:
        extras.extend([Salad.Cucumber,Sandwich.Mustard])
    for e in extras:
        if randint(0,1):
            if e.name=="Ketchup":
                oc.append(e("liquid"))
            elif e.name=="Cheese":
                oc.append(e("grated"))
            else:
                oc.append(e("chopped"))
    oc.append(Burger.BunTop())
    return oc
orderers=[world_1,world_2,world_3]
