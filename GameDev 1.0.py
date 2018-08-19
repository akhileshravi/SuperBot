"""
           SUPERBOT
Class 12 Computer Science Project     """


import pygame,sys
import time, random

from pygame.locals import *

pygame.init()


"""Initial definitions of global varibales for screen setup and images of each object"""

scrwidth = 640
scrheight = 360
scr = pygame.display.set_mode((scrwidth,scrheight),0,32)                 

pwidth = 150          #sizes of the platform images
pheight = 40

cwidth = 20           #sizes of the coin images
cheight = 20

skwidth = 80       
skheight = 36   

#Colours
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)
WHITE = (255,255,255)
MENUCL = (0,0,0)



#better to have pics which require high resolution in jpg
#pics which are small in size/res can be in png instead
back = "backt.jpg"
back1 = "back3.jpg"

platimg = "platform2t.png"
supermanimg = "superman2t.png"
supermanupimg = "supermanupt.png"
supermandownimg = "supermandownt.png"

inst = "Instructions.png"
sto = "Story.png"

coin1 = "coin1.png"
coin10 = "coin10.png"
coin5 = "coin5.png"



lavaimg = "lava.png"
#supermanslantimg = "superman2.jpg" # for 'jumping'


#must convert images to use in pygame
spimg = pygame.image.load(supermanimg).convert_alpha() # Normal
spUpimg = pygame.image.load(supermanimg).convert_alpha() # Move Up
spDownimg = pygame.image.load(supermanimg).convert_alpha() # Move Down

corner = spimg.get_at((0, 0))
spimg.set_colorkey(corner, RLEACCEL)

angle = 5
spUpimg = pygame.transform.rotate(spUpimg, angle)
spDownimg = pygame.transform.rotate(spDownimg, -angle)

corner = spUpimg.get_at((0, 0))
spUpimg.set_colorkey(corner, RLEACCEL)

corner = spDownimg.get_at((0, 0))
spDownimg.set_colorkey(corner, RLEACCEL)

coin1 = pygame.image.load(coin1).convert_alpha()
coin10 = pygame.image.load(coin10).convert_alpha()
coin5 = pygame.image.load(coin5).convert_alpha()
corner = coin1.get_at((0, 0))
coin1.set_colorkey(corner, RLEACCEL)
corner = coin10.get_at((0, 0))
coin10.set_colorkey(corner, RLEACCEL)
corner = coin5.get_at((0, 0))
coin5.set_colorkey(corner, RLEACCEL)

instr = pygame.image.load(inst).convert()
story = pygame.image.load(sto).convert()

background = pygame.image.load(back).convert()
background1 = pygame.image.load(back1).convert()
platimg = pygame.image.load(platimg).convert_alpha()

lava = pygame.image.load(lavaimg).convert_alpha()
#sp2img = pygame.image.load(supermanslantimg).convert()



#Font Defintions
up = 'up'
centre = 'centre'
down = 'down'
font1 = pygame.font.SysFont('Arial', 18)
font2 = pygame.font.SysFont('Arial', 20)
font2.set_bold(True)
font3 = pygame.font.SysFont('Arial', 40)
font4 = pygame.font.SysFont('Arial', 28)
font5 = pygame.font.SysFont('Arial', 18)
font6 = pygame.font.SysFont('Algerian', 32)
font6b = pygame.font.SysFont('Algerian', 26)

font7 = pygame.font.SysFont('Rockwell', 44)
font8 = pygame.font.SysFont('Monaco', 34)
font9 = pygame.font.SysFont('Monaco', 28)
font10 = pygame.font.SysFont('Arial', 28)
font10.set_bold(True)

studio_red, studio_green, studio_blue = 135,201,233
game_red, game_green, game_blue = 203, 236, 19

linewidth = 10




#Class Definitions

class MainChar(pygame.sprite.Sprite): 
    """ Class MainChar determines the behavior and properties of Superman

    Retrieves Image for Superman and derives from Sprite Class to check for collisions"""


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

    def x_y(self,sx, sy):
        
        self.rect.x = sx
        self.rect.y = sy

    def dx_dy(self,dsx, dsy):
        
        self.rect.x += dsx
        self.rect.x += dsy
    

    def default(self):
        self.image = spimg
        self.rect = self.image.get_rect()
        self.rect.x = 100  # Initially it was 30
        self.rect.y = ((scrheight + 20 )/2) - skheight 
        self.true_y = 0
        


class Coins(pygame.sprite.Sprite):
    
    """Class Coins for coin objects and the functions, movement

    and values of coins in the game. Derived from Sprite Class to detect collisions"""

    clist = []
    sound = pygame.mixer.Sound('coin1.wav')
    ctime = time.time()
    rt = 8      # time for second coin after first

    def __init__(self,px,py,n):

        pygame.sprite.Sprite.__init__(self)

        if n == 1:
            self.image = coin1
            self.type = 1
        elif n == 5:
            self.image = coin5
            self.type = 5

        elif n == 10:
            self.image = coin10
            self.type = 10


        pygame.sprite.Sprite.__init__(self)
        
        self.rect = self.image.get_rect()
        self.rect.x = px
        self.rect.y = py
        

    def update(self,dpx,dpy):

        self.rect.x += dpx
        self.rect.y += dpy

        if self in Coins.clist and self.rect.x < -(cwidth) :

            Coins.clist.remove(self)
            splist.remove(self)
            del self

    @staticmethod
    def generate():
        r1 = [1,2,2,3,3,3,4,4,4,5,5,5,5,6,6,6,5,5,8,8,8,8,10,12,12] 
        r2 = [1]*4+[5]
        rt = random.choice(r1)
        
        Coins.rt = random.choice(r1)
        Coins.ctime = time.time()
        gen = False

        while not(gen):

            ycoin = yabs + random.randint(-100,100)
            c = Coins(scrwidth+30, ycoin, random.choice(r2))
            gen = Coins.checkcollide(c)

        Coins.clist += [c]              

    @staticmethod
    def checkcollide(c):
        splist.add(c)
        for i in Plat.plist:
            for j in Plat.plist[i]:
                if pygame.sprite.collide_rect(c, j):
                    splist.remove(c)
                    return False
        return True
                            
                        
            
            
                                   



class Plat(pygame.sprite.Sprite):
    
    """ Class Plat for all platform objects and controls movement and image blitted"""

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

############################################################################
    
#User Defined Functions


def Platgen(yabs, sigma,position):
    
    """Generates the each of the platforms at one position and accepts location variables"""

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


def quitter(score):
    
    """Function to handle the quitting of game and calls for highscore and displaying it"""

    global alive
    alive = False

    txt1 = font3.render('YOU DIED!', True, WHITE)
    txt2 = font1.render('Click to continue', True, WHITE)
    txt3 = font1.render('Your score is: ' + str(int(score)), True, WHITE)
    scr.blit(txt1, ((scrwidth-txt1.get_width())/2, int(scrheight/2.5)))
    scr.blit(txt2, ((scrwidth-txt2.get_width())/2, int(scrheight/2.5)+70))
    scr.blit(txt3, ((scrwidth-txt3.get_width())/2, int(scrheight/2.5+145)))

    
    flag = True
    while flag:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                scr.blit(background,(0,0))
                hscore(score)
                dispscore()
                flag = False
                break
            
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    scr.blit(background,(0,0))
                    hscore(score)
                    dispscore()
                    flag = False
                    break
                
        pygame.display.update()


def bi(n):
    
    """Converts decimal number n to binary equivalent"""
    
    b,p=0,1
    while n>0:
        m=n%2
        b+=m*p
        p*=10
        n//=2
    return b

def hscore(n):
    
    """Checks if new highscore is applicable, writes over
    Checks for Errors and tampering by external sources as well"""

    n = int(n)
    
    while True:
        
        try:
            b = db = vc = hsr = 0
            f = open("HScore.bin","rb")
            d = f.read()
            f.close()
            if d == "#\#001":
                b = hsr =001
                db = 1
            else:
                dec,last = 0,0
                for i in range(len(d)):
                    if d[i:i+3] == "#\#":
                        dec += 1
                        last = i
                for i in range(len(d)):
                    if 47<ord(d[i])<58 and db == 1 and vc == 1:
                        hsr = hsr*10+int(d[i])
                    if 47<ord(d[i])<58 and db == dec and vc == 1:
                        b = b*10+int(d[i])
                    elif d[i:i+3] == "#\#":
                        db += 1
                        vc = 0
                    elif d[i:i+2]=="AF":
                        vc = 1
            if (int(str(b//100),2)%9999999967) != 0 or (int(str(hsr//100),2)%9999999967)!=0:
                raise ValueError("Tampered file!")
            s = (int(str(b//100),2)/9999999967)
      
            
            if (n >= s or dec < 5) and n!=0:
                

                nam = getname()

                tnam = "F/"
                for i in nam:
                    tnam = tnam+str(bi(ord(i)*137))+"/"
                nam = tnam+"AF"
                if db == 1 and s == 0:
                    f = open("HScore.bin","wb")
                    f.write("#\#"+nam+"//"+str(bi(n*9999999967)*100+len(str(n))))
                    f.close()
                else:
                    f = open("HScore.bin","rb")
                    d = f.read()
                    f.close()
                    j = flag = i = 0
                    while i <len(d):
                        if d[i:i+3] == "#\#":
                            j = i
                            dec = ""    
                        if d[i:i+4] == "AF//":
                            i += 4
                            while (d[i:i+3]!="#\#" and i<len(d)):
                                dec += d[i]
                                i += 1
                            dec = int(dec)
                            i -= 1
                            if (int(str(dec//100),2)/9999999967)<n:
                                flag = 1
                                break
                        i += 1
                    if db == 5:
                        d = d[:last]
                    f = open('HScore.bin',"wb")
                    if flag:
                        f.write(d[:j]+"#\#"+nam+"//"+str(bi(n*9999999967)*100+len(str(n)))+d[j:])
                    else:
                        f.write(d+"#\#"+nam+"//"+str(bi(n*9999999967)*100+len(str(n))))
                    f.close()
                
            else:
                scr.blit(font4.render('High score:' + str(int(str(hsr//100),2)/9999999967), True, (255,255,255)), (scrwidth//2.5-50, int(scrheight/2.5)+55))
            break

        except:
            f = open("HScore.bin","wb")
            f.write("#\#001")
            f.close()


def dispscore1():
    
    """Function for simple viewing of highscores only
    Also checks for tampering from external sources"""
    

    while True:
        try:
            f = open('HScore.bin',"rb")
            d = f.read()
            f.close()
            break
        except:
            f = open("HScore.bin","wb")
            f.write("#\#001")
            f.close    
    i = 0
    scr.blit(background,(0,0))
    sl=0
    linespace = 40
    scrwidth = 640
    scrheight = 360
    if d == "#\#001":
        
        scr.blit(font4.render("No Scores Yet On This Device", True, (255,255,255)), (scrwidth//2.5-80, int(scrheight/2.5)))
        sl = 3
    else: 
        
        l = []
        size = sznstr = 0
        
        while i < len(d):

            if d[i] == "#":
                sl += 1
                nstr = b = ""
                i += 5
                while d[i] != "A":
                    while d[i].isdigit():
                        b += d[i]
                        i += 1
                    nstr += chr(int(b,2)/137)
                    i += 1
                    b = ''
                i += 4
                while i < len(d):
                    b += d[i]
                    if i+1==len(d) or d[i] == "#":
                        b = b[:-3]
                        i-=2
                        break
                    i+=1
                b = int(b,2)/9999999967
                if i == len(d) -3:
                    b *= 2
                l += [[sl , nstr , b]]

                  
                txt1 = font4.render(str(sl)+nstr + str(b), True, (255,255,255))
                if size < sznstr:
                    sznstr = font4.render(nstr, True, (255,255,255)).get_width()
                    size = sznstr
                txt2 = font4.render(str(sl)+nstr + str(b), True, (255,255,255))
                if size < txt1.get_width():
                    size = txt1.get_width()+3
                    sznstr = font4.render(nstr, True, (255,255,255)).get_width()
                centre = scrwidth//2
                if i == len(d) -3:
                    for j in l:
                        if j[0] == 1:
                            
                            txt1 = font4.render("SL No.", True, (255,255,255))
                            txt2 = font4.render("NAME", True, (255,255,255))
                            txt3 = font4.render("SCORE", True, (255,255,255))
                            half = sznstr//2
                            nsx = (centre - half)+(sznstr-txt2.get_width())/2
                            scr.blit(txt1, (nsx-90, int(scrheight/4.5)-20)) 
                            scr.blit(txt2, (((nsx+10, int(scrheight/4.5)-20))))
                            scr.blit(txt3, (nsx+half+60, int(scrheight/4.5)-20))
                          
                    
                        txt4 = font4.render(str(j[0]), True, (255,255,255))
                        txt5 = font4.render(j[1], True, (255,255,255))
                        txt6 = font4.render(str(j[2]), True, (255,255,255))
                        half = (txt5.get_width())//2
                        nsx = (centre - half)+(sznstr-txt5.get_width())/2
                        scr.blit(txt4, (nsx-58, int(scrheight/4.5)+j[0]*linespace-15)) 
                        scr.blit(txt5, (nsx, int(scrheight/4.5)+j[0]*linespace-15)) 
                        scr.blit(txt6, (nsx+half+80, int(scrheight/4.5)+j[0]*linespace-15))
                
            i += 1
        
    scr.blit(font1.render('Click to continue', True, WHITE), (scrwidth//2.5+23, int(scrheight/4.5)+(sl+1)*(linespace)))

    pygame.display.update()
    flag = True
    while flag:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                flag = False
                break
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    flag = False
                    break

def dispscore():
    
    """Function for simple viewing of highscores only
    Also checks for tampering from external sources"""
    

    while True:
        try:
            f = open('HScore.bin',"rb")
            d = f.read()
            f.close()
            break
        except:
            f = open("HScore.bin","wb")
            f.write("#\#001")
            f.close    
    i = 0
    scr.blit(background,(0,0))
    sl=0
    linespace = 40
    scrwidth = 640
    scrheight = 360
    if d == "#\#001":
        
        scr.blit(font4.render("No Scores Yet On This Device", True, (255,255,255)), (scrwidth//2.5-80, int(scrheight/2.5)))
        sl = 3
    else: 
        l1,l2 = ["NAME"], ["SCORE"]
        l = [["SL No.","NAME","SCORE"]]
        size = sznstr = 0
        
        while i < len(d):

            if d[i] == "#":
                sl += 1
                nstr = b = ""
                i += 5
                while d[i] != "A":
                    while d[i].isdigit():
                        b += d[i]
                        i += 1
                    nstr += chr(int(b,2)/137)
                    i += 1
                    b = ''
                i += 4
                while i < len(d):
                    b += d[i]
                    if i+1==len(d) or d[i] == "#":
                        b = b[:-3]
                        i-=2
                        break
                    i+=1
                b = int(b,2)/9999999967
                if i == len(d) -3:
                    b *= 2
                l += [[sl , nstr , b]]
                l1 += [nstr]
                l2 += [str(b)]
            i += 1
            
        centre = scrwidth//2
        bsx = bnx = 0
        for i in range(len(l1)):
            if font4.render(l2[i], True, (255,255,255)).get_width() > bsx:
                bsx = font4.render(l2[i], True, (255,255,255)).get_width()
                
            if font4.render(l1[i], True, (255,255,255)).get_width() > bnx:
                bnx = font4.render(l1[i], True, (255,255,255)).get_width()
                
        halfn = bnx/2
        halfs = bsx/2
        
        for j in l:
            if j[0] == "SL No.":
                
                txt1 = font10.render("SL No.", True, (255,255,255))
                txt2 = font10.render("NAME", True, (255,255,255))
                txt3 = font10.render("SCORE", True, (255,255,255))
                
                nsx = centre - halfn
                cn = (bnx-txt2.get_width())/2
                nnx = centre +halfn
                cs = (bsx-txt3.get_width())/2
                scr.blit(txt1, (nsx-110, int(scrheight/4.5)-20)) 
                scr.blit(txt2, (((nsx + cn, int(scrheight/4.5)-20))))
                scr.blit(txt3, (nnx+cs+50, int(scrheight/4.5)-20))
                continue
              
        
            txt4 = font4.render(str(j[0])+".", True, (255,255,255))
            txt5 = font4.render(j[1], True, (255,255,255))
            txt6 = font4.render(str(j[2]), True, (255,255,255))
            nsx = centre - halfn
            cn = (bnx-txt5.get_width())/2
            nnx = centre + halfn
            cs = (bsx-txt6.get_width())/2
            scr.blit(txt4, (nsx-80, int(scrheight/4.5)+j[0]*linespace-15)) 
            scr.blit(txt5, (nsx+cn, int(scrheight/4.5)+j[0]*linespace-15)) 
            scr.blit(txt6, (nnx+cs+53, int(scrheight/4.5)+j[0]*linespace-15))
        
    scr.blit(font1.render('Click to continue', True, WHITE), (scrwidth//2.5+23, int(scrheight/4.5)+(sl+1)*(linespace)))

    pygame.display.update()
    flag = True
    while flag:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                flag = False
                break
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    flag = False
                    break

  

def getname():
    
    """Function to retreive name from pygame window with input inside a box"""

    nstr = key = ''
    blink = ["|"," "]
    bl = 0
    blt = time.time() 
    
    while True:
        txt = font4.render(nstr + blink[bl], 1, (255,255,255))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                key =  event.key
                
                if key == K_RETURN:
                    return nstr

                elif key == K_BACKSPACE:
                    nstr = nstr[:-1]
                    
                elif key<=127:
                    twidth = txt.get_width()
                    if twidth < 224:
                        nstr += chr(key)
                    else:
                        nstr = nstr[:-1] + chr(key)
        if time.time() - blt > 0.4 :
            bl += 1
            bl %= 2
            blt = time.time()
        txt = font4.render(nstr + blink[bl], 1, (255,255,255))
        scr.blit(background,(0,0))
        scr.blit(font4.render('You got a new high score!', True, WHITE), (scrwidth//2.5-70, int(scrheight/3.5)))

        scr.blit(font4.render("Enter your Name:", 1, WHITE),((scrwidth / 2) - 240, (scrheight / 2)-13))
        pygame.draw.rect(scr, (0,0,0),((scrwidth / 2) - 50,(scrheight / 2) - 10,230,32), 0)
        pygame.draw.rect(scr, (255,255,255),((scrwidth / 2) - 50,(scrheight/ 2) - 12,230,34), 1)
        nstr = nstr.title()
        #Blits the flashing line
        scr.blit(txt,((scrwidth / 2) - 47, (scrheight / 2) - 14))
        pygame.display.update()

          
def pause():

    """ Function to handle the game when paused by user"""
    
    scr.blit(background,(0,0))
    pygame.draw.polygon(scr, BLACK, ((fl_x, fl_y),
            (fl_x + flwidth, fl_y), (fl_x + flwidth, fl_y + flheight),
            (fl_x, fl_y + flheight)))

    pygame.draw.polygon(scr, barcolour, ((fl_x + 2, fl_y + 1),
            (fl_x + greenwidth + 2, fl_y), (fl_x + greenwidth + 2, fl_y + flheight - 1),
            (fl_x + 2, fl_y + flheight - 1)))
    
    scr.blit(font2.render('STAMINA', True, (255,255,255)), (fl_x+flwidth/4, fl_y))
    scr.blit(font2.render('SCORE: ', True, (255,0,0)), (scrwidth - 150, 20))
    scr.blit(font1.render(str(int(score)), True, (255,0,0)), (scrwidth - 150 + 80, 22)) ###
    scr.blit(lava, (xlava, ylava))

    
    txt1 = font3.render('GAME PAUSED', True, WHITE)
    txt2 = font1.render('Click to continue', True, WHITE)
    scr.blit(txt1, ((scrwidth-txt1.get_width())/2, int(scrheight/2.5)))
    scr.blit(txt2, ((scrwidth-txt2.get_width())/2, int(scrheight/2.5)+70))
    pygame.display.update()
    
    paused = True
    while paused:
        
        
        for event in pygame.event.get():
            if event.type == QUIT:

                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key in [K_q,K_ESCAPE]:
                    scr.blit(background,(0,0))
                    quitter(score)

                elif event.key in [K_p]:
                    paused = False
                    
                    
                elif event.key == K_RETURN:
                    paused = False
                    
            if event.type == MOUSEBUTTONDOWN:
                paused = False         
    
intern
def list_gen():
    
    """Generates the list with random length"""

    global length_list
    notyet = []
    for i in xrange(0,scrwidth, box_width):
        for j in xrange(0,scrheight, box_width):
            notyet.append([i,j])
    
    while notyet:
        j = random.choice(notyet)
        notyet.remove(j)
        length_list -= 1
        yield j

def pixelator():
    
    """Function for initial animation of pixels appearing"""

    clock = pygame.time.Clock()
    fill_num = 2
    pix = list_gen()
    prev_length = length_list
    esc_flag = False
    try:
        
        fps = 500
        while True and not esc_flag:
            
            if length_list <= int(prev_length*0.25):
                fill_num += 1
                prev_length = length_list
            for i in xrange(fill_num):
                j = pix.next()
                a, b = j[0], j[1]
                red = random.randint(0,255)
                green = random.randint(0,255)
                blue = random.randint(0,255)
                pygame.draw.polygon(scr, (red, green, blue),
                            ((a,b),
                            (a + box_width -1, b), (a + box_width -1, b + box_width -1),
                            (a, b + box_width -1)))

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == KEYDOWN:
                    if event.key == [K_ESCAPE, K_SPACE, K_RETURN]:
                        esc_flag = True
                        
                if event.type == MOUSEBUTTONDOWN:
                    esc_flag = True
                
            pygame.display.update()
            clock.tick(fps)
            
    except StopIteration:
        pass

    fps = 50
    i = 0
    while i<= scrwidth/2 and not esc_flag:
        left, right = scrwidth/2 - i, scrwidth/2 + i
        up = int(left * float(scrheight)/scrwidth)
        down = int(right * float(scrheight)/scrwidth)              
        pygame.draw.polygon(scr, MENUCL,
                    ((left,up), (right, up), (right, down), (left, down)))

        i += 3

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key in [K_ESCAPE, K_SPACE, K_RETURN]:
                    esc_flag = True

            if event.type == MOUSEBUTTONDOWN:
                esc_flag = True
        
        pygame.display.update()
        clock.tick(fps)



    pygame.draw.polygon(scr, MENUCL,((0,0),(scrwidth, 0),
                                      (scrwidth, scrheight),(0, scrheight)))
    pygame.display.update()

def logo():
    
    """Displays GA Studios Logo in different colours"""

    red, green, blue = studio_red, studio_green, studio_blue
    steps = 15.0
    txt = font6.render('GA Studios'+' '+chr(169), True,
            (0, 0, 0))
    txt_width = txt.get_width()
    txt_height = txt.get_height()
    del txt

    clock = pygame.time.Clock()
    fps = 10
    rcount = gcount = bcount = 0
    esc_flag = False
    while True and not esc_flag:

        pygame.draw.polygon(scr, MENUCL, ((int(scrwidth*0.3), int(scrheight*0.4)),
                            (int(scrwidth*0.7), int(scrheight*0.4)),
                            (int(scrwidth*0.7), int(scrheight*0.6)),
                            (int(scrwidth*0.3), int(scrheight*0.6))))
        pygame.display.update()
        
        if rcount <= int(steps):
            
            scr.blit(font6.render('GA Studios'+' '+chr(169), True,
                (int(red * rcount/steps), 0, 0)),
                ((scrwidth - txt_width)/2, (scrheight - txt_height)/2))
            pygame.display.update()

            rcount += 1

        elif gcount <= int(steps):
            
            scr.blit(font6.render('GA Studios'+' '+chr(169), True,
                (red, int(green * gcount/steps), 0)),
                ((scrwidth - txt_width)/2, (scrheight - txt_height)/2))
            pygame.display.update()

            gcount += 1

        elif bcount <= int(steps):
            
            scr.blit(font6.render('GA Studios'+' '+chr(169), True,
                (red, green, int(blue * bcount/steps))),
                ((scrwidth - txt_width)/2, (scrheight - txt_height)/2))
            pygame.display.update()

            bcount += 1

        else:
            break

        

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key in [K_ESCAPE, K_SPACE]:
                    esc_flag = True

            if event.type == MOUSEBUTTONDOWN:
                esc_flag = True

        clock.tick(fps)
        
    pygame.draw.polygon(scr, MENUCL,((0,0),(scrwidth, 0),
                                      (scrwidth, scrheight),(0, scrheight)))        
    scr.blit(font6.render('GA Studios'+' '+chr(169), True,
                (red, green, blue)),
                ((scrwidth - txt_width)/2, (scrheight - txt_height)/2))
    pygame.display.update()
    time.sleep(0.5)
    
def instructions():
    "Displays the intructions and the story"
    
    scr.blit(story, (0,0))
    pygame.display.update()
    
    esc_flag = False
    
    clock = pygame.time.Clock()
    fps = 40
    
    while not esc_flag:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key in [K_ESCAPE, K_SPACE, K_RETURN]:
                    esc_flag = True
                else:
                    pass

            if event.type == MOUSEBUTTONDOWN:
                pass

        clock.tick(fps)

    scr.blit(instr, (0,0))
    pygame.display.update()
    
    esc_flag = False

    while not esc_flag:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key in [K_ESCAPE, K_SPACE, K_RETURN]:
                    esc_flag = True
                else:
                    pass

            if event.type == MOUSEBUTTONDOWN:
                pass
    
    
def linelistgen():
    try:
        linelist = [i for i in range(scrwidth/linewidth)]
        while True:
            item = random.choice(linelist)
            linelist.remove(item)
            yield item
    except IndexError:
        raise StopIteration

        
def exitter():
    pygame.draw.polygon(scr, (0,0,0),((0,0),(scrwidth, 0),
                                      (scrwidth, scrheight),(0, scrheight)))

    red, green, blue = studio_red, studio_green, studio_blue
    txt = font6.render('GA Studios'+' '+chr(169), True,
            (0, 0, 0))
    txt_width = txt.get_width()
    txt_height = txt.get_height()


    scr.blit(font6.render('GA Studios'+' '+chr(169), True,
                (red, green, blue)),
                ((scrwidth - txt_width)/2, (scrheight - txt_height)/2))
    pygame.display.update()
    
    time.sleep(0.5)
    
    try:
        
        line = linelistgen()
        width = linewidth
        clock = pygame.time.Clock()
        fps = 60
        n = 4
        while True:
            colours = {}
            for i in range(n):
                colours [line.next()] = (random.randint(0,255),
                                        random.randint(0,255),
                                        random.randint(0,255))
            
            addheight = 40
            height = 0
            draw = True
            while draw:
                for i in colours:
                    left = width*i
                    right = width*(i+1)
                    pygame.draw.polygon(scr, colours[i],((left,0),(right, 0),
                                              (right, height),(left, height)))
                pygame.display.update()

                height += addheight

                if height > scrheight:
                    draw = False

                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == KEYDOWN:
                        pass

                    if event.type == MOUSEBUTTONDOWN:
                        pass

                clock.tick(fps)
                
    
    except StopIteration:
        pass
        

def menu():
    
    """Main function to handle menu and subsequent input from user"""

    pygame.draw.polygon(scr, MENUCL,((0,0),(scrwidth, 0),
                                      (scrwidth, scrheight),(0, scrheight)))

    scr.blit(background1,(0,0))
    
    
    txt = font6b.render('GA Studios'+' '+chr(169), True,
                (studio_red, studio_green, studio_blue))
    txt_width = txt.get_width()
    txt_height = txt.get_height()
    scr.blit(txt, ((scrwidth - txt_width)/2, (scrheight - txt_height)/2 + 100))

    game_txt = font7.render('Superbot', True,
                (game_red, game_green, game_blue))
    game_width, game_height = game_txt.get_width(), game_txt.get_height()
    scr.blit(game_txt, ((scrwidth - game_width)/2,
                        (scrheight - 150 - game_height)/2))

    pygame.display.update()
    time.sleep(0.2)

    menu_list = ['Play', 'Instructions', 'High scores', 'Exit']
    menu_state = prev_state= 0
    st_left = ' '*12
    st_right = menu_list[1]
    st_current = menu_list[0]

    superman.x_y(-skwidth, scrheight/2 + 40)
    dsx, dsy = 4,0

    clock = pygame.time.Clock()
    fps = 60

    col_1 = (150,220,150)
    col_2 = (200,250,250)
    start_play = False

    txt1 = font1.render('Use SPACE or ENTER key to select', True, (250,215,215))
    
    
    while True:

        
        pygame.draw.polygon(scr, MENUCL,((0,0),(scrwidth, 0),
                            (scrwidth, scrheight),(0, scrheight)))

        scr.blit(background1,(0,0))
        
        if start_play:
            break

        scr.blit(superman.image, (superman.rect.x,superman.rect.y))
        
        scr.blit(txt, ((scrwidth - txt_width)/2,
                       (scrheight - txt_height)/2 + 100))

        scr.blit(game_txt, ((scrwidth - game_width)/2,
                        (scrheight - 150 - game_height)/2))
        
        scr.blit(txt1, (20,330))
        
        if menu_state != prev_state:

            prev_state = menu_state
            st_current = menu_list[menu_state]

            if menu_state != 0:
                st_left = menu_list[menu_state-1]
                
            else:
                st_left = ' '*12

            try:
                st_right = menu_list[menu_state+1]
                
            except IndexError:
                st_right = ' '*12

        txt_left = font9.render(st_left, True, col_1)

        scr.blit(txt_left, (scrwidth/5 - txt_left.get_width()/2,
                            (scrheight - txt_left.get_height())/2))

        txt_right = font9.render(st_right, True, col_1)

        scr.blit(txt_right, ((scrwidth*4)/5 - txt_right.get_width()/2,
                            (scrheight - txt_right.get_height())/2))

        txt_current = font8.render(st_current, True, col_2)

        scr.blit(txt_current, ((scrwidth - txt_current.get_width())/2,
                            (scrheight - txt_current.get_height())/2))

        if superman.rect.x > scrwidth:
            superman.x_y(-skwidth, scrheight/2 + 40)
        
        superman.dx_dy(dsx, dsy)
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    if menu_state < 3:
                        menu_state += 1
                        
                if event.key == K_LEFT:
                    if menu_state > 0:
                        menu_state -= 1

                if event.key in [K_RETURN, K_SPACE]:
                    if menu_state == 0:
                        start_play = True
                        superman.default()

                    elif menu_state == 1:
                        instructions()

                    elif menu_state == 2:
                        dispscore()
                        
                    elif menu_state == 3:
                        exitter()
                        pygame.quit()
                        sys.exit()
                        

            if event.type == MOUSEBUTTONDOWN:
                pass
        
        clock.tick(fps)
############################################################################


"""Data Definitions at the start of the program"""
superman = MainChar()
splist = pygame.sprite.Group()
splist.add(superman)

box_width = 5
length_list = 0
    
fl_x = fl_y = 20
flwidth = 200
flheight = 20
maxflytime = 2.0    # Fly Key is f
flydivconst = 3.0 # The flybar will get charged at 1/flydivconst times the
                    # speed with fly gets used up
clock = pygame.time.Clock()

yabs = skheight+superman.rect.y-1    #starting height of platforms (mean of Gaussian Distribution)
sigma = 20 #Standard deviation for the Gaussian distribution of platforms
# sigma was initially 150

pixelator()
logo()
ingame = True

"""Loop to run entire game begins"""
while ingame:
    #Data Definitions
    superman = MainChar()
    splist = pygame.sprite.Group()
    splist.add(superman)

    yabs = skheight+superman.rect.y-1
    
    Coins.clist = []

    fps = 60

    dx = -5
    dy = fy = 0
    y_coord = ((scrheight + 20 )/2) - skheight 

    xlava = 0
    ylava = scrheight+220  #200 pixels below bottom of screen
    minylava = 290  # lava rises to this height
    deathsound = pygame.mixer.Sound('lava.wav')
    deathsoundstate = True

    for i in range(10):
        for position in Plat.pos:
            platform = Plat(i*pwidth, yabs, position)
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
    flyflag = False     # To check whether superman is flying
    prevflytime = time.time()
    jump = 0

    score = 0
    dist = 0
    coincount = 0
    newcoin = False
    coinscore = 500
    alive = True

    menu()

    c1 = Coins(10*pwidth-10,yabs-35, 1)
    Coins.clist += [c1]
    Coins.ctime = time.time()
    splist.add(c1)

    superman.default()
    
    pygame.sprite.spritecollide
    """Loop for inividual gameplay begins"""
    while alive:
        
        scr.blit(background,(0,0))
        splist.draw(scr)
        scr.blit(superman.image, (superman.rect.x,superman.rect.y))

        dist += abs(dx)
        
        if newcoin:
            score += (abs(dx))**1.2 * (coincount)*coinscore
            coincount = 0
            newcoin = False
        else:
            score += (abs(dx))**1.2
        for i in Coins.clist:
            if pygame.sprite.collide_rect(superman, i):
                Coins.sound.play()
                newcoin = True
                coincount = i.type
                Coins.clist.remove(i)
                splist.remove(i)
                del i
        if time.time() - Coins.ctime > Coins.rt:
            Coins.generate()

            
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
        
        
        greenwidth = int((flwidth-4) * flybarfraction)

        if flybar > 1.25:
            barcolour = GREEN
        elif 1.25 > flybar > 0.45:
            barcolour = YELLOW
        else:
            barcolour = RED
            
        pygame.draw.polygon(scr, barcolour, ((fl_x + 2, fl_y + 1),
                (fl_x + greenwidth + 2, fl_y), (fl_x + greenwidth + 2, fl_y + flheight - 1),
                (fl_x + 2, fl_y + flheight - 1)))
        scr.blit(font2.render('STAMINA', True, (255,255,255)), (fl_x+flwidth/4, fl_y))

        
        
        scr.blit(font2.render('SCORE: ', True, (255,0,0)), (scrwidth - 150, 20))
        scr.blit(font1.render(str(int(score)), True, (255,0,0)), (scrwidth - 150 + 80, 22)) ###

        scr.blit(lava, (xlava, ylava))

        pygame.display.update()

        y_coord += dy
        ylava += dy
        

        if y_coord < -100:
            superman.rect.y += 5

            if deathsoundstate and superman.rect.y > (scrheight-130):
                deathsound.play()
                deathsoundstate = False

            elif superman.rect.y > (scrheight+10):

                #code to die
                quitter(score)
                                #alive = False
                break
        

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

        for i in Coins.clist:
            i.update(dx,dy)

        superman.update(dy)


        #Generating new platforms
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

            


        #Retrieving user input from Keypress and Mouse Actions
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and deathsoundstate:
                if event.key == K_SPACE and deathsoundstate:
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
                    quitter(score)

                elif event.key in [K_p]:
                    pause()

                elif event.key in [K_w]:
                    
                    while True:
                        pass
                    
                elif event.key in (K_f,) and flybar > 0:    # I thought (K_f, K_F)
                    dy = 0
                    flyflag = True
                    startflytime = time.time()
                    superman.image = spimg  # Changing it back to the normal image

            if event.type == KEYUP and deathsoundstate:
                if flyflag:
                    dy = -2
                    flyflag = False    
                    superman.image = spDownimg
                    
                    
            if event.type == MOUSEBUTTONDOWN and deathsoundstate:
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
                    
                

        #Ensures the screen updates at fps frames per second
        clock.tick(fps)
    
