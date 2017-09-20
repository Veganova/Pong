import pygame, sys
import math
from pygame.locals import *
'''
#MAKE A BETTER BORDER CHECKING AREA ... THIS IS BAD TOWARDS THE EDGES
#MAYBE USE THE (A A-1)T ... MATRIX ERROR THINGY TO FIND OUT DISTANCE BETWEEN BETWEEN BALL AND LINE MORE EFFECIENTLY
#BALL ON BALL COLLISSION

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


class ZoomScreen:
	"""
	"""
	def __init__(self, size, source = None, opts = DOUBLEBUF):
		"""		ZoomScreen( size [,source [,options]] )   -->   None

		This is intended to be the main screen, the one usually returned
		by display.set_mode()
		Therefore, it takes mostly the same arguments as set_mode()does, with
		the optional addition of a specified source surface.

		The source surface defaults to None, which is really useless unless you
		set_source() soon after...

		This was written mainly with the intent of making small-scale graphics
		work visible while debugging, although I think it could also be used
		to show a miniature of a large surface, instead.  (eg: an inset map of
		the whole world while one sector of it is on screen)

		Possibly useless technical note:  if given a tuple, this function will
		use the transform.scale() function, or if given a scaling factor, will
		use tranform.rotozoom() (with rotation==0)
		"""
		pygame.init()
		try:
			if len(size) == 2:
				self.size = size
			elif len(size) == 4:
				self.size == size[-2:]
			else:
				self.size = size[:2]
		except TypeError:
			self.size = float(size)
		self.img = display.set_mode( self.size, opts )
		if source:
			self.source = source
		else:
			self.source = Surface( (0,0) )

	def set_source(self, src):
		if type(src) == pygame.SurfaceType:
			self.source = src
		self.draw()
		return

	def draw(self):
		"""		ZoomScreen.draw()   -->  None
		"""
		try:
			len(self.size)
			self.img.blit( scale(self.source, self.size),(0,0) )
		except TypeError:
			self.img.blit( rotozoom(self.source, 0, self.size),(0,0) )
		return



class ZSurface( pygame.Surface ):
	"""		Mostly like any other Surface, with a few extra methods for zoom-related 
	actions.  Scales the ZSurface to any arbitrary size requested, when drawing. 
	
	The ZSurface itself remains a constant size, acting just like a normal Surface; 
	it only scales its draw() output.
	
	New member variables are:
		zoomsize 				# most recent requested size
		_aspect_ratio			# (read-only) current aspect ratio 

	Any Surface inquiries having to do with size will answer with actual sizes,
	not zoomed ones.	
	"""

	def __init__(self, *argv):
		Surface.__init__(self, argv)
		self.zoomsize = None
		if self.get_height() != 0:
			self._aspect_ratio = float(self.get_width()) / float(self.get_height())
		else:
			self._aspect_ratio = None
			
	def get_aspect_ratio(self):
		"""		ZSurface.get_aspect_ratio()  -->  float or None
		
		This method returns this ZSurface's aspect ratio, which is its width divided
		by its height ( w/h ).  If height is zero, (ie, divide-by-zero trouble) the 
		aspect ratio is redefined as None.
		"""
		return self._aspect_ratio
		
	def check_ratio(self, src, acceptable = 0.1):
		"""		ZSurface.check_ratio( src [, acceptable_distortion] )  -->  int

		Designed as a small convenience, this method will compare the aspect 
		ratios of this ZSurface and the given src Surface.  If the difference 
		between them is a float within an acceptable range, 0.1 (10%) by 
		default, this returns a 1, giving back a 0 if the distortion is too 
		great.  
		
		If either Surface has an aspect ratio of None, it's certainly a bad 
		match, so it will simply return 0.
		
		This function is best called _before_ blitting a Surface to this one.  
		Otherwise, you could mistakenly blit a 10x75 Surface into, say, a 
		320x480 ZSurface, with appropriately disasterously ugly stretchy 
		results.
		However, squeezing a 180x200 Surface into a 170x190 ZSurface shouldn't 
		work out too badly (it's less than 1% distortion).

		Note that this function won't prevent you from doing such a (possibly) 
		foolish thing, if you want to.  Its sole purpose is to check beforehand.
		"""
		if self._aspect_ratio == None:
			return 0
		else:
			if is_instance( src, ZSurface ):
				othrAR = ZSurface.get_aspect_ratio()
				if othrAR == None:
					return 0
			else:
				x, y = src.get_size()
				if y== 0 or x==0:
					return 0
				else:
					othrAR = float(x)/float(y)
			ratio_diff = self._aspect_ratio - othrAR
			if abs( ratio_diff ) <= acceptable:
				return 1
			else:
				return 0

	def draw(self, (wide,high)=(0,0) ):
		"""		ZSurface.draw( [ (width,height)=(0,0) ] )    -->  Surface
		
		This function is for output only.  Big surprize.
		
		Called without arguments, it will return a copy of this ZSurface
		in its last known dimensions.  That is, if you haven't ever resized it,
		it will return in original size, but if you asked it to draw itself at,
		say, 320x200, each subsequent call will return a Surface of 320x200, 
		until you specify otherwise.
		
		This method will optionally take 1 argument, a length==2 sequence to 
		designate the desired return size (which will then be its default size).
		
		In the future, I think I'll also make it support RectType arguments, but
		it doesn't yet.  Sorry.
		"""
		if (wide == 0) and (high == 0):
			if self.zoomsize:
				zsize = self.zoomsize
			else:
				zsize = self.get_size()
		elif (wide == 0) or (high == 0):
			if self.zoomsize:
				if wide == 0:
					wide == self.zoomsize[0]
				else:
					high == self.zoomsize[1]
				self.zoomsize = [wide,high]
			else:		
				if wide == 0:
					wide == self.get_width()
				else:
					high == self.get_height()
				self.zoomsize = [wide,high]
			zsize = self.zoomsize
		else:	
			self.zoomsize = [wide,high]
			zsize = None
		if zsize:
			return scale( self, zsize )
		else:
			return self







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
         #  self.size += 3
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
        #screen.blit(self.image,(self.x-self.r,self.y-self.r))

        #----NON IMAGE DRAWING TECHNIQUE-----#
        ballBorder = 3
        pygame.draw.circle(screen, BLACK, (int(self.x),int(self.y)), self.r, ballBorder)
        pygame.draw.circle(screen, BLUE, (int(self.x),int(self.y)), self.r-ballBorder, 0)

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
        orig_coords = [self.x,self.y]
        line_vec = [line[1][0] - line[0][0], line[1][1] - line[0][1]]
        ball_vec = [self.dx,self.dy]
        if(line_vec[0] == 0):#check for horizontal and vertical cases
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
        self.x = orig_coords[0]
        self.y = orig_coords[1] 
                 
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
            drawSquare([x,y])# DRAWS A SMALL SQUARE AT THE EXPECTED POINT OF INTERSECTION OF THE BALL AND THE LINE
            distance = dist([self.x,self.y],[x,y])
        if(distance<=self.r):
            self.bounce(line)
    def Check(self,line):#MAKE A BETTER BORDER CHECKING AREA ... THIS IS BAD TOWARDS THE EDGES
        #pygame.draw.rect(screen, color, (x,y,width,height), thickness)
        xdif = abs(line[0][0]-self.x)+abs(line[1][0] - self.x)#+2*self.r
        ydif = abs(line[0][1]-self.y)+abs(line[1][1] - self.y)#+2*self.r 
        ''' Draw border of checking area
        if((line[0][1]-line[1][1]>0)):
            pygame.draw.rect(screen,BLACK,(line[0][0]-self.r,line[1][1]-self.r,abs(line[0][0]-line[1][0])+2*self.r,abs(line[0][1]-line[1][1])+2*self.r),2)
        else:
            pygame.draw.rect(screen,BLACK,(line[0][0]-self.r,line[0][1]-self.r,abs(line[0][0]-line[1][0])+2*self.r,abs(line[0][1]-line[1][1])+2*self.r),2)
        '''
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

def ballCollide(b1,b2):
    distance = b1.r + b2.r + 3
    if(distance >= dist([b1.x,b1.y],[b2.x,b2.y])):
        intersection = [b1.r/distance *(b2.x - b1.x) + b1.x , b1.r/distance * (b2.y - b1.y) + b1.y]
        if(b1.go):#to check if balls are stationary
            b1.bounce([[intersection[0] - b1.x , -1 * (intersection[1] - b1.y)],[0,0]])
        if(b2.go):
            b2.bounce([[intersection[0] - b2.x , -1 * (intersection[1] - b2.y)],[0,0]])
  
def checkBallCollide(collection):
    if(pygame.key.get_pressed()[K_SEMICOLON]!=1):
        max_len = len(collection)
        for n in range(max_len):
            for m in range(max_len-n-1):
                ballCollide(collection[n],collection[(max_len - m - 1)])
                
            
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
    checkBallCollide(ball_collec)
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
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
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

ball_collec = [Ball(x,y,dx,dy),Ball(y,x,dx,dy),Ball(100,x,dx,dy),Ball(300,x,dx,dy)]

    
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
   
