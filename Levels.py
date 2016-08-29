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
    if level==4:
        return world_3(1) if randint(0,1) else world_1(1)
    if level==7:
        if randint(0,1):
            return world_3(1)
        else:
            return randomsoup([Salad.Tomato,Breakfast.Steak,Salad.Carrot,Sandwich.Ketchup],True)
    if level==8:
        return toastie([Salad.Tomato,Salad.Carrot,Sandwich.Ketchup,Salad.Lettuce,Sandwich.Cheese],3)
    if level==9:
        return world_3(8) if randint(0,1) else pizza([Salad.Tomato,Salad.Carrot],2)
    if level==10:
        return world_3(3) if randint(0,1) else pizza([Salad.Tomato,Salad.Carrot,Breakfast.Steak],2)
    oc=[]
    oc.append(Burger.Burger())
    if level==3 and not randint(0,2):
        oc.append(Breakfast.Steak("hammered+cooked"))
        oc.append(Burger.Chicken("hammered+cooked"))
    elif level==1 or randint(0,1):
        oc.append(Breakfast.Steak("hammered+cooked"))
    else:
        oc.append(Burger.Chicken("hammered+cooked"))
    extras=[Salad.Lettuce,Salad.Tomato,Sandwich.Cheese,Sandwich.Ketchup]
    if level>1:
        extras.extend([Salad.Cucumber,Sandwich.Mustard])
    for e in extras:
        if not randint(0,2):
            if e.name in ["Ketchup","Mustard"]:
                oc.append(e("liquid"))
            elif e.name=="Cheese":
                oc.append(e("grated"))
            else:
                oc.append(e("chopped"))
    oc.append(Burger.BunTop())
    return oc
def world_4(level):
    if level==1:
        return world_1(3)
    oc=[]
    oc.append(Salad.Potato("grated+fried"))
    if randint(0,1):
        oc.append(Sandwich.Ketchup("liquid"))
    if randint(0,1):
        oc.append(Sandwich.Mustard("liquid"))
    return oc
def randomsoup(soupings,allow_cheese):
    soupitems = []
    for _ in range(3):
        ch = choice(soupings)
        if ch.name in ["Ketchup", "Mustard"]:
            soupitems.append(ch("liquid"))
        elif ch.name=="Carrot":
            soupitems.append(ch("chopped" if randint(0,1) else "grated"))
        elif ch.name=="Steak":
            soupitems.append(ch("cooked+chopped"))
        else:
            soupitems.append(ch("chopped"))
    return [Soup.Soup.order_init(soupitems)] + ([Sandwich.Cheese("grated")] if allow_cheese and randint(0, 1) else [])
def toastie(toastings,chance):
    toastitems = []
    while not toastitems:
        for t in toastings:
            if not randint(0,chance):
                if t.name in ["Ketchup", "Mustard"]:
                    toastitems.append(t("liquid"))
                elif t.name == "Carrot":
                    toastitems.append(t("chopped" if randint(0, 1) else "grated"))
                elif t.name == "Cheese":
                    toastitems.append(t("grated"))
                elif t.name == "Steak":
                    toastitems.append(t("cooked+chopped"))
                else:
                    toastitems.append(t("chopped"))
    return [Sandwich.Bread("grilled")]+toastitems+[Sandwich.Bread("grilled")]
def pizza(pizzings,chance):
    pizzitems = []
    if randint(0,3):
        pizzitems.append(Sandwich.Cheese("grated"))
    for t in pizzings:
        if not randint(0, chance):
            if t.name in ["Ketchup", "Mustard"]:
                pizzitems.append(t("liquid"))
            elif t.name == "Carrot":
                pizzitems.append(t("chopped" if randint(0, 1) else "grated"))
            elif t.name == "Steak":
                pizzitems.append(t("cooked+chopped"))
            else:
                pizzitems.append(t("chopped"))
    npizza=Burger.Dough()
    npizza.order_init(pizzitems)
    return [npizza]
orderers=[world_1,world_2,world_3,world_4]
haunted=[(3,4),(3,10),(4,1)]
outdoors=[(3,5),(3,6)]
snowy=[(4,1),(4,2)]
tutorials={(1,1):"Salad",(1,6):"Sandwich"}