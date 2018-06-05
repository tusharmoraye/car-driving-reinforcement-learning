import pygame, random, sys ,os,time
from pygame.color import THECOLORS
from pygame.locals import *
import numpy as np
import math


WINDOWWIDTH = 800
WINDOWHEIGHT = 600
TEXTCOLOR = (255, 255, 255)
BACKGROUNDCOLOR = (0, 0, 0)
FPS = 1000
BADDIEMINSIZE = 10
BADDIEMAXSIZE = 20
BADDIEMINSPEED = 8
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 20
PLAYERMOVERATE = 5
angle = 3.142/2
training_data = []


#arraySave=np.load('coordinates.npy')
arraySave=np.load('new.npy')
#arraySave = []
arrInd = 0
arrLen = len(arraySave)

'''
count=1
score=0
baddieAddCounter =0
moveLeft=False
moveRight=False
baddies=[]
'''

# set up pygame, the window, and the mouse cursor
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('car race')
pygame.mouse.set_visible(False)



class GameState:
    def terminate(self):
        pygame.quit()
        sys.exit()

    def waitForPlayerToPressKey(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE: #escape quits
                        terminate()
                    return

    def playerHasHitBaddie(self, playerRect, baddies):
        for b in baddies:
            if playerRect.colliderect(b['rect']):
                return True
        return False

    def drawText(self, text, font, surface, x, y):
        textobj = font.render(text, 1, TEXTCOLOR)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    def sum_readings(self, readings):
        """Sum the number of non-zero readings."""
        tot = 0
        for i in readings:
            tot += i
        return tot

    def get_sonar_readings(self, playerRect, angle):
        readings = []
        """
        Instead of using a grid of boolean(ish) sensors, sonar readings
        simply return N "distance" readings, one for each sonar
        we're simulating. The distance is a count of the first non-zero
        reading starting at the object. For instance, if the fifth sensor
        in a sonar "arm" is non-zero, then that arm returns a distance of 5.
        """
        # Make our arms.

        #1:upword 2:left 3:right

        x, y, w, h = self.playerRect
        arm_topleft = self.make_sonar_arm(x, y, 2)
        arm_topright = self.make_sonar_arm(x + w, y, 3)
        arm_frontleft = self.make_sonar_arm(x, y, 1)
        arm_front = self.make_sonar_arm(x+int(w/2), y, 1)
        arm_frontright = self.make_sonar_arm(x+w, y, 1)
        arm_bottomleft = self.make_sonar_arm(x, y+h-10, 2)
        arm_bottomright = self.make_sonar_arm(x+w, y+h-10, 3)

        # Rotate them and get readings.
        readings.append(self.get_arm_distance(arm_topleft, x, y, angle, 0))
        readings.append(self.get_arm_distance(arm_topright, x + w, y, angle, 0))
        readings.append(self.get_arm_distance(arm_frontleft, x, y, angle, 1.7453))
        readings.append(self.get_arm_distance(arm_front, x+int(w/2), y, angle, 0))
        readings.append(self.get_arm_distance(arm_frontright, x+w, y, angle, 1.396))
        readings.append(self.get_arm_distance(arm_bottomleft, x, y+h-10, angle, 0))
        readings.append(self.get_arm_distance(arm_bottomright, x+w, y+h-10, angle, 0))


        pygame.display.update()

        return readings

    def make_sonar_arm(self, x, y, direction):
        spread = 6  # Default spread.
        distance = 2  # Gap before first sensor.
        arm_points = []
        # Make an arm. We build it flat because we'll rotate it about the
        # center later.

        if direction == 1:
            for i in range(1, 60):
                arm_points.append((x, (y - distance - (spread * i))))
        elif direction == 2:
            for i in range(1, 60):
                arm_points.append((x - distance - (spread * i), y))
        elif direction == 3:
            for i in range(1, 60):
                arm_points.append((distance + x + (spread * i), y))
        #print()
        #print(arm_points)
        #print()
        return arm_points

    def get_arm_distance(self, arm, x, y, angle, offset):
        # Used to count the distance.
        i = 0

        # Look at each point and see if we've hit something.
        for point in arm:
            i += 1

            # Move the point to the right spot.
            #rotated_p = self.get_rotated_point(
            #    x, y, point[0], point[1], angle + offset
            #)
            if(offset != 0):
                rotated_p = self.get_rotated_point(
                    x, y, point[0], point[1], angle + offset
                )
            else:
                rotated_p = point
            # Check if we've hit something. Return the current i (distance)
            # if we did.
            #print(rotated_p)
            if rotated_p[0] <= 100 or rotated_p[1] <= 0 \
                    or rotated_p[0] >= 500 or rotated_p[1] >= WINDOWHEIGHT:
                return i  # Sensor is off the screen.
            else:
                obs = windowSurface.get_at(rotated_p)
                if self.get_track_or_not(obs) != 0:
                    return i
            #print(obs)
            #if show_sensors:
            pygame.draw.circle(windowSurface, (255, 255, 255), (rotated_p), 1)

        # Return the distance for the arm.
        return i

    def get_track_or_not(self, reading):
        if reading == THECOLORS['black']:
            return 0
        else:
            return 1

    def get_rotated_point(self, x_1, y_1, x_2, y_2, radians):
            # Rotate x_2, y_2 around x_1, y_1 by angle.
            x_change = (x_2 - x_1) * math.cos(radians) + \
                (y_2 - y_1) * math.sin(radians)
            y_change = (y_1 - y_2) * math.cos(radians) - \
                (x_1 - x_2) * math.sin(radians)
            new_x = x_change + x_1
            new_y = WINDOWHEIGHT - (y_change + y_1)
            new_x = ((x_2-x_1)*math.cos(radians)-(y_2-y_1)*math.sin(radians)) + x_1
            new_y = y_1 - ((x_2-x_1)*math.sin(radians)+(y_2-y_1)*math.cos(radians))
            return int(new_x), int(new_y)



    def __init__(self):
        
        # fonts
        self.font = pygame.font.SysFont(None, 30)

        # sounds
        self.gameOverSound = pygame.mixer.Sound('music/crash.wav')
        pygame.mixer.music.load('music/car.wav')
        self.laugh = pygame.mixer.Sound('music/laugh.wav')
        self.count=1
        self.score = 0
        self.gameEnd = False
        # images
        self.playerImage = pygame.image.load('image/car1.png')
        self.car3 = pygame.image.load('image/car3.png')
        self.car4 = pygame.image.load('image/car4.png')
        self.playerRect = self.playerImage.get_rect()
        self.baddieImage = pygame.image.load('image/car2.png')
        self.sample = [self.car3,self.car4,self.baddieImage]
        self.wallLeft = pygame.image.load('image/left.png')
        self.wallRight = pygame.image.load('image/right.png')

        arrInd = 0
        # "Start" screen
        #self.drawText('Press any key to start the game.', self.font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3))
        #self.drawText('And Enjoy', self.font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3)+30)
        pygame.display.update()
        #self.waitForPlayerToPressKey()
        zero=0
        if not os.path.exists("data/save.dat"):
            f=open("data/save.dat",'w')
            f.write(str(zero))
            f.close()   
        v=open("data/save.dat",'r')
        self.topScore = int(v.readline())
        v.close()
        # start of the game
        self.baddies = []
        self.score = 0
        self.playerRect.topleft = ((140+485) / 2, WINDOWHEIGHT - 50)
        self.moveLeft = self.moveRight = self.moveUp = self.moveDown = False
        self.reverseCheat = self.slowCheat = False
        self.baddieAddCounter = 0
        #pygame.mixer.music.play(-1, 0.0)



    def recover_from_crash(self):
        self.__init__()


    def frame_step(self, inputStep):

        global arrInd
        self.score += 1 # increase score

        for event in pygame.event.get():
            
            if event.type == QUIT:
                self.terminate()

        if inputStep == 0:
            pass
        if inputStep == 1:
            self.moveRight = False
            self.moveLeft = True
        if inputStep == 2:
            self.moveLeft = False
            self.moveRight = True
            

        # Add new baddies at the top of the screen
        self.baddieAddCounter += 1
        if self.baddieAddCounter == ADDNEWBADDIERATE:
            self.baddieAddCounter = 0
            self.baddieSize =30 
            sampleInd = random.randint(0, 2)

            
            if arrInd >= arrLen:
                arrInd = 0
            newBaddie = {
                        #'rect': pygame.Rect(random.randint(140, 485), 0 - self.baddieSize, 23, 47),
                        'rect': pygame.Rect(arraySave[arrInd][0][0], arraySave[arrInd][0][1], 23, 47),
                        'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                        #'surface':pygame.transform.scale(random.choice(self.sample), (23, 47)),
                        'surface':pygame.transform.scale(self.sample[arraySave[arrInd][1]], (23, 47)),                        
                        }
            #arraySave.append
            #arraySave.append( [np.array(newBaddie['rect'].topleft), sampleInd] )
            arrInd += 1;
            self.baddies.append(newBaddie)
            sideLeft= {'rect': pygame.Rect(0,0,126,600),
                       'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                       'surface':pygame.transform.scale(self.wallLeft, (126, 599)),
                       'type': 'wall'
                       }
            self.baddies.append(sideLeft)
            sideRight= {'rect': pygame.Rect(497,0,303,600),
                       'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                       'surface':pygame.transform.scale(self.wallRight, (303, 599)),
                       'type': 'wall'
                       }
            self.baddies.append(sideRight)
            
            

        # Move the player around.
        if self.moveLeft and self.playerRect.left > 0:
            self.playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if self.moveRight and self.playerRect.right < WINDOWWIDTH:
            self.playerRect.move_ip(PLAYERMOVERATE, 0)
        
        for b in self.baddies:
            b['rect'].move_ip(0, b['speed'])
            

         
        for b in self.baddies[:]:
            if b['rect'].top > WINDOWHEIGHT:
                self.baddies.remove(b)

        # Draw the game world on the window.
        windowSurface.fill(BACKGROUNDCOLOR)

        # Draw the score and top score.
        self.drawText('Score: %s' % (self.score), self.font, windowSurface, 128, 0)
        self.drawText('Top Score: %s' % (self.topScore), self.font, windowSurface,128, 20)
        self.drawText('Rest Life: %s' % (self.count), self.font, windowSurface,128, 40)
        
        windowSurface.blit(self.playerImage, self.playerRect)

        
        for b in self.baddies:
            windowSurface.blit(b['surface'], b['rect'])


        self.readings = self.get_sonar_readings(self.playerRect, angle)

        pygame.display.update()

        # Check if any of the car have hit the player.
        #if playerHasHitBaddie(playerRect, baddies):
        if 1 in self.readings:
            if self.score > self.topScore:
                g=open("data/save.dat",'w')
                g.write(str(self.score))
                g.close()
                self.topScore = self.score
            self.gameEnd = True

        mainClock.tick(FPS)

        normalized_readings = [(x-20.0)/20.0 for x in self.readings] 
        state = np.array([normalized_readings])
        
        # Set the reward.
        # Car crashed when any reading == 1
        if self.gameEnd:
            arrInd = 0
            reward = -500
            self.recover_from_crash()
        else:
            # Higher readings are better, so return the sum.
            reward = -5 + int(self.sum_readings(self.readings) / 10)

        return reward, state



if __name__ == "__main__":
    game_state = GameState()
    while True:
        reward, state = game_state.frame_step((random.randint(0, 2)))
        print(reward, state)

