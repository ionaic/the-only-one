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
        self.knight = animatedobject.AnimationState(self.tstobj)
        self.knight.setAnimation('move')
        self.knight.setDirection(0)

        self.iohandler = ioprocess.IOFunctions(self)
        self.lettermap = terrain.createLetterMap('../assets/terrain','terrainObjects.ini')
        self.tilemap = terrain.createTiledMap(self.lettermap, '../assets/terrain','test.txt',['overlay.txt'])

    def processInputs(self):
        self.iohandler.handleEvents(pygame.event.get())
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         sys.exit()
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_ESCAPE:
        #             sys.exit()
        #         if event.key == pygame.K_LEFT:
        #             self.knight.setDirection(2)
        #         if event.key == pygame.K_RIGHT:
        #             self.knight.setDirection(6)
        #         if event.key == pygame.K_UP:
        #             self.knight.setDirection(4)
        #         if event.key == pygame.K_DOWN:
        #             self.knight.setDirection(0)

    def update(self):
        self.time.update()

    def draw(self):
        #self._screen.fill((0,0,0))
        self._screen.blit(self.tilemap.surface,(0,0))
        frame = self.knight.getFrame(self.time.time())
        self._screen.blit(frame,self.knight.getPos())
        pygame.display.flip()
