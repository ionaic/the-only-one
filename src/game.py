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
import projectile # projectile handling
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
        #self.tiger.setAnimation('move')
        #self.tiger.setDirection(0)

        self.pigobj = animatedobject.createAnimatedObject('../assets/piglet','object.ini')
        self.pig = animatedobject.AnimationState(self.pigobj)
        self.pig.setAnimation('stopped')
        self.pig.setDirection(0)
        self.pig.setPos(300,200)
        
        # handler for keyboard inputs, maps them to movements
        self.iohandler = ioprocess.IOFunctions(self)

        self.lettermap = terrain.createLetterMap('../assets/terrain','terrainObjects.ini')
        self.tilemap = terrain.createCSVMap(self.lettermap,'../assets/terrain','test.csv',['overlay.csv'])
        self._screen.blit(self.tilemap.surface,(0,0))

        # handler for projectiles
        self.bullets = projectile.Projectiles(self)

        self.objects = list()
        self.objects.append(self.tiger)
        self.objects.append(self.pig)

    def processInputs(self):
        self.iohandler.handleEvents(pygame.event.get())

    def update(self):
        self.time.update()
        self.iohandler.mover.updatePos()
        self.bullets.moveAll()
    def preDraw(self):
        for object in self.objects:
            frame = object.getFrame(self.time.time())
            self._screen.blit(self.tilemap.surface,object.getPos(),frame.get_rect().copy().move(object.getPos()))
        for rect in self.bullets.getDirty(self.time):
            self._screen.blit(self.tilemap.surface,(rect.left,rect.top),rect)
        
    def draw(self):
        self.tiger.draw(self._screen,self.time)
        self.pig.draw(self._screen,self.time)
        self.bullets.handleProjectiles(self.time)
        pygame.display.flip()
