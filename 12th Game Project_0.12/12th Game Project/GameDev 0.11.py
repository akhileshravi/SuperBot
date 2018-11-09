import pygame,sys
import time, random

from pygame.locals import *

pygame.init()


scrwidth = 640
scrheight = 360
scr = pygame.display.set_mode((scrwidth,scrheight),0,32)
                    

pwidth = 150          #sizes of the images
pheight = 40

skwidth = 80       
skheight = 36   

#Colours
BLACK = (0,0,0)
GREEN = (0,255,0)

angle = 30      # Angle for rotation

#better to have pics which require high resolution in jpg
#pics which are small in size/res can be in png instead
back = "back.jpg"
cursorimg = "cursorimg.png"
dot = "dot.jpg"
platimg = "platform2.png"
supermanimg = "superman3.jpg"
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



up = 'up'
centre = 'centre'
down = 'down'



#Classes
class MainChar(pygame.sprite.Sprite):

    flightstate = False
    alive = True
    
    def __init__(self):
        
        pygame.sprite.Sprite.__init__(self)
 
        self.image = spimg
        self.rect = self.image.get_rect()
        self.rect.x = 100  # Initially it was 30
        self.rect.y = ((scrheight + 20 )/2) - skheight
        self.true_y = 0

    def update(self,dsy):
        
        self.true_y += dsy


        



class Plat(pygame.sprite.Sprite):


    pos = [up, centre, down]
    plist = {up : [], centre : [], down : []}
    pyabs = {up : -200, centre : 0, down : 200}
    endcoor = {up : 0, centre : 0, down : 0} # The ending x-coordinate of the last platform
    height_flag = {up : False, centre : False, down : False}
            # This determines whether the blocks added continuously
            # are added at the same height

    def __init__(self,px,py,position):


        pygame.sprite.Sprite.__init__(self) 
        self.image = platimg
        self.rect = self.image.get_rect()
        self.rect.x = px
        self.rect.y = py
        Plat.plist[position] += [self]
        Plat.endcoor[position] = px + pwidth        # This gives the ending 
                                    # x-coordinate of the last added platform

    def update(self,dpx,dpy):

        self.rect.x += dpx
        self.rect.y += dpy

        for position in Plat.plist:
            
            if self in Plat.plist[position] and self.rect.x < -(pwidth) :

                Plat.plist[position].remove(self)
                splist.remove(self)
                del self
                break
            

    def __del__(self):
        pass

class Water(pygame.sprite.Sprite):

    
    def __init__(self):
        self.start_x = 0
        self.start_y = scrheight           
    

#New form of Platgen function
def Platgen(yabs, sigma,position):

    global Plat

    # plat_num is a list that contins the values - 1,2,3 with
    # different frequencies.
    
    num = random.choice(plat_num)   # num determines the number of plates
    # that will be added continuously in one go
    
    if random.choice(existlist):
        # Here, the plates are added continuously at the same height
        
        fixed_height = random.gauss( yabs + Plat.pyabs[position] - 30, sigma)
        for i in range(num):
            platform = Plat( scrwidth + i*pwidth , fixed_height, position)
            splist.add(platform)
        Plat.height_flag[position] = True
        # Here, height_flag is True. Thus, more plates will be added
        # after leaving some space. Otherwise it becomes inconvenient.
        

    else:
        # Here, the plates are added continuously at different heights
        
        for i in range(num):
            platform = Plat( scrwidth + i*pwidth , random.gauss( yabs + Plat.pyabs[position]- 30, sigma), position)
            splist.add(platform)
        Plat.height_flag[position] = False
        # Here, height_flag is False. Thus, more plates can be added
        # immediately.

def quitter():
    pass
                    


#Data Definitions
superman = MainChar()
splist = pygame.sprite.Group()
splist.add(superman)


fps = 60

dx = -5
dy = fy = 0

yabs = skheight+superman.rect.y-1     #starting height of platforms (mean of Gaussian Distribution)
sigma = 20 #Standard deviation for the Gaussian distribution of platforms
# sigma was initially 150

clock = pygame.time.Clock()

for i in range(10):
    for position in Plat.pos:
        platform = Plat(i*pwidth, skheight+superman.rect.y-1, position)
        splist.add(platform)
    
st = time.time()

fsj = False


#Platform variables
existlist = [0 for i in range(13)] + [1 for i in range(3)] # This is used to
                            #determine whether a plate should be added or not

gap_length = {up : 0, centre : 0, down : 0}
                    # if a plate is not added, then gap_length is added
                    # to endcoor (ending coordinate), so, there will be some
                    # space before the next plate is added
                    
plat_num = [1 for i in range(11)] + [2 for i in range(5)] + [3 for i in range(2)]
        # This has the values for the number of plates that should be added
        # continuously in one go
        
last_platform = {}  # Stores the last platform of each level


#Flying 
flybar = 0.0      # Show how much fly you have left
maxflytime = 2.0    # Fly Key is f
flyflag = False # To check whether superman is flying
prevflytime = time.time()
flydivconst = 3.0 # The flybar will get charged at 1/flydivconst times the
                    # speed with fly gets used up

#Flybar Rectangle
fl_x = 20
fl_y = 20
flwidth = 200
flheight = 20

jump = 0

score = 0
dist = 0
coincount = 0
coinscore = 500

while True:

    
    scr.blit(background,(0,0))
    splist.draw(scr)
    scr.blit(superman.image, (superman.rect.x,superman.rect.y))


    font1 = pygame.font.SysFont('Arial', 18)
    font2 = pygame.font.SysFont('Arial', 20)
    font3 = pygame.font.SysFont('Arial', 18)
    dist += abs(dx)
    if coincount:
        score += (abs(dx))**1.2 * (coincount)*coinscore
    else:
        score += (abs(dx))**1.2

    # Fly Bar Code Starts
    # Checking how long superman can fly
    flybarfraction = flybar/maxflytime
    if flybarfraction > 1:
        flybarfraction = 1
    elif flybarfraction < 0:
        flybarfraction = 0
    pygame.draw.polygon(scr, BLACK, ((fl_x, fl_y),
            (fl_x + flwidth, fl_y), (fl_x + flwidth, fl_y + flheight),
            (fl_x, fl_y + flheight)))
    scr.blit(font2.render('STAMINA', True, (255,255,255)), (fl_x+flwidth/4, fl_y))
    
    
    
    greenwidth = int((flwidth-4) * flybarfraction)
    pygame.draw.polygon(scr, GREEN, ((fl_x + 2, fl_y + 1),
            (fl_x + greenwidth + 2, fl_y), (fl_x + greenwidth + 2, fl_y + flheight - 1),
            (fl_x + 2, fl_y + flheight - 1)))

    
    
    scr.blit(font2.render('SCORE: ', True, (255,0,0)), (scrwidth - 150, 20))
    scr.blit(font1.render(str(int(score)), True, (255,0,0)), (scrwidth - 150 + 80, 22)) ###

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

    #Fly Bar Code Ends Here
        
    
    
    if dy == 2 and time.time()-uptime >= 0.8:
        
        superman.image = spDownimg  
        dy = -2
        uptime = 0


    if dy != 2 and not(flyflag):

        
        dy = -2
        superman.image = spDownimg
        for a in Plat.plist:

            for i in Plat.plist[a]:
    
                if i.rect.x-skwidth-6 <= superman.rect.x <= (i.rect.x+pwidth+6) and -3<i.rect.y -(superman.rect.y+skheight)<3 :

                    dy = 0
                    jump = 0
                    flyflag = False
                    fsj = False
                    
                    superman.image = spimg  # To change images while moving straight, moving up and moving down
                    break
        


    yabs += dy
    for i in Plat.plist:
        for j in Plat.plist[i]:
            j.update(dx,dy)

    superman.update(dy)


    # New code
    for position in Plat.pos:
        #last_platform[position] = Plat.plist[position][-1]
        last_platform = Plat.plist[position][-1]
        Plat.endcoor[position] = last_platform.rect.x + pwidth + gap_length[position]
                    # gap_length is added if a gap should be inserted
                    
        if Plat.endcoor[position] - scrwidth <= 0:
            
            if random.choice(existlist) and not Plat.height_flag[position]:
                # In this case, platform(s) will be added
                
                Platgen(yabs, sigma, position)
                gap_length[position] = 0

            else:
                # In this case, gap(s) will be added
            
                gap_length[position] = pwidth * random.choice(plat_num)
                if Plat.height_flag[position] == True:
                    Plat.height_flag[position] = False

        


        
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
                    superman.image = spUpimg  # Moving Up

                elif (dy == -2 or fsj) and jump < 2: 
                    dy = 2
                    jump = 2
                    uptime = time.time()
                    fsj = not(fsj)
                    superman.image = spUpimg  # Moving Up
            
            elif event.key in [K_q,K_ESCAPE]:
                pygame.quit()
                sys.exit()

            elif event.key in (K_f,) and flybar > 0:    # I thought (K_f, K_F)
                dy = 0
                flyflag = True
                startflytime = time.time()
                superman.image = spimg  # Changing it back to the normal image

        if event.type == KEYUP:
            if flyflag:
                dy = -2
                flyflag = False    
                superman.image = spDownimg
                
                
        if event.type == MOUSEBUTTONDOWN:
            if dy == 0 and jump < 2:
                dy = 2
                jump += 1
                uptime = time.time()
                superman.image = spUpimg
                

            elif dy == -2 and jump < 2:
                dy = 2
                jump = 2
                uptime = time.time()
                superman.image = spUpimg
                
            

        
    clock.tick(fps)
    
