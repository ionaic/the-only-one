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
import game as _game

#------------------------------------------------------------------------------
# Global Variables for Export ---------------------------------------
game = _game.Game()
# Global Variables for use Inside the Module ------------------------

# timing init
ticks = 0
framestart = 0
frames = 0

#------------------------------------------------------------------------------

try:
    while True:
        # timing code
        framestart = pygame.time.get_ticks()
        frames = frames +1
        if framestart >= ticks + 1000:
            print ((framestart-ticks)*.0001)*frames
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
except:
    pygame.quit()
    raise
