"""This is a template Python file.
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

# Local Application/Library Specific Imports ------------------------
import gametime
import animatedobject
import ioprocess # io handling

#------------------------------------------------------------------------------
# Global Variables for Export ---------------------------------------

# Global Variables for use Inside the Module ------------------------

#------------------------------------------------------------------------------
class Game():
    def __init__(self):
        pygame.init()
        self._screen = pygame.display.set_mode((800,600), \
            pygame.DOUBLEBUF+pygame.HWSURFACE)

        self.time = gametime.GameTime()
        self.tstobj = animatedobject.createAnimatedObject('../assets/knight','object.ini')
        self.knight = animatedobject.AnimationState(self.tstobj)
        self.knight.changeAnimation('stopped')
        self.knight.changeDirection(0)

        self.iohandler = ioprocess.IOFunctions(self)

    def processInputs(self):
        self.iohandler.handleEvents(pygame.event.get())
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         sys.exit()
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_ESCAPE:
        #             sys.exit()

    def update(self):
        self.time.update()

    def draw(self):
        frame = self.knight.getFrame(self.time.time())
        self._screen.blit(frame,frame.get_rect())
        #self._screen.fill((0,0,0))
        #self._screen.blit(self._ball,self._ball.get_rect())
        #self._screen.blit(self._square, (150,45))
        #flip
        pygame.display.flip()
