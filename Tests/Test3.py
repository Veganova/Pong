import pygame, sys
import math
from pygame.locals import *
'''
#SLOW THE BALL RELATIVE TO THE STARTING SPEED OF THE BALL!!!
#CHECK FOR DIVISION BY ZERO IN BOUNCE
#STOPPING ON TOP OF A LINE

issues
UNRESOLVED - ball hitting the corener of a barrier
UNRESOLVED - lines are not visually appealing
UNRESOLVED - game is laggy
UNRESOLVED - make a creator mode (can make the maze and the program records the data points of the lines they create)
UNRESOLVED - make an AI based on the TIC-TAC-TOE project idea
UNRESOLVED - Goal visual

RESOLVED - ball bounce off any type of straight barrier
RESOLVED - draws image from top left, shifted image drawing location appropriately
RESOLVED - make boxes r + k larger in wierd cases (horizontal)
MISC.
-pygame.sprite.colide_cricle can be used for the two circles
-pygame.sprite.groupcollide - can be used for collisions between ball and the many lines
'''
pygame.init()
#myfont = pygame.font.SysFont("monospace", 15)
MAX_X = 960
MAX_Y = 640
first = 0
game = False
starting_dx = 0
starting_dy = 0
lines = [
    [ [200,300] , [300,100] ],# [[204,302],[196,298] ],
    [ [300,100] , [700,390] ],
    #[ [390,300] ,[390,580] ]
    [ [250,640] , [320,600] ],
    [ [320,600] , [400,600] ],
    [ [400,600] , [470,640] ]
    ]

'''
lines = [ [[200,300] , [500,550]] ,
          [[200,300] , [216,280]]
        ]
'''
#lines = [[[400,300],[570,440]], [[100,200],[250,240]]]
#lines = [[[440,300], [530,230]],[[400,500],[580,420]],[ [400,300],[570,440] ] ]
#lines = [[[500,400],[500,550]]]
#lines = [[[200,400],[400,400]]]
#lines = [[[400,500],[580,420]] , [ [100,200],[250,240] ] ]
#lines = [[[400,300],[570,430]]]
#lines = [ [[200,200],[500,200]],[[500,200],[
# set up the window
screen = pygame.display.set_mode((MAX_X,MAX_Y))

  #change pygame.sprite.Sprite to objects and take out the first line after the def__init__ to revert back to old class
class Text(pygame.sprite.Sprite):
    def __init__(self,text, x,y,color,size):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        
    def draw(self):
        font = pygame.font.Font(None, self.size)
        text = font.render(self.text, 1, self.color)
        screen.blit(text, [self.x,self.y])
    def hover(self):
        global game
        length = len(self.text)
        text_width = 87
        text_height = 30
        #l = list(color)
        #pygame.draw.rect(screen,BLACK,(self.x,self.y,text_width,text_height),3)
        x=pygame.mouse.get_pos()[0]
        y=pygame.mouse.get_pos()[1]
        if(self.x<x and x<self.x+text_width)and(self.y<y and y<self.y+text_height):
                self.change()
                if(pygame.mouse.get_pressed()[0] == 1):
                    game = True
        else:
            #self.size = 50
            #self.x = 420
            #self.y = 200
            self.color = (255,255,255)
    def change(self):
        l = list(self.color)
        #if(self.size < 75):
         #   self.size += 3
        #self.size = 70
        if(l[2] > 100):
            l[2] = (l[2]%256)-10
        self.color = tuple(l)
        
class Ball(pygame.sprite.Sprite):
    def __init__(self, x,y,dx,dy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("BaLl.png")
        self.x = x
        self.r = 30
        self.y = y
        self.dx = dx
        self.dy = dy
        self.stop = 0
        self.go = False
    def move(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self, screen):
        screen.blit(self.image,(self.x-self.r,self.y-self.r))
        #pygame.draw.rect(screen,BLACK,(self.x,self.y,10,10),0)
        
    def checkEdges(self):
        if((self.x+self.r)>MAX_X):
            self.dx = -self.dx
        if((self.x-self.r)<=0):
            self.dx = -self.dx
        if((self.y+self.r)>MAX_Y):
            self.dy = -self.dy
        if((self.y-self.r)<0):
            self.dy = -self.dy

    def endZone(self):
        #screen.blit(goals_image,[0,0])
        width = 93
        length = 252
        #180 - y
        pygame.draw.rect(screen,BLACK,((MAX_X-width),(MAX_Y/2-length/2),width,length),4)
        if((self.x>(MAX_X- width)) and (MAX_Y/2 - length/2 <self.y) and (MAX_Y/2+length/2 > self.y) and (self.dx==0 and self.dy==0)):#if ball in goal and not moving
            print"goal"
    def bounce(self, line):
        line_vec = [line[1][0] - line[0][0], line[1][1] - line[0][1]]
        ball_vec = [self.dx,self.dy]
        if(line_vec[0] == 0):
            ball_vec[0] = -ball_vec[0]
        elif(line_vec[1] == 0):
            ball_vec[1] = -ball_vec[1]
        else:
            side = self.line_side(line)#next few variables cannot cause error if declared in the beginning of the function because of the straight line cases
            deg = CrossProductDegrees(line_vec, ball_vec)
            line_slope = findSlope(line)#float(line_vec[1])/line_vec[0]
            if(side == 1 and line_slope<0):
                ball_vec = rotateVec(ball_vec,(2*math.pi - 2*deg))
            elif(side == 0 and line_slope<0):
                ball_vec = rotateVec(ball_vec,(2*deg))
            elif(side == 1 and line_slope>0):
                ball_vec = rotateVec(ball_vec,(2*deg))
            elif(side == 0 and line_slope>0):
                ball_vec = rotateVec(ball_vec,(2*math.pi - 2*deg))
        self.dx = ball_vec[0]
        self.dy = ball_vec[1]
                 
    def line_side(self,line):
        m = findSlope(line)
        b = line[0][1] - (m*line[0][0])
        x_line = (self.y -b)/m
        if(self.x - x_line > 0):
            return 0#right
        else:
            return 1#left
    def slow(self,x):
        k =  math.sqrt(self.dx*self.dx + self.dy*self.dy)
        if(k<.2):
            self.dy =0
            self.dx =0
        else:
            self.dy /= x
            self.dx /= x
    '''
        k = 1.0/12.0
        stop_dx = starting_dx * k
        stop_dy = starting_dy * k

        if(((abs(self.dx) > stop_dx)and(abs(self.dy )> stop_dy))and((abs(self.dx) > 0.05)and(abs(self.dy) > 0.05))):
            self.dy = self.dy/x
            self.dx = self.dx/x
        else:
            self.dy = 0
            self.dx = 0
        '''
    def pointToLine(self,line):#[[400,500],[580,420]]
        m = findSlope(line)#slope of the barrier line
        if(m==0):
            distance = abs(line[0][1] - self.y)
        else:
            x = ((self.y + (1/m)*self.x)-(line[0][1]- m*line[0][0]))/(m+(1/m))
            y = x*m+(line[0][1]- m*line[0][0])
            #drawSquare([x,y]) DRAWS A SMALL SQUARE AT THE EXPECTED POINT OF INTERSECTION OF THE BALL AND THE LINE
            distance = dist([self.x,self.y],[x,y])
        if(distance<=self.r):
            self.bounce(line)
    def Check(self,line):
        #pygame.draw.rect(screen, color, (x,y,width,height), thickness)
        xdif = abs(line[0][0]-self.x)+abs(line[1][0] - self.x)#+2*self.r
        ydif = abs(line[0][1]-self.y)+abs(line[1][1] - self.y)#+2*self.r 
        #if((line[0][1]-line[1][1]>0)):
         #   pygame.draw.rect(screen,BLACK,(line[0][0]-self.r,line[1][1]-self.r,abs(line[0][0]-line[1][0])+2*self.r,abs(line[0][1]-line[1][1])+2*self.r),2)
        #else:
         #   pygame.draw.rect(screen,BLACK,(line[0][0]-self.r,line[0][1]-self.r,abs(line[0][0]-line[1][0])+2*self.r,abs(line[0][1]-line[1][1])+2*self.r),2)
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

                             
def CrossProductDegrees(line_v, ball_v):#meant to be dot product. uses that to find degrees between two vectors
    #print "line: ", line_v[0] ," " , line_v[1]
    #print "ball: " , ball_v[0] , " " , ball_v[1]
    return math.acos((line_v[0]*ball_v[0]+line_v[1]*ball_v[1])/(math.sqrt((line_v[0]*line_v[0] +line_v[1]*line_v[1])*(ball_v[1]*ball_v[1] + ball_v[0]*ball_v[0]))))
    
def rotateVec(vec,deg):#clockwise rotation matrix
    new_vec = [vec[0]* math.cos(deg)- vec[1]*math.sin(deg), vec[0]*math.sin(deg) + vec[1]*math.cos(deg)]
    return new_vec

def logistic(time):
    return 1.0/(1+math.e**(-2*time/150))

def score(ball, num):
    if(ball.dx != 0 or ball.dy != 0):
        ball.go = True
    elif(ball.dx == 0 and ball.dy == 0 and ball.go == True):
        ball.stop += 1
        ball.go = False
    
    text = pygame.font.Font(None, 35).render(str(ball.stop), 1, (0,0,0))
    player = pygame.font.Font(None, 30).render("P" + str(num+1),1,(0,0,0))
    screen.blit(player, [10+num*30,0])
    screen.blit(text, [10+num*30,20])
                      
def mouseShoot(ball):
    global first, starting_dx, starting_dy
    r = 2.5*ball.r
    k = 16 #max speed
    if(abs(pygame.mouse.get_pos()[0]-ball.x) < r):
        if(abs(pygame.mouse.get_pos()[1]-ball.y) < r):#if mouse is within the circle
            curr_time = pygame.time.get_ticks()
            #print pygame.time.get_ticks()
            if(pygame.mouse.get_pressed()[0] == 1):#if mouse is clicked
                pygame.draw.line(screen,BLACK, (pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]),(ball.x,ball.y),1)
                #print pygame.mouse.get_pressed()
                if(first == 0): #first time registered click for all the ongoing loops
                    first = curr_time
                    
            elif((first!=0)and(pygame.mouse.get_pressed()[0] == 0)):
                total = curr_time - first
                #print total
                first = 0
                x=(ball.x- pygame.mouse.get_pos()[0])
                y=(ball.y- pygame.mouse.get_pos()[1])
                m = math.sqrt(x**2 + y**2)
                ball.dx = x/m*k*logistic(total)
                ball.dy = y/m*k*logistic(total)
                starting_dx = ball.dx
                starting_dy = ball.dy
                                
            pygame.draw.line(screen,BLACK, (pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]),(ball.x,ball.y),5)
            
def drawShootCircle(x,y,r):
    for i in range(16):
        if (i%2 == 1):
            drawCircleArc((x,y),r,(i*math.pi/6),((i+1)*math.pi/6))

def dist(pnta,pntb):
    return math.sqrt((pnta[0]-pntb[0])**2+(pnta[1]-pntb[1])**2)
def drawSquare(point):
    pygame.draw.rect(screen,BLACK,(point[0],point[1],20,20),4)

def findSlope(line):
    if((line[0][0]-line[1][0]) == 0):
        return 1000.0
    slope =  float(line[0][1]-line[1][1])/(line[0][0]-line[1][0])
    return slope
def drawLines(lines, thickness):
    for i in lines:
        pygame.draw.line(screen, BLACK, (i[0][0],i[0][1]), (i[1][0],i[1][1]), thickness)
def starting():
    screen.blit(start_screen,[0,0])
    #drawInteractiveText("PLAY", [400,200], WHITE, 60)
    text_play.draw()
    text_play.hover()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()

def keyPress(ball):
    global game
    key=pygame.key.get_pressed()
    if(key[K_SPACE]):
        ball.dx = 0
        ball.dy = 0
    if((ball.dx ==0 )and( ball.dy ==0)):
        drawShootCircle(ball.x,ball.y,2.5*ball.r)
        mouseShoot(ball)
    if(key[K_ESCAPE]):
        game = False
        
        
def drawInteractiveText(text, location, color, size):
    font = pygame.font.Font(None, size)
    rbg = color
    text = font.render(text, 1, rbg)
    screen.blit(text, location)
    
def runGame():
    #--------------------------------------DRAW SCREEN COMPONENTS------------------------------------------#
    screen.blit(background_image,[0,0])
    for n in range(len(ball_collec)):
        ball_collec[n].endZone()#check if goal is scored
        score(ball_collec[n],n)
    drawLines(lines, 5)#draw the obstacles
    
        
    #--------------------------------------GAME FUNCTIONS--------------------------------------------------#
    for n in range(len(ball_collec)):   #BUGS MIGHT COME FROM HERE BECAUSE EARLIER ALL THESE FUNCTIONS WERE IN THEIR OWN FOR LOOPS.  
        keyPress(ball_collec[n])        #NOW EACH BALL GETS *ALL* THEIR FUNCTIONS DONE AND THEN IT GOES TO THE NEXT BALL INSTEAD
        ball_collec[n].draw(screen)
        ball_collec[n].move()
        ball_collec[n].checkEdges()
        ball_collec[n].slow(1.022)
    
    #print pygame.mouse.get_pos()
    #print "SIDE: ",ball1.line_side(lines[0])
    #print "Ball:" , ball1.dy/ball1.dx
    #print "Line:" , findSlope(lines[0])
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    for line in lines:
        #pygame.draw.circle(screen, BLACK, (line[0][0],line[0][1]), 2, 0)
        #pygame.draw.circle(screen, BLACK, (line[1][0],line[1][1]), 2, 0)
        for n in range(len(ball_collec)):
            if(ball_collec[n].Check(line)):
                ball_collec[n].pointToLine(line)
    pygame.display.update()


    
# set up the colors
BLACK = (  0,   0,   0)
WHITE = (255,255,255)
# draw on the surface object

#ball_image= pygame.image.load("MetalBal.png")
goals_image = pygame.image.load("Goals.png")
background_image = pygame.image.load("icebackground.png")
start_screen = pygame.image.load("OpenScreen.png")
#pygame.draw.circle(screen, BLACK, (300, 50), 20, 0)
#[[400,500],[580,420]]
x = 320.0
y = 500.0
dx = 0
dy = 0
starting_dx = dx
starting_dy = dy
'''
x = 620.0
y = 399.0

dx = 4
dy = 2
'''

ball_collec = [Ball(x,y,dx,dy)]#,Ball(y,x,dx,dy),Ball(100,x,dx,dy)]
text_play = Text("PLAY",420,200,(255,255,255),50)
# run the game loop
while True:
    if(game==False):
        starting()
        for x in range(len(ball_collec)):
            ball_collec[x].stop = 0
    elif(game==True):
        runGame()
        #print ball1.dx
   
