import pygame,sys
import time, random

from pygame.locals import *

pygame.init()


scrwidth = 640
scrheight = 360
scr = pygame.display.set_mode((scrwidth,scrheight),0,32)
                    

pwidth = 150          #sizes of the images
pheight = 40

skwidth = 100        
skheight = 45

angle = 30      

flytime = 3   


#better to have pics which require high resolution in jpg
#pics which are small in size/res can be in png instead
back = "back.jpg"
cursorimg = "cursorimg.png"
dot = "dot.jpg"
platimg = "platform2.png"
supermanimg = "superman2.jpg" 
#supermanslantimg = "superman2.jpg" # for 'jumping'


#must convert images to use in pygame

background = pygame.image.load(back).convert()
mscursor = pygame.image.load(cursorimg).convert_alpha()
dot = pygame.image.load(dot).convert_alpha()
platimg = pygame.image.load(platimg).convert_alpha()
spimg = pygame.image.load(supermanimg).convert() 
spUpimg = pygame.image.load(supermanimg).convert() # Ak
spDownimg = pygame.image.load(supermanimg).convert() # Ak
#sp2img = pygame.image.load(supermanslantimg).convert()

spUpimg = pygame.transform.rotate(spUpimg, angle) # Ak
spDownimg = pygame.transform.rotate(spDownimg, -angle) # Ak



#Classes
class MainChar(pygame.sprite.Sprite):

    flightstate = False
    alive = True
    
    def __init__(self):
        
        pygame.sprite.Sprite.__init__(self)
 
        self.image = spimg
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
superman = MainChar()
splist = pygame.sprite.Group()
splist.add(superman)


fps = 60

dx = -5
dy = 0

yabs = skheight+superman.rect.y-1     #starting height of platforms (mean of Gaussian Distribution)
sigma = 150 #Standard deviation for the Gaussian distribution of platforms

clock = pygame.time.Clock()

for i in range(10):
    platform = Plat(i*pwidth, skheight+superman.rect.y-1)
    splist.add(platform)
    
st = time.time()

fsj = False

jump = 0
flyflag = False 

while True:

    
    scr.blit(background,(0,0))
    splist.draw(scr)
    scr.blit(superman.image, (superman.rect.x,superman.rect.y))

    
    pygame.display.update()


    if dy == 2 and time.time()-uptime >= 0.8:
        
        #superman.image = pygame.transform.rotate(superman.image, -2*angle)   # Ak Clockwise
        superman.image = spDownimg  # Ak
        dy = -2
        uptime = 0


    if dy != 2:

        
        dy = -2
        for i in Plat.plist:
    
            if i.rect.x-skwidth-6 <= superman.rect.x <= (i.rect.x+pwidth+6) and -3<i.rect.y -(superman.rect.y+skheight)<3 :

                dy = 0
                jump = 0    
                fsj = False
                
                superman.image = spimg  # Ak
                ###### #superman.image = pygame.transform.rotate(superman.image, angle)   # Ak - AntiClockwise
                break
        


    yabs += dy
    for i in Plat.plist:
        i.update(dx,dy)

    if len(Plat.plist) < 4:
        Platgen(yabs, sigma)


    if flyflag:     
        dy -=3
        flyflag = False
        
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if (dy == 0 or fsj) and jump < 2:
                    dy = 2
                    jump += 1    
                    uptime = time.time()
                    fsj = not(fsj)
                    #superman.image = pygame.transform.rotate(superman.image, angle)   # Ak - AntiClockwise
                    superman.image = spUpimg  

                elif (dy == -2 or fsj) and jump < 2: 
                    dy = 2
                    jump = 2    
                    uptime = time.time()
                    fsj = not(fsj)
                    #superman.image = pygame.transform.rotate(superman.image, angle)   # Ak - AntiClockwise
                    superman.image = spUpimg  # Ak
            
            elif event.key in [K_q,K_ESCAPE]:
                pygame.quit()
                sys.exit()

            elif event.key in (K_f,):    
                dy += 3
                flyflag = True
                
                
                
        if event.type == MOUSEBUTTONDOWN:
            if dy == 0 and jump < 2:  
                dy = 2
                jump += 1
                uptime = time.time()
                #superman.image = pygame.transform.rotate(superman.image, angle)   # Ak - AntiClockwise
                

            elif dy == -2 and jump < 2:  
                dy = 2
                jump = 2
                uptime = time.time()
                #superman.image = pygame.transform.rotate(superman.image, angle)   # Ak - AntiClockwise
            

        
    clock.tick(fps)
    
