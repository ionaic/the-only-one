"""This is a test pygame application.
Python Version: 2.7.3
Author: Matthew McMullan

Description: This template was made using best practices from...
http://www.python.org/dev/peps/pep-0008/
http://www.python.org/dev/peps/pep-0257/

"""
#------------------------------------------------------------------------------
# Standard Library Imports ------------------------------------------
import sys

# 3'rd Party Imports ------------------------------------------------
import pygame

# Local Application/Library Specific Imports ----------------------------
import animatedobject
import gametime
#------------------------------------------------------------------------------
# Init
pygame.init()
screen = pygame.display.set_mode((800,600), pygame.DOUBLEBUF+pygame.HWSURFACE)

# Global Variables for Export ---------------------------------------

# Global Variables for use Inside the Module ------------------------

def createCharacter(pos,folder,inifile,animation):
    object = animatedobject.createAnimatedObject(folder,inifile)
    state = animatedobject.AnimationState(object)
    state.setAnimation(animation)
    state.setDirection(0)
    state.setPos(pos[0],pos[1])
    return state

characters = list()
characters.append(createCharacter((0,0),'../assets/tigger','object.ini','stopped'))
characters.append(createCharacter((160,0),'../assets/tigger','object.ini','shoot'))
characters.append(createCharacter((320,0),'../assets/tigger','object.ini','move'))
characters.append(createCharacter((480,0),'../assets/tigger','object.ini','moveshoot'))
characters.append(createCharacter((640,0),'../assets/tigger','object.ini','damaged'))

characters.append(createCharacter((0,160),'../assets/tigger','object.ini','launch'))
characters.append(createCharacter((160,160),'../assets/tigger','object.ini','rocket'))
characters.append(createCharacter((320,160),'../assets/tigger','object.ini','groundpound'))

characters.append(createCharacter((0,320),'../assets/enemies/tigglette (needle)/blue','object.ini','stopped'))

characters.append(createCharacter((640,480),'../assets/static','object.ini','stuffing'))
characters.append(createCharacter((480,480),'../assets/projectiles/button_placeholder','object.ini','move'))
#------------------------------------------------------------------------------

# timing init
ticks = 0
framestart = 0
frames = 0

time = gametime.GameTime()

try:
    background = pygame.Surface((800,600))
    background.fill((191,123,199))
    screen.fill((191,123,199))
    while True:
        # timing code
        framestart = pygame.time.get_ticks()
        frames = frames +1
        if framestart >= ticks + 1000:
            print ((framestart-ticks)*.001)*frames
            ticks = framestart
            frames = 0
        # process input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_DOWN:
                    for character in characters:
                        character.setDirection(0)
                if event.key == pygame.K_LEFT:
                    for character in characters:
                        character.setDirection(2)
                if event.key == pygame.K_UP:
                    for character in characters:
                        character.setDirection(4)
                if event.key == pygame.K_RIGHT:
                    for character in characters:
                        character.setDirection(6)
        # update
        time.update()
        # draw
        #screen.fill((191,123,199))
        for character in characters:
            character.undraw(background,screen,time)
            character.draw(screen,time)
            #frame = character.getFrame(time.time())
            #screen.blit(frame,character.getPos())
        pygame.display.flip()
except SystemExit:
    pygame.quit()
except:
    pygame.quit()
    raise
