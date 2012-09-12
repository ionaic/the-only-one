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
import terrain

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
        self.tstobj = animatedobject.createAnimatedObject('../assets/tigger','object.ini')
        self.tiger = animatedobject.AnimationState(self.tstobj)
        self.tiger.setAnimation('move')
        self.tiger.setDirection(0)

        self.iohandler = ioprocess.IOFunctions(self)
        self.lettermap = terrain.createLetterMap('../assets/terrain','terrainObjects.ini')
        self.tilemap = terrain.createCSVMap(self.lettermap,'../assets/terrain','test.csv',['overlay.csv'])
        self._screen.blit(self.tilemap.surface,(0,0))

        self.objects = list()
        self.objects.append(self.tiger)

    def processInputs(self):
        self.iohandler.handleEvents(pygame.event.get())

    def update(self):
        self.time.update()

    def draw(self):
        #self._screen.fill((0,0,0))
        #self._screen.blit(self.tilemap.surface,(0,0))
        frame = self.tiger.getFrame(self.time.time())
        for object in self.objects:
            self._screen.blit(self.tilemap.surface,object.getPos(),frame.get_rect().copy().move(object.getPos()))
        self._screen.blit(frame,self.tiger.getPos())
        pygame.display.flip()
