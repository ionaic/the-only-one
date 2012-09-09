"""This file contains an object that converts between real-time and game-time.
Python Version: 2.7.3
Author: Matthew McMullan

Description: This template was made using best practices from...
http://www.python.org/dev/peps/pep-0008/
http://www.python.org/dev/peps/pep-0257/

"""
#------------------------------------------------------------------------------
# Standard Library Imports ------------------------------------------

# 3'rd Party Imports ------------------------------------------------
import pygame

# Local Application/Library Specific Imports ------------------------

#------------------------------------------------------------------------------
# Global Variables for Export ---------------------------------------

# Global Variables for use Inside the Module ------------------------

#------------------------------------------------------------------------------

class GameTime():
    def __init__(self):
        self.lastReal = pygame.time.get_ticks()
        self.gameTime = 0
        self.conversion = 1.0
        self.paused = False
    def update(self):
        if (self.paused == False):
            ticks = pygame.time.get_ticks()
            diff = ticks-self.lastReal
            self.gameTime += diff*self.conversion
            self.lastReal = ticks
    def pause(self):
        self.paused = True
    def resume(self):
        self.paused = False
        self.lastReal = pygame.time.get_ticks()
    def time(self):
        return self.gameTime
