__author__ = 'NoNotCar'
import pygame
import os
from random import choice
import colorsys

np = os.path.normpath
loc = os.getcwd() + "/Assets/"
pygame.mixer.init()

def img(fil):
    return pygame.image.load(np(loc + fil + ".png")).convert_alpha()
def img4(fil):
    return xn(img(fil),4)
def xn(img,n):
    return pygame.transform.scale(img,(int(img.get_width()*n),int(img.get_height()*n))).convert_alpha()
def imgsz(fil, sz):
    return pygame.transform.scale(pygame.image.load(np(loc + fil + ".png")), sz).convert_alpha()

def imgstrip4(fil):
    img = pygame.image.load(np(loc + fil + ".png"))
    imgs = []
    h=img.get_height()
    for n in range(img.get_width() // h):
        imgs.append(pygame.transform.scale(img.subsurface(pygame.Rect(n * h, 0, h, h)), (h*4, h*4)).convert_alpha())
    return imgs
def imgstrip(fil):
    img = pygame.image.load(np(loc + fil + ".png"))
    imgs = []
    h=img.get_height()
    for n in range(img.get_width() // h):
        imgs.append(img.subsurface(pygame.Rect(n * h, 0, h, h)).convert_alpha())
    return imgs
def imgstrip4f(fil,w):
    img = pygame.image.load(np(loc + fil + ".png"))
    imgs = []
    h=img.get_height()
    for n in range(img.get_width() // w):
        imgs.append(pygame.transform.scale(img.subsurface(pygame.Rect(n * w, 0, w, h)), (w*4, h*4)).convert_alpha())
    return imgs
def imgrot(i):
    imgs=[i]
    for n in range(3):
        imgs.append(pygame.transform.rotate(i,-90*n-90))
    return imgs


def musplay(fil,loops=-1):
    if fil[:4]=="MEMX":
        pygame.mixer.music.load(np(loc+"EMX/Menu/" + fil[4:]+".ogg"))
    elif fil[:4]=="CEMX":
        pygame.mixer.music.load(np(loc + "EMX/Cooking/" + fil[4:] + ".ogg"))
    elif fil[:4] == "MMUS":
        pygame.mixer.music.load(np(loc + "Music/Menu/" + fil[4:] + ".ogg"))
    elif fil[:4] == "CMUS":
        pygame.mixer.music.load(np(loc + "Music/Cooking/" + fil[4:] + ".ogg"))
    else:
        pygame.mixer.music.load(np(loc+"Music/" + fil+".ogg"))
    pygame.mixer.music.play(loops)


def bcentre(font, text, surface, offset=0, col=(0, 0, 0), xoffset=0):
    render = font.render(str(text), True, col)
    textrect = render.get_rect()
    textrect.centerx = surface.get_rect().centerx + xoffset
    textrect.centery = surface.get_rect().centery + offset
    return surface.blit(render, textrect)

def bcentrex(font, text, surface, y, col=(0, 0, 0), xoffset=0):
    render = font.render(str(text), True, col)
    textrect = render.get_rect()
    textrect.centerx = surface.get_rect().centerx + xoffset
    textrect.top = y
    return surface.blit(render, textrect)
def bcentrerect(font, text, surface, rect, col=(0, 0, 0)):
    render = font.render(str(text), True, col)
    textrect = render.get_rect()
    textrect.centerx = rect.centerx
    textrect.centery = rect.centery
    return surface.blit(render, textrect)
def cxblit(source, dest, y, xoff=0):
    srect=source.get_rect()
    drect=dest.get_rect()
    srect.centerx=drect.centerx+xoff
    srect.top=y
    return dest.blit(source,srect)
def sndget(fil):
    return pygame.mixer.Sound(np(loc+"Sound/"+fil+".wav"))

def hflip(img):
    return pygame.transform.flip(img,1,0)

def x4(img):
    return pygame.transform.scale(img,(img.get_width()*4,img.get_height()*4))

def fload(fil,sz=16):
    return pygame.font.Font(np(loc+fil+".ttf"),sz)
buttimg=img4("MenuButton")
def button(text,font):
    img=buttimg.copy()
    bcentre(font,text,img,-4)
    return img
# draw some text into an area of a surface
# automatically wraps words
# returns any text that didn't get blitted
def drawTextRect(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text
def colswap(img,sc,ec):
    px=pygame.PixelArray(img)
    px.replace(sc,ec)
def colcopy(img,sc,ec):
    i=img.copy()
    px=pygame.PixelArray(i)
    px.replace(sc,ec)
    return i
def new_man(fil,col):
    imgs=imgstrip4(fil)
    for i in imgs:
        colswap(i,(128,128,128),col)
    return imgs
def darken(surface, value):
    "Value is 0 to 255. So 128 would be 50% darken"
    dark = pygame.Surface(surface.get_size(), 32)
    dark.set_alpha(value, pygame.RLEACCEL)
    surface.blit(dark, (0, 0))
def darkcopy(surface,value):
    nsurf=surface.copy()
    darken(nsurf,value)
    return nsurf
def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


blank64=img4("Trans")
memxs = os.listdir(np(loc+"EMX/Menu/"))
cemxs = os.listdir(np(loc+"EMX/Cooking/"))
mmusics=os.listdir(np(loc+"Music/Menu/"))
cmusics=os.listdir(np(loc+"Music/Cooking/"))
memix=[]
cemix=[]
mmus=[]
cmus=[]
for emx in memxs:
    if emx[-4:] == ".ogg":
        memix.append("MEMX"+emx[:-4])
for emx in cemxs:
    if emx[-4:] == ".ogg":
        cemix.append("CEMX"+emx[:-4])
for mus in mmusics:
    if mus[-4:] == ".ogg":
        mmus.append("MMUS"+mus[:-4])
for mus in cmusics:
    if mus[-4:] == ".ogg":
        cmus.append("CMUS"+mus[:-4])
class DJ(object):
    def __init__(self):
        if memix:
            self.songs=memix
        else:
            self.songs=mmus
    def switch(self):
        if cemix:
            self.songs=cemix
        else:
            self.songs=cmus
        pygame.mixer.music.stop()
        musplay(choice(self.songs), 1)
    def update(self):
        if not pygame.mixer.music.get_busy():
            musplay(choice(self.songs),1)
prog=img4("Progress")
progresses=[prog]
wprogresses=[prog]
for n in range(1,15):
    pimg=prog.copy()
    pygame.draw.rect(pimg,(255*(14-n)//14,155*n//14,0),pygame.Rect(4,4,4*n,8))
    progresses.append(pimg)
    pimg = prog.copy()
    pygame.draw.rect(pimg, (255,100,0), pygame.Rect(4, 4, 4 * n, 8))
    wprogresses.append(pimg)
#dfont=fload("PressStart2P")