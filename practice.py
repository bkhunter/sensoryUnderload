import pygame
import sys
import random
from pygame.locals import *

#-----------initializers-----------------
pygame.init()

screen = pygame.display.set_mode((450, 450))
clock = pygame.time.Clock()
isBlue = True
x = 30
y = 30
size = 60

sound_lib = {}
image_lib = {}

pygame.display.set_caption('Hello World!')

#-----------image/background stuff -------

def get_image(path):
    global image_lib
    image = image_lib.get(path)
    if image is None:
        image = pygame.image.load(path).convert()
        image_lib[path] = image
    return image


#-------------sound stuff--------------------

songs = ['Raining.mp3','punk.mp3']
currentSong = 'assets/' + songs[0]
pygame.mixer.music.load(currentSong)
SONG_END = pygame.USEREVENT + 1 # USEREVENT has the highest value of the enum
pygame.mixer.music.set_endevent(SONG_END)
#pygame.mixer.music.play()
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
def deduct(coord):
    coord -= 6
    if coord < 0:
        return 0
    return coord

def increase(coord):
    coord += 6
    if coord > (450-size):
        return (450-size)
    return coord

isActive = False
winCount = 1000
window = 130
windowMax = 130.0
whooshSound = 0

hit = False

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

    winCount -= 1
    if isActive:
        window -= 1

    if isActive:
        whoosh()
    
    if winCount == 900:
        isActive = True
        whooshSound = playSound('assets/Raining.wav')

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        if isActive and (window > 0 and window < 50):
            print 'you win'
            end()
        elif window <= 0:
            print 'you lose!'
            end()
        else:
            print 'you lose'
            print window
            end()
            
    if window <= 0:
        print 'you lose'
        end()

    if winCount == 0:
        print 'you lose'
        end()

    pygame.display.flip()
    
    #60 FPS
    clock.tick(30)
    pygame.event.pump()


