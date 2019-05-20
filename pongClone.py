import pygame
import random
from vec2d import *

#todo: paddles can move at same time, ball interact with paddles, opponent AI
#todo: fix score moving more than 1 at a time.

white=(255,255,255)
black=(0,0,0)
green = (0, 255, 0)
orange = (255,140,0)

winW=640
winH=480
paddleWidth=6
paddleHeight=60
paddleVel=5
ballWidth=10
score1=0
score2=0
fps=pygame.time.Clock()

def playerServe(right):
    global ballVel
    horz=random.randrange(2,4)
    vert=random.randrange(1,3)
    if(right==False):
        horz= -horz
    ballVel=[horz,-vert]

def setUp():
    global player1, player2, ball
    player1=Player(paddleWidth*2,winH//2)
    player2=Player(winW-(paddleWidth*2)-paddleWidth,winH//2)
    if(random.randrange(0,2)==0):
        playerServe(True)
    else:
        playerServe(False)
    ball=Ball(winW//2,winH//2,ballVel,2)

class Player():
    def __init__(self, x, y):
        self.x=x
        self.y=y
        pygame.draw.rect(screen, white, (self.x,self.y,paddleWidth,paddleHeight))

    def drawPlayer(self):
        pygame.draw.rect(screen, white, (self.x,self.y,paddleWidth,paddleHeight))

    def movePlayer(self,locY):
        if(locY!=0):
            self.y+=locY
            if(self.y<0):
                self.y+=paddleVel
            elif(self.y>(winH-50)):
                self.y-=paddleVel

class Ball():
    #ball=Ball(winW//2,winH//2,random.randint(0,3),random.randint(0,3),2)
    def __init__(self, x, y, ballVel, speed):
        self.x=x
        self.y=y
        self.direction=Vec2d(ballVel[0],ballVel[1])
        self.pos=Vec2d(self.x,self.y)
        self.Xbvel=speed
        self.Ybvel=speed
        pygame.draw.circle(screen,white,self.pos,ballWidth)

    def drawBall(self):
        pygame.draw.circle(screen,white,self.pos,ballWidth)

    def update(self): #needs work
        displacement = Vec2d(
            self.direction.x * self.Xbvel,
            self.direction.y * self.Ybvel)
        self.pos += displacement
        bounds_rect = screen.get_rect()
        if self.pos.x < bounds_rect.left:#player 1 goal
            self.pos.x = bounds_rect.left
            #self.direction.x *= -1
            self.direction.y = 0
            checkGoal(bounds_rect.left, ball)
        elif self.pos.x > bounds_rect.right:#player 2 goal
            self.pos.x = bounds_rect.right
            #self.direction.x *= -1
            self.direction.y = 0
            checkGoal(bounds_rect.right, ball)
        elif self.pos.y < bounds_rect.top:
            self.pos.y = bounds_rect.top
            self.direction.y *= -1
        elif self.pos.y > bounds_rect.bottom:
            self.pos.y = bounds_rect.bottom
            self.direction.y *= -1

    def collision(self): #needs work
        global score1, score2
        if int(self.pos[0]) <= ballWidth + paddleWidth and int(self.pos[1]) in range(player1.y - (paddleHeight//2), player1.y + (paddleHeight//2), 1):
            ballVel[0] = -ballVel[0]
            ballVel[0] *= 1.1
            ballVel[1] *= 1.1

        elif int(self.pos[0]) <= ballWidth + paddleWidth:
            score2 += 1
            playerServe(True)

        if int(self.pos[0]) >= winW + 1 - ballWidth - paddleWidth and int(self.pos[1]) in range(player2.y - (paddleHeight//2), player2.y + (paddleHeight//2), 1):
            ballVel[0] = -ballVel[0]
            ballVel[0] *= 1.1
            ballVel[1] *= 1.1
        elif int(self.pos[0]) >= winW + 1 - ballWidth - paddleWidth:
            score1 += 1
            playerServe(False)

def checkGoal(boundary,ball): #needs work
    if(boundary==640):
        screen.fill(black)
        setUp()
    elif(boundary==0):
        screen.fill(black)
        items=setUp()

def draw(screen):
    screen.fill(black)
    pygame.draw.line(screen, white, [winW//2,0],[winW//2,winH],1)
    pygame.draw.line(screen, white, [0,60],[winW,60],1)

    player1.drawPlayer()
    player2.drawPlayer()
    ball.drawBall()
    ball.collision()
    ball.update()

    myfont1 = pygame.font.SysFont("Comic Sans MS", 20)
    label1 = myfont1.render("Score " + str(score1), 1, (255, 255, 0))
    screen.blit(label1, (50, 20))

    myfont2 = pygame.font.SysFont("Comic Sans MS", 20)
    label2 = myfont2.render("Score " + str(score2), 1, (255, 255, 0))
    screen.blit(label2, (470, 20))

def main():
    running=True
    locY=0

    pygame.init()
    pygame.display.set_caption("Pong Clone")
    global screen
    screen=pygame.display.set_mode((winW,winH))
    clock = pygame.time.Clock()
    setUp()
    draw(screen)
    pygame.key.set_repeat(10,10)

    while (running==True):
        draw(screen)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_s:
                    locY+=paddleVel
                    player1.movePlayer(locY)
                    locY=0
                if event.key==pygame.K_w:
                    locY-=paddleVel
                    player1.movePlayer(locY)
                    locY=0
                if event.key==pygame.K_DOWN:
                    locY+=paddleVel
                    player2.movePlayer(locY)
                    locY=0
                if event.key==pygame.K_UP:
                    locY-=paddleVel
                    player2.movePlayer(locY)
                    locY=0
        fps.tick(60)
    pygame.quit()

if __name__=="__main__":
    main()
