import pygame
import sys
import random
from pygame.locals import *

#-----------initializers-----------------
pygame.init()

screen = pygame.display.set_mode((450, 450))
clock = pygame.time.Clock()

sound_lib = {}

pygame.display.set_caption('Hello World!')

#-------------sound stuff--------------------

songs = ['Raining.mp3','punk.mp3']
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
        print tot
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

boingPoing = obstacle(pygame.K_LEFT,'assets/boing_poing.wav',100)
Ahem = obstacle(pygame.K_RIGHT,'assets/test.wav',100)

obstacles.append(boingPoing)
obstacles.append(Ahem)

isActive = False
winCount = 1
window = 130
windowMax = 130.0
whooshSound = 0
obstacleKey = ''
lives = 3
score = 0

def whoosh():
    vol = whooshSound.get_volume()
    incr = 0.01
    tot = vol+incr
    print tot
    whooshSound.set_volume(tot)

def end():
    pygame.quit()
    sys.exit()
    

# -----------Game Loop ---------------


while True:


    if not isActive and (winCount % 300 == 0): 
        obstacleIndex = random.randint(0,len(obstacles)-1)
        obstacle = obstacles[obstacleIndex]
        window = obstacle.windowSize
        obstacle.playSound(0.0)
        isActive = True
        


    winCount += 1
    if isActive:
        window -= 1

    if isActive:
        obstacle.whoosh()
    
    keys = pygame.key.get_pressed()
    if isActive:
        if keys[obstacle.keyToPress]:
            if isActive and (window > 0 and window < 50):
                score+=1
                print score
                isActive = False

            elif window <= 0:
                print 'you lose!'
                end()
            else:
                lives -= 1
    if keys[pygame.K_ESCAPE]:
        end()
            
    if isActive and window <= 0:
        lives -= 1

    if lives == 0:
        end()


    pygame.display.flip()
    
    #60 FPS
    clock.tick(30)
    pygame.event.pump()


