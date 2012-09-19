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
import cProfile
import pstats

# 3'rd Party Imports ------------------------------------------------
import pygame

# Local Application/Library Specific Imports ----------------------------
import game as _game
import terrain
import interactions

#------------------------------------------------------------------------------
# Global Variables for Export ---------------------------------------

# Global Variables for use Inside the Module ------------------------



#------------------------------------------------------------------------------

def menu():
    screen = _game.Game.universal._screen
    old = pygame.Surface((800,600))
    old.blit(screen,(0,0))

    menu = [pygame.image.load('../assets/Title0001.png').convert(), \
            pygame.image.load('../assets/Title0002.png').convert(), \
            pygame.image.load('../assets/Title0003.png').convert()]
    index = 0
    credits = pygame.image.load('../assets/Credits.png').convert()
    go = True
    onCredits = False
    screen.blit(menu[index%3],(0,0))
    while go:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    if onCredits==True:
                        onCredits = False
                        screen.blit(menu[index%3],(0,0))
                        continue
                    sys.exit()
                if event.key==pygame.K_UP or event.key==pygame.K_w or event.key==pygame.K_j:
                    index = index-1
                    screen.blit(menu[index%3],(0,0))
                    onCredits=False
                if event.key==pygame.K_DOWN or event.key==pygame.K_s or event.key==pygame.K_k:
                    index = index+1
                    screen.blit(menu[index%3],(0,0))
                    onCredits=False
                if event.key==pygame.K_RETURN or event.key==pygame.K_SPACE:
                    if onCredits==True:
                        screen.blit(menu[index%3],(0,0))
                        onCredits=False
                        continue
                    if index%3==2:
                        sys.exit()
                    elif index%3==1:
                        screen.blit(credits,(0,0))
                        onCredits = True
                    else:
                        go=False
                        
        pygame.display.flip()
        
    screen.blit(old,(0,0))
def loss():
    screen = _game.Game.universal._screen
    old = pygame.Surface((800,600))
    old.blit(screen,(0,0))

    index = 0
    loss_screen = pygame.image.load('../assets/GameOver.png').convert()
    go = True
    onCredits = False
    screen.blit(loss_screen,(0,0))
    while go:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    sys.exit()
                if event.key==pygame.K_RETURN or event.key==pygame.K_SPACE:
                    sys.exit()
                        
        pygame.display.flip()
def victory():
    screen = _game.Game.universal._screen
    old = pygame.Surface((800,600))
    old.blit(screen,(0,0))

    index = 0
    loss_screen = pygame.image.load('../assets/YouWin.png').convert()
    go = True
    onCredits = False
    screen.blit(loss_screen,(0,0))
    while go:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    sys.exit()
                if event.key==pygame.K_RETURN or event.key==pygame.K_SPACE:
                    sys.exit()
                        
        pygame.display.flip()    
def main():
    game = _game.Game()
    # timing init
    ticks = 0
    framestart = 0
    frames = 0
    try:
        menu()
        while True:
            # timing code
            framestart = pygame.time.get_ticks()
            frames = frames +1
            if framestart >= ticks + 1000:
                print ((framestart-ticks)*.001)*frames
                ticks = framestart
                frames = 0
            # process input
            game.processInputs()
            # update
            game.update()
            # draw
            game.draw()
    except SystemExit:
        pygame.quit()
    except interactions.Loss:
        try:
            loss()
        except SystemExit:
            pygame.quit()
    except interactions.Victory:
        try:
            victory()
        except SystemExit:
            pygame.quit()
    except:
        pygame.quit()
        raise
main()
#cProfile.run('main()','perfstat')
#p = pstats.Stats('perfstat')
#p.strip_dirs().sort_stats('time').print_stats()
