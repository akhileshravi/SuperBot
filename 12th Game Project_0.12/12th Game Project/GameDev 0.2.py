import pygame,sys
import time, random

from pygame.locals import *

pygame.init()


scrwidth = 640
scrheight = 360
scr = pygame.display.set_mode((scrwidth,scrheight),0,32)
                    

pwidth = 150          #sizes of the images
pheight = 40

skwidth = 60
skheight = 70

#better to have pics which require high resolution in jpg
#pics which are small in size/res can be in png instead
back = "back.jpg"
cursorimg = "cursorimg.png"
dot = "dot.jpg"
platimg = "platform2.png"
skaterimg = "skater.jpg"


#must convert images to use in pygame

background = pygame.image.load(back).convert()
mscursor = pygame.image.load(cursorimg).convert_alpha()
dot = pygame.image.load(dot).convert_alpha()
platimg = pygame.image.load(platimg).convert_alpha()
skimg = pygame.image.load(skaterimg).convert()




#Classes
class MainChar(pygame.sprite.Sprite):

    flightstate = False
    alive = True
    
    def __init__(self):
        
        pygame.sprite.Sprite.__init__(self)
 
        self.image = skimg
        self.rect = self.image.get_rect()
        self.rect.x = 30
        self.rect.y = ((scrheight + 20 )/2) - skheight



class Plat(pygame.sprite.Sprite):

    
    plist = []

    def __init__(self,px,py):


        pygame.sprite.Sprite.__init__(self) 
        self.image = platimg
        self.rect = self.image.get_rect()
        self.rect.x = px
        self.rect.y = py
        Plat.plist += [self]


    def update(self,dpx,dpy):

        self.rect.x += dpx
        self.rect.y += dpy

        if self in Plat.plist and self.rect.x < -(pwidth) :

            Plat.plist.remove(self)
            splist.remove(self)
            del self
            

    def __del__(self):
        pass
        


def Platgen(yabs, sigma):


    for i in range(random.randint(1,8)):
        platform = Plat( scrwidth +i*pwidth , random.gauss( yabs-30, sigma))
        splist.add(platform)
                    


#Data Definitions
skater = MainChar()
splist = pygame.sprite.Group()
splist.add(skater)


fps = 60

dx = -5
dy = 0

yabs = skheight+skater.rect.y-1     #starting height of platforms (mean of Gaussian Distribution)
sigma = 150 #Standard deviation for the Gaussian distribution of platforms

clock = pygame.time.Clock()

for i in range(10):
    platform = Plat(i*pwidth, skheight+skater.rect.y-1)
    splist.add(platform)
    
st = time.time()

fsj = False

while True:


    scr.blit(background,(0,0))
    splist.draw(scr)
    scr.blit(skater.image, (skater.rect.x,skater.rect.y))

    
    pygame.display.update()


    if dy == 2 and time.time()-uptime >= 0.8:
        dy = -2
        uptime = 0


    if dy != 2:
        dy = -2
        for i in Plat.plist:
    
            if i.rect.x-skwidth-6 <= skater.rect.x <= (i.rect.x+pwidth+6) and -3<i.rect.y -(skater.rect.y+skheight)<3 :

                dy = 0
                fsj = False
                break
        


    yabs += dy
    for i in Plat.plist:
        i.update(dx,dy)

    if len(Plat.plist) < 4:
        Platgen(yabs, sigma)


        
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if dy == 0 or fsj:
                    dy = 2
                    uptime = time.time()
                    fsj = not(fsj)
            
            elif event.key in [K_q,K_ESCAPE]:
                pygame.quit()
                sys.exit()
                
        if event.type == MOUSEBUTTONDOWN and dy == 0:
            dy = 2
            uptime = time.time()

        
    clock.tick(fps)
    
