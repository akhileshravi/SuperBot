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

#Colours
BLACK = (0,0,0) # Ak
GREEN = (0,255,0) # Ak

angle = 30      # Angle for rotation

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
spimg = pygame.image.load(supermanimg).convert() # Normal
spUpimg = pygame.image.load(supermanimg).convert() # Move Up
spDownimg = pygame.image.load(supermanimg).convert() # Move Down
#sp2img = pygame.image.load(supermanslantimg).convert()

spUpimg = pygame.transform.rotate(spUpimg, angle) 
spDownimg = pygame.transform.rotate(spDownimg, -angle) 



#Classes
class MainChar(pygame.sprite.Sprite):

    flightstate = False
    alive = True
    
    def __init__(self):
        
        pygame.sprite.Sprite.__init__(self)
 
        self.image = spimg
        self.rect = self.image.get_rect()
        self.rect.x = 100 # Initially it was 30
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
dy = fy = 0

yabs = skheight+superman.rect.y-1     #starting height of platforms (mean of Gaussian Distribution)
sigma = 150 #Standard deviation for the Gaussian distribution of platforms

clock = pygame.time.Clock()

for i in range(10):
    platform = Plat(i*pwidth, skheight+superman.rect.y-1)
    splist.add(platform)
    
st = time.time()

fsj = False

#Flying 
flybar = 0.0      # Show how much fly you have left
maxflytime = 1.5    # Fly Key is f
flyflag = False # To check whether superman is flying
prevflytime = time.time()
flydivconst = 2.0 # The flybar will get charged at 1/flydivconst times the
                    # speed with fly gets used up

#Flybar Rectangle  # Ak
fl_x = 20
fl_y = 20
flwidth = 200
flheight = 20

jump = 0

while True:

    
    scr.blit(background,(0,0))
    splist.draw(scr)
    scr.blit(superman.image, (superman.rect.x,superman.rect.y))

    
    

    # Fly Bar Code Starts   # Ak
    # Ak - Checking how long superman can fly
    flybarfraction = flybar/maxflytime ###
    if flybarfraction > 1:
        flybarfraction = 1
    elif flybarfraction < 0:
        flybarfraction = 0
    pygame.draw.polygon(scr, BLACK, ((fl_x, fl_y),
            (fl_x + flwidth, fl_y), (fl_x + flwidth, fl_y + flheight),
            (fl_x, fl_y + flheight)))
    
    
    greenwidth = int((flwidth-4) * flybarfraction)
    pygame.draw.polygon(scr, GREEN, ((fl_x + 2, fl_y + 1),
            (fl_x + greenwidth + 2, fl_y), (fl_x + greenwidth + 2, fl_y + flheight - 1),
            (fl_x + 2, fl_y + flheight - 1)))

    


    pygame.display.update()

    

    if not flyflag:
        if flybar < maxflytime: 
            flybar += 1.0/(fps * flydivconst)
            
        else:
            flybar = maxflytime
        
    

    if flyflag:
        if jump == 0:
            jump = 1
            
        if flybar <= 0:
            flybar = 0
            flyflag = False
            dy = -2
            prevflytime = time.time()
        else:
            flybar -= 1.0/(fps)

    #Fly Bar Code Ends Here   # Ak
        
    
    
    if dy == 2 and time.time()-uptime >= 0.8:
        
        #superman.image = pygame.transform.rotate(superman.image, -2*angle)   #  Clockwise
        superman.image = spDownimg  
        dy = -2
        uptime = 0


    if dy != 2 and not(flyflag):

        
        dy = -2
        superman.image = spDownimg
        for i in Plat.plist:
    
            if i.rect.x-skwidth-6 <= superman.rect.x <= (i.rect.x+pwidth+6) and -3<i.rect.y -(superman.rect.y+skheight)<3 :

                dy = 0
                jump = 0
                flyflag = False
                fsj = False
                
                superman.image = spimg  # To change images while moving straight, moving up and moving down 
                ###### #superman.image = pygame.transform.rotate(superman.image, angle)   # Ak - AntiClockwise
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
                if (dy == 0 or fsj) and jump < 2: 
                    dy = 2
                    jump += 1    
                    uptime = time.time()
                    fsj = not(fsj)
                    #superman.image = pygame.transform.rotate(superman.image, angle)   # Ak - AntiClockwise
                    superman.image = spUpimg  # Moving Up

                elif (dy == -2 or fsj) and jump < 2: 
                    dy = 2
                    jump = 2
                    uptime = time.time()
                    fsj = not(fsj)
                    #superman.image = pygame.transform.rotate(superman.image, angle)   # Ak - AntiClockwise
                    superman.image = spUpimg  # Moving Up
            
            elif event.key in [K_q,K_ESCAPE]:
                pygame.quit()
                sys.exit()

            elif event.key in (K_f,) and flybar > 0:    # I thought (K_f, K_F)
                dy = 0
##                if not flyflag:     # Ak - Checking how long superman can fly
##                    flybar = (time.time() - prevflytime)/flydivconst #+ flyrem
##                    if flybar > maxflytime:
##                        flybar = maxflytime
                flyflag = True
                startflytime = time.time()
                superman.image = spimg  # Ak - Changing it back to the normal image

        if event.type == KEYUP:
            if flyflag:
                dy = -2
                flyflag = False     # Ak
                superman.image = spDownimg
                #flyrem = flybar
                
        if event.type == MOUSEBUTTONDOWN:
            if dy == 0 and jump < 2:
                dy = 2
                jump += 1
                uptime = time.time()
                superman.image = spUpimg
                #superman.image = pygame.transform.rotate(superman.image, angle)   # Ak - AntiClockwise
                

            elif dy == -2 and jump < 2:
                dy = 2
                jump = 2
                uptime = time.time()
                superman.image = spUpimg
                #superman.image = pygame.transform.rotate(superman.image, angle)   # Ak - AntiClockwise
            

        #print event,flyflag
    clock.tick(fps)
    
