import pygame, sys
import math
from pygame.locals import *
'''
issues
UNRESOLVED - more facts than slope determine cases for bounce. if the intersection angle is >90 or <90 makes a difference
UNRESOLVED - direction with which the ball hits the barrier matters
UNRESOLVED - side from which the ball hits the barrier matters
SEMIRESOLVED- since y goes oppositely, slope will be made negative , another way of going about this could have been to flip all y values until the end to get the normal coodrinate system

RESOLVED - draws image from top left, shifted image drawing location appropriately
RESOLVED - make boxes r + k larger in wierd cases (horizontal)
MISC.
-pygame.sprite.colide_cricle can be used for the two circles
-pygame.sprite.groupcollide - can be used for collisions between ball and the many lines
'''
pygame.init()
MAX_X = 960
MAX_Y = 640
lines = [[[440,300], [530,230]],[[400,500],[580,420]],[[120,500],[200,600]]]

# set up the window
screen = pygame.display.set_mode((MAX_X,MAX_Y))

  #change pygame.sprite.Sprite to objects and take out the first line after the def__init__ to revert back to old class
class Ball(pygame.sprite.Sprite):
    def __init__(self, x,y,dx,dy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("BaLl.png")
        self.x = x
        self.r = 30
        self.y = y
        self.dx = dx
        self.dy = dy
        
    def move(self):
        self.x += self.dx
        self.y += self.dy
    def mag(self):
        return math.sqrt((dx)**2+(dy)**2)
    def draw(self, screen):
        screen.blit(self.image,(self.x-self.r,self.y-self.r))
        pygame.draw.rect(screen,BLACK,(self.x,self.y,10,10),0)
    def checkEdges(self):
        if((self.x+self.r)>MAX_X):
            self.dx = -self.dx
        if((self.x-self.r)<=0):
            self.dx = -self.dx
        if((self.y+self.r)>MAX_Y):
            self.dy = -self.dy
        if((self.y-self.r)<0):
            self.dy = -self.dy
    def bounce(self,line):
        m = findSlope(line)#slope of the barrier line
        m2 = self.dy/self.dx#ball slope
        line_angle = math.atan(m)
        if(m<0):#barrier slope is positive
            if(m2>0):#ball slope is negative
                if(m2>(1/m)):
                    mid_angle = math.pi + math.atan(m2) - line_angle#mid_angle = abs(line_angle-math.atan(m2))
                    new_angle = line_angle + math.pi - mid_angle#new_angle = math.pi-abs(line_angle+mid_angle)
                elif (m2<(1/m)):
                    mid_angle = line_angle + math.atan(m2)
                    new_angle = line_angle + mid_angle
                
                    
            if(m2<0):#ball slope is positivea
                if(m2<(1/m)):
                    mid_angle = math.atan(m2) - line_angle #line_angle is negative
                    new_angle = math.pi- (mid_angle - line_angle)
                
                mid_angle = abs(line_angle-math.atan(m2))#mid_angle = math.pi-(math.atan(m2)+abs(math.pi-line_angle))
                new_angle = math.pi-abs(line_angle+mid_angle)#new_angle = line_angle + mid_angle
        if(m>0):#barrier slope is negative
            if(m2>0):#ball slope is negative
                mid_angle = line_angle - math.atan(m2)
                new_angle = math.pi-(mid_angle+line_angle)
            if(m2<0):#ball slope is positive
                mid_angle = abs(math.atan(m2)- line_angle)
                new_angle = math.pi-abs(mid_angle + line_angle)
        #elif (m2 == (1/m)):
                
                
        self.dx = math.cos(new_angle)*self.mag()
        self.dy = math.sin(new_angle)*self.mag()
    def slow(self,x):
        self.dy = self.dy/x
        self.dx = self.dx/x
    def pointToLine(self,line):#[[400,500],[580,420]]
        m = findSlope(line)#slope of the barrier line
        x = ((self.y + (1/m)*self.x)-(line[0][1]- m*line[0][0]))/(m+(1/m))
        y = x*m+(line[0][1]- m*line[0][0])
        drawSquare([x,y])
        distance = dist([self.x,self.y],[x,y])
        if(distance<=self.r):
            self.bounce(line)
    def Check(self,line):
        #pygame.draw.rect(screen, color, (x,y,width,height), thickness)
        xdif = abs(line[0][0]-self.x)+abs(line[1][0] - self.x)#+2*self.r
        ydif = abs(line[0][1]-self.y)+abs(line[1][1] - self.y)#+2*self.r 
        if((line[0][1]-line[1][1]>0)):
            pygame.draw.rect(screen,BLACK,(line[0][0]-self.r,line[1][1]-self.r,abs(line[0][0]-line[1][0])+2*self.r,abs(line[0][1]-line[1][1])+2*self.r),2)
        else:
            pygame.draw.rect(screen,BLACK,(line[0][0]-self.r,line[0][1]-self.r,abs(line[0][0]-line[1][0])+2*self.r,abs(line[0][1]-line[1][1])+2*self.r),2)
        if(xdif<=abs(line[1][0]-line[0][0])+2*self.r):
            if(ydif<=abs(line[1][1] - line[0][1])+2*self.r):
                return True
            else:
                return False
  # def lineCrash(self, line):
       #intersection point, new vector
       
def dist(pnta,pntb):
    return math.sqrt((pnta[0]-pntb[0])**2+(pnta[1]-pntb[1])**2)
def drawSquare(point):
    pygame.draw.rect(screen,BLACK,(point[0],point[1],20,20),4)

def findSlope(line):
    slope =  float(line[0][1]-line[1][1])/(line[0][0]-line[1][0])
    return slope
def drawLines(lines):
    for i in lines:
        pygame.draw.line(screen, BLACK, (i[0][0],i[0][1]), (i[1][0],i[1][1]), 8)
# set up the colors
BLACK = (  0,   0,   0)
WHITE = (255,255,255)
# draw on the surface object

#ball_image= pygame.image.load("MetalBal.png")

background_image = pygame.image.load("icebackground.png")

pygame.draw.circle(screen, BLACK, (300, 50), 20, 0)

x = 400.0
y = 350.0
dx = .1
dy = 1

ball1 = Ball(x,y,dx,dy)
lol2 = 0.0
lol = 0

# run the game loop
while True:
   
    screen.blit(background_image,[0,0])
    drawLines(lines)
    ball1.draw(screen)
    ball1.move()
    ball1.checkEdges()
   
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    for line in lines:
        if(ball1.Check(line)):
            lol=lol+1
            lol2 = findSlope(line)
            ball1.pointToLine(line)
            
            #print lol2
    pygame.display.update()
