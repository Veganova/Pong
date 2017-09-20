import pygame, sys
import math
from pygame.locals import *
'''
#SLOW THE BALL RELATIVE TO THE STARTING SPEED OF THE BALL!!!
#CHECK FOR DIVISION BY ZERO IN BOUNCE
#STOPPING ON TOP OF A LINE

issues
UNRESOLVED - more facts than slope determine cases for bounce. if the intersection angle is >90 or <90 makes a difference
UNRESOLVED - direction with which the ball hits the barrier matters
UNRESOLVED - side from which the ball hits the barrier matters CHECK DY SIGN
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
first = 0
starting_dx = 0
starting_dy = 0
#lines = [[ [400,300],[570,440] ] ] #, [ [100,200],[250,240] ] ]
lines = [[[440,300], [530,230]],[[400,500],[580,420]],[ [400,300],[570,440] ] ]
#lines = [[[400,500],[580,420]] , [ [100,200],[250,240] ] ]
#lines = [[ [400,300],[570,440] ]  ]
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
        
        return math.sqrt((self.dx)**2+(self.dy)**2)
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
        
    def bounce(self,line):#POSITIVES AND NEGATIVES ARE SWITCHED B/C OF Y AXIS
        
        line_slope = findSlope(line)#slope of the barrier line
        if(abs(self.dx)<.00001):
            
            ball_slope = 1000#/(self.dx/abs(self.dx)) #denominator to get the sign of self.dx
        else:
            ball_slope = self.dy/self.dx#ball slope
        perp = -1/line_slope
        l = math.atan(line_slope)
        b = math.atan(ball_slope)
        side = self.line_side(line)
        
        
        if(line_slope < 0):
            
           
            if(ball_slope<0):
                if(side== 1):#left
                    if(ball_slope > line_slope):
                        print "1"
                        mid_angle = l-b
                        new_angle = l+mid_angle
                    elif(ball_slope < line_slope):
                        print "2"
                        mid_angle = b - l;
                        new_angle = math.pi + l - mid_angle
                elif(side == 0):#right
                    if(ball_slope < line_slope):
                        print "3"
                        mid_angle = b -l
                        new_angle = l - mid_angle
                    elif(ball_slope > line_slope):
                        print"4"
                        mid_angle = l - b
                        new_angle = l + math.pi + mid_angle
            elif(ball_slope > 0):
                if(side== 0):#right
                    if(ball_slope > perp):
                        mid_angle = math.pi - (l-b)
                        new_angle = l - mid_angle
                        print "5"
                    elif(ball_slope < perp):
                        mid_angle = l - b
                        new_angle = l + math.pi + mid_angle
                        print "6"
                elif(side == 1):#left
                    if(ball_slope < perp):
                        mid_angle = l-b
                        new_angle = l +mid_angle
                        print "7"
                    if(ball_slope > perp):
                        mid_angle = math.pi - (l-b)
                        new_angle = l + math.pi - mid_angle
                        print "8"
            
            
        elif(line_slope > 0):
            perp = line_slope
            line_slope = -1/line_slope
           
            if(ball_slope<0):
                if(side== 1):#left
                    if(-ball_slope > perp):
                        print "-1"
                        mid_angle = math.pi - (b-l)
                        new_angle = b + 2*mid_angle

                    elif(-ball_slope < perp):
                        print "-2"
                        mid_angle = b-l
                        new_angle = l - mid_angle
                elif(side== 0):#right
                    if(-ball_slope > perp):
                        print "-3"
                        mid_angle = math.pi - (b-l)
                        new_angle = mid_angle + l

                    elif(-ball_slope < perp):
                        print "-4"
                        mid_angle = b-l
                        new_angle = l + math.pi - mid_angle

            elif(ball_slope > 0):
                if(side == 1):#left
                    if(-ball_slope > line_slope):
                        mid_angle = b - l
                        new_angle = l - mid_angle
                        print "-5"
                    elif(-ball_slope < line_slope):
                        mid_angle = l -b
                        new_angle = l + math.pi + mid_angle
                        print "-6"
                elif(side== 0):#right
                    if(-ball_slope  < line_slope):
                        mid_angle = l - b
                        new_angle = l + mid_angle
                        print "-7"

                    elif(-ball_slope > line_slope):
                        mid_angle = b - l
                        new_angle = l + math.pi - mid_angle
                        print "-8"

                    
        self.dx = math.cos(new_angle)*self.mag()
        self.dy = math.sin(new_angle)*self.mag()
            
               
    def line_side(self,line):
        m = findSlope(line)
        b = line[0][1] - (m*line[0][0])
        x_line = (self.y -b)/m
        if(self.x - x_line > 0):
            return 0#right
        else:
            return 1#left
    def slow(self,x):
        k = 1.0/12.0
        stop_dx = starting_dx * k
        stop_dy = starting_dy * k
        if(((abs(self.dx) > stop_dx)and(abs(self.dy )> stop_dy))and((abs(self.dx) > 0.05)and(abs(self.dy) > 0.05))):
            self.dy = self.dy/x
            self.dx = self.dx/x
        else:
            self.dy = 0
            self.dx = 0
        
    def pointToLine(self,line):#[[400,500],[580,420]]
        m = findSlope(line)#slope of the barrier line
        x = ((self.y + (1/m)*self.x)-(line[0][1]- m*line[0][0]))/(m+(1/m))
        y = x*m+(line[0][1]- m*line[0][0])
        #drawSquare([x,y])
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
def drawCircleArc(center,radius,startDeg,endDeg):
    (x,y) = center
    rect = (x-radius,y-radius,radius*2,radius*2)
    pygame.draw.arc(screen,BLACK,rect,startDeg,endDeg, 3)

def mouseShoot():
    global first, starting_dx, starting_dy
    r = 80
    k = .0005
    if(abs(pygame.mouse.get_pos()[0]-ball1.x) < r):
        if(abs(pygame.mouse.get_pos()[1]-ball1.y) < r):#if mouse is within the circle
            curr_time = pygame.time.get_ticks()
            if(pygame.mouse.get_pressed()[0] == 1):#if mouse is clicked
                pygame.draw.line(screen,BLACK, (pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]),(ball1.x,ball1.y),1)
                #print pygame.mouse.get_pressed()
                if(first == 0):
                    first = curr_time
                    
            elif((first!=0)and(pygame.mouse.get_pressed()[0] == 0)):
                total = curr_time - first
                first = 0
                ball1.dx = (ball1.x- pygame.mouse.get_pos()[0])*k*total
                ball1.dy = (ball1.y- pygame.mouse.get_pos()[1])*k*total
                starting_dx = ball1.dx
                starting_dy = ball1.dy
                
                
            pygame.draw.line(screen,BLACK, (pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]),(ball1.x,ball1.y),5)
            
def drawShootCircle(x,y,r):
    for i in range(16):
        if (i%2 == 1):
            drawCircleArc((x,y),r,(i*math.pi/6),((i+1)*math.pi/6))
def keyPress():
    key=pygame.key.get_pressed()
    if(key[K_SPACE]):
        ball1.dx = 0
        ball1.dy = 0
    if((ball1.dx ==0 )and( ball1.dy ==0)):
        drawShootCircle(ball1.x,ball1.y,80)
        mouseShoot()
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
#[[400,500],[580,420]]
x = 320.0
y = 500.0
dx = 5.0
dy = -2.50
starting_dx = dx
starting_dy = dy
'''
x = 620.0
y = 399.0
dx = 4
dy = 2
'''
ball1 = Ball(x,y,dx,dy)
lol2 = 0.0
lol = 0

# run the game loop
while True: 
    
    screen.blit(background_image,[0,0])
    drawLines(lines)
    ball1.draw(screen)
    keyPress()
    ball1.move()
    #ball1.x = pygame.mouse.get_pos()[0]
    #ball1.y = pygame.mouse.get_pos()[1]
    ball1.checkEdges()
    ball1.slow(1.01)
    #print pygame.mouse.get_pos()
    #print "SIDE: ",ball1.line_side(lines[0])
    #print "Ball:" , ball1.dy/ball1.dx
    #print "Line:" , findSlope(lines[0])
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
