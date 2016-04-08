import pygame
import sys
import random
from pygame.locals import *

#-----------initializers-----------------
pygame.init()

screen = pygame.display.set_mode((1200, 700))
clock = pygame.time.Clock()
sound_lib = {}

pygame.display.set_caption('Sensory Underload')

#-------------sound stuff--------------------

songs = ['jungleMusic.mp3','punk.mp3']
currentSong = 'assets/' + songs[0]
pygame.mixer.music.load(currentSong)
SONG_END = pygame.USEREVENT + 1 # USEREVENT has the highest value of the enum
pygame.mixer.music.set_endevent(SONG_END)
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.play()
#pygame.mixer.music.queue('assets/crash.mp3')

def play_a_different_song():
    global currentSong,songs
    next_song =  'assets/'+random.choice(songs)
    while next_song == currentSong:
        next_song =  'assets/' + random.choice(songs)
    currentSong = next_song
    pygame.mixer.music.load(next_song)
    pygame.mixer.music.play()

def playSound(path):
    global sound_lib
    sound = sound_lib.get(path)
    if sound is None:
        sound = pygame.mixer.Sound(path)
        sound_lib[path] = sound
    sound.set_volume(0)
    sound.play()
    return sound


#---------- functions ------------------- 

class obstacle():

    def __init__(self,keyToPress,path,windowSize):
        self.keyToPress = keyToPress
        self.path = path
        self.windowSize = windowSize
        self.whooshSound = ''

    def whoosh(self):
        vol = self.whooshSound.get_volume()
        incr = 0.01
        tot = vol+incr
        #print tot
        self.whooshSound.set_volume(tot)
        
    def playSound(self,volume):

        global sound_lib
        sound = sound_lib.get(self.path)
        if sound is None:
            sound = pygame.mixer.Sound(self.path)
            sound_lib[self.path] = sound
        sound.set_volume(volume)
        sound.play()
        self.whooshSound = sound
        

obstacles = [];
gameKeys = []

positive = pygame.mixer.Sound('assets/pickup.wav')
negative = pygame.mixer.Sound('assets/GETBONKED.wav')
negative.set_volume(0.6)
positive.set_volume(0.6)

# Duck
duck = obstacle(pygame.K_DOWN,'assets/flyby.wav',60)
flock = obstacle(pygame.K_DOWN,'assets/birdflap.wav',150)
up = obstacle(pygame.K_UP,'assets/wallsmash.wav',100)

left = obstacle(pygame.K_RIGHT,'assets/pannedLeft.wav',90)
right = obstacle(pygame.K_LEFT,'assets/pannedRight.wav',90)

obstacles.extend([duck,left,right,flock,up])
gameKeys.extend([pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT,pygame.K_UP])

isActive = False
winCount = 1
window = 130
windowMax = 130.0
whooshSound = 0
obstacleKey = ''
lives = 3
score = 0


#positive.play()

def whoosh():
    vol = whooshSound.get_volume()
    incr = 0.01
    tot = vol+incr
    print tot
    whooshSound.set_volume(tot)

def end():
    pygame.quit()
    sys.exit()
    
counter = 0
pushed = False
timeToWait = 120;
decrementmoment = True

# -----------Game Loop ---------------

while True:

    if not isActive and (winCount % timeToWait == 0): 
        obstacleIndex = random.randint(0,len(obstacles)-1)
        obstacle = obstacles[obstacleIndex]
        window = obstacle.windowSize
        obstacle.playSound(0.0)
        isActive = True
        
    winCount += 1

    if isActive:
        window -= 1
        obstacle.whoosh()
    
    keys = pygame.key.get_pressed()

    if isActive:

        if obstacle.path == 'assets/birdflap.wav':

            # If they press the key, uncrement the counter
            if keys[obstacle.keyToPress]:
                pushed = True
                counter += 1
            elif counter > 70:
                print 'yall held it long enough'
                isActive = False
                pushed = False
                score += 1
                positive.play()
                counter = 0
            elif window < 50:
                print 'not long enough yall'
                isActive = False
                pushed = False
                lives -= 1
                negative.play()
                counter = 0

            # # If they press the wrong key, lose a life
            # for key in gameKeys:
            #     if (not key == obstacle.keyToPress) and (keys[key]):
            #         print 'yall goofed'
            #         lives-=1
            #         isActive = False
            #         pushed = False
            #         negative.play()
            #         break
            
        else:    
            if keys[obstacle.keyToPress]:
                if isActive and (window > 0):# and window < 50):
                    print 'yall hit it'
                    decrementMoment = True
                    score+=1
                    isActive = False
                    positive.play()
                else:
                    print 'yall missed'
                    isActive = False
                    lives -= 1
                    negative.play()
            else:
                for key in gameKeys:
                    if (not key == obstacle.keyToPress) and (keys[key]):
                        print 'yall pressed the wrong key'
                        lives-=1
                        isActive = False
                        negative.play()
                        break
        
    if keys[pygame.K_ESCAPE]:
        end()
            
    if isActive and window <= 0:
        negative.play()
        isActive = False
        lives -= 1

    if lives == 0:
        print 'yall lost'
        end()

    if score % 5 == 0 and score != 0 and decrementMoment == True:
        timeToWait -=30
        decrementMoment = False
        print timeToWait

    if score == 20:
        print 'you win!'
        end()

    pygame.display.flip()
    
    #60 FPS
    clock.tick(30)
    pygame.event.pump()
