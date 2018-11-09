import pygame,sys,time
from pygame.locals import *

pygame.init()



scr = pygame.display.set_mode((640,360),0,32)
                    #screen size,state,no. of bits for colours

#better to have pics which require high resolution in jpg
#pics which are small in size/res can be in png instead
back = "back.jpg"
cursorimg = "cursorimg.png"
dot = "dot.jpg"
plat = "platform.png"
skater = "skater.jpg"


#must convert images to use in pygame

background = pygame.image.load(back).convert()
mscursor = pygame.image.load(cursorimg).convert_alpha()
dot = pygame.image.load(dot).convert_alpha()
plat = pygame.image.load(plat).convert_alpha()
skater = pygame.image.load(skater).convert()




#Classes
class MainChar(pygame.sprite.Sprite):

    flightstate = False
    alive = True
    
    def __init__(self, color, width, height):
        
        pygame.sprite.Sprite.__init__(self)
 
        self.image = skater
        self.rect = self.image.get_rect()

        




fps = 40
dx = dy = x = y = 0
px = 640
py = 100
dpx =-1

clock = pygame.time.Clock()


cursorstate = False #whether cursor visible or not


st = time.time()
while True:

    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_LEFT or event.key==K_a:
                dx=-1
            if event.key == K_RIGHT or event.key==K_d:
                dx=1
            if event.key==K_UP or event.key==K_w:
                dy=-1
            if event.key==K_DOWN or event.key==K_s:
                dy=1
            if event.key in [K_q,K_ESCAPE]:
                pygame.quit()
                sys.exit()

                
        if event.type==KEYUP:
            if event.key==K_LEFT or event.key==K_a:
                dx=0
            if event.key==K_RIGHT or event.key==K_d:
                dx=0
            if event.key==K_UP or event.key==K_w:
                dy=0
            if event.key==K_DOWN or event.key==K_s:
                dy=0


        if event.type==MOUSEBUTTONDOWN:
            cursorstate=not(cursorstate)
            px=640

        
            
        #print event,event.type
            
            
    
    scr.blit(background,(0,0))

    cx,cy = pygame.mouse.get_pos()
    cx -=mscursor.get_width()/2
    cy -=mscursor.get_height()/2
    x+=dx
    y+=dy
    px+=dpx
    if px<0:
        cursorstate=False

    if x<0:         #this block is to ensure dot stays on screen
        x=640
    elif x>640:
        x=0
    if y<0:
        y=360
    elif y>360:
        y=0
    
    
    scr.blit(dot,(x,y))
    #blit is to display an image
    #blit(imagename,xcentre,ycentre)
    
    if cursorstate:
        scr.blit(mscursor,(cx,cy))
         
        scr.blit(plat,(px,py))
        
        
    
    pygame.display.update()

    clock.tick(fps)

    
