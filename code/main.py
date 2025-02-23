import pygame, sys, math, random
from pygame.locals import *
pygame.init()
 
# Colours
BACKGROUND = (0, 0, 0)
 
# Game Setup
FPS = 60
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
 
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('My Game!')

randSpawn = random.randint(1,2)

SPAWNMISSILE = pygame.USEREVENT
pygame.time.set_timer(SPAWNMISSILE, random.randint(1000, 2000))

# source for missles fired during a level
missileList = []


class ALine():
    def __init__(self):
        self.x_pos = random.randint(20, WINDOW_WIDTH - 20)
        self.startPos = pygame.Vector2((self.x_pos, 0))
        self.endPos = pygame.Vector2((self.x_pos, 0))
        x_f = random.randint(20, WINDOW_WIDTH - 20)
        self.final_pos = pygame.Vector2((x_f, WINDOW_HEIGHT))
        self.add_x, self.add_y = self.calcAngle(self.startPos, self.final_pos)

    # angle from top x_y loc to bottom x_y loc    
    def calcAngle(self, s_Pos, e_Pos):
        x = e_Pos[0] - s_Pos[0]
        y = e_Pos[1] - s_Pos[1]
        angle = math.atan2(y, x)

        x_dir = math.cos(angle)
        y_dir = math.sin(angle)
        return x_dir, y_dir
    

    def drawLine(self, screen):
        pygame.draw.line(screen, "yellow", self.startPos, self.endPos, 5)
        self.endPos[0] += self.add_x
        self.endPos[1] += self.add_y

# replace this with flack explosion method - only utilize main while loop
def misExplosion(endPos):
    for i in range(1000):
        rad = i/10
        pygame.draw.circle(WINDOW, 'red', endPos, rad)
    

class Flack:
    def __init__(self, m_x, m_y):
        self.start_loc = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
        self.f_x, self.f_y = self.start_loc
        self.add_x, self.add_y = self.calcAngle(self.start_loc, (m_x, m_y))
        self.color = 'cyan'
        # location of mouse at click
        self.m_x = m_x
        self.m_y = m_y
        # variables to try and slow down explosion
        self.f_speed = 0
        self.x_t = 0
        self.sx_t = 0
        self.blowUpYes = False # allow explosion
        self.beginOfEnd = False

    # angle from start location to mouse pointer at click time
    def calcAngle(self, s_Pos, e_Pos):
        x = e_Pos[0] - s_Pos[0]
        y = e_Pos[1] - s_Pos[1]
        angle = math.atan2(y, x)

        x_dir = math.cos(angle)
        y_dir = math.sin(angle)
        return x_dir, y_dir

    def create_flack(self):
        self.endLoc = pygame.mouse.get_pos()
        self.flk = pygame.draw.rect(WINDOW, self.color, (self.f_x, self.f_y, 5,5))
        
    def move(self):
        if abs(self.f_x - self.m_x) < 1 and abs(self.f_y -self.m_y) < 1:
            self.f_x = self.m_x
            self.f_y = self.m_y
        else:
            self.f_x += self.add_x
            self.f_y += self.add_y
        
    def exp_timer(self, x_t, sx_t):
        x_timer = x_t
        x_timer += 1
        sx_timer = sx_t
        if x_timer % 2 == 0:
            # print('x timer: ', x_timer, ' sx timer: ', sx_timer)
            sx_timer += 1
        return x_timer, sx_timer

    def explode(self):        
        self.x_t, self.sx_t = self.exp_timer(self.x_t, self.sx_t)
        pygame.draw.circle(WINDOW, self.color, (self.f_x, self.f_y), self.sx_t)

        if self.x_t > 100:
            self.beginOfEnd = True
        
        # print("x_t: ", self.x_t, "blow up: ", self.blowUpYes)
        
    def update(self):
        # print('position: ', math.ceil(self.f_x), math.ceil(self.f_y), '(', self.m_x, self.m_y, ')')
        if abs(self.f_x - self.m_x) < 1 and abs(self.f_y -self.m_y) < 1:
            self.blowUpYes = True
            # print('arrived!!!')
        if self.blowUpYes == True:
            self.explode()
        

flackList = []

flack1 = Flack(200,200)



# The main function that controls the game
def main () :
    looping = True
    time_to_fire = False
  
    # The main game loop
    while looping :
        # Get inputs
        for event in pygame.event.get() :
            if event.type == QUIT :
                pygame.quit()
                sys.exit()
            if event.type == SPAWNMISSILE:
                time_to_fire = True
            if event.type == MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                flackList.append(Flack(m_x, m_y))

    
        # Processing
        # This section will be built out later


        # Render elements of the game
        WINDOW.fill(BACKGROUND)

        if time_to_fire == True:
            missileList.append(ALine())
            time_to_fire = False

        for m in missileList:
            if len(missileList) > 0:
                m.drawLine(WINDOW)
            if m.endPos[1] > WINDOW_HEIGHT:
                print("index: ", missileList.index(m))
                misExplosion(m.endPos)
                missileList.remove(m) # erase missile trail


        for f in flackList:
            if len(flackList) > 0:
                f.create_flack()
                f.move()
            if f.beginOfEnd == True and f.blowUpYes == True:
                flackList.remove(f)
            f.update()
            

        # pressed = pygame.key.get_pressed()
        # if pressed[pygame.K_SPACE]:
        #     print("f list: ", len(flackList))

        flack1.create_flack()

        pygame.display.update()
        
        fpsClock.tick(FPS)
 
main()








    # maybe a swarm tower defense
    # fight swarms (and eventually fight with swarms)
    # just add vulnerabilities - characters that give benefits but also cause loss
    #       must keep them alive?
    #       a drone iv bag


    # part of the crafting optional game
    # spell casting might require an entire shelf of potions or a pylactory
    # teleporting all these items possible, but obviously risky and cumbersome






# class Missle():
#     def __init__(self,x, direction, speed):
    
#         # lines fall from random spots on the top screen and head towards a randomish spot on the bottom screen
#         # city skyline
#         # mouse sets a target point that an explosion instantiates at
#         self.direction = math.radians(direction)
#         self.speed = speed
#         self.mStartPos = pygame.Vector2(random.randint(10, 395), 50)
#         self.mEndPos = pygame.Vector2(self.mStartPos[0], self.mStartPos[1])
#         # self.x_speed = random.randint(-2, 2) * 0.05
#         # self.y_speed = random.randint(1, 5) * 0.05
  
#     def drawMissile(self):
#         pygame.draw.line(WINDOW, "white", self.mStartPos, self.mEndPos, width = 5)
#         while self.mEndPos[1] < WINDOW_HEIGHT:
#             # print("mEndPos: ", self.mEndPos)
#             self.mEndPos[0] += 0.05
#             self.mEndPos[1] += 0.5


#     def update(self):
#         self.drawMissile()




# missileList[0].drawLine(WINDOW)     # works
# aLine.drawLine(WINDOW)              # works

# if len(missileList) > 0:
#     # print("firing!!!")
#     missileList[0].drawLine(WINDOW)         # works




# def instMissle(self):
    #     self.missle_list.append(ALine())
        # self.x_pos = random.randint(20, WINDOW_WIDTH - 20)
        # self.startPos = pygame.Vector2((self.x_pos, 0))
        # self.endPos = pygame.Vector2((self.x_pos, 0))
        # x_f = random.randint(20, WINDOW_WIDTH - 20)
        # self.final_pos = pygame.Vector2((x_f, WINDOW_HEIGHT))
        # self.add_x, self.add_y = self.calcAngle(self.startPos, self.final_pos)



        # def createAngles(self, x_pos, y_pos):
    #     self.startPos = pygame.Vector2((x_pos, y_pos))
    #     self.endPos = pygame.Vector2((x_pos, y_pos))
    #     self.final_pos = pygame.Vector2((20, 800))
    #     self.add_x, self.add_y = self.calcAngle(self.startPos, self.final_pos)

    # def drawLine(self, screen, x_sp, y_sp):
    #    self.x_sp = x_sp
    #    self.y_sp = y_sp
    #    pygame.draw.line(screen, "yellow", self.startPos, self.endPos, 10)
    #    self.endPos[0] += self.x_sp
    #    self.endPos[1] += self.y_sp