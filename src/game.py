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
import ConfigParser
import os

# 3'rd Party Imports ------------------------------------------------
import pygame

# Local Application/Library Specific Imports ------------------------
import gametime
#------------------------------------------------------------------------------
# Global Variables for Export ---------------------------------------

# Global Variables for use Inside the Module ------------------------

#------------------------------------------------------------------------------
class AABB():
    def __init__(self,raw):
        split = raw.split(',')
        self.left = int(split[0])
        self.top = int(split[1])
        self.width = int(split[2])
        self.height = int(split[3])
    def __str__(self):
        return '{ left: ' + str(self.left) + ' top: ' + str(self.top) + \
                ' width: ' + str(self.width) + ' height: ' + str(self.height)

class Direction():
    def __init__(self,config,section,frames):
        self.frames = list()
        self.aabbs = list()
        for n in range(1,frames+1):
            self.frames.append(pygame.image.load(config.get(section,str(n))))
            self.aabbs.append(AABB(config.get(section,str(n)+'_hitbox')))
        for aabb in self.aabbs:
            print aabb

class Animation():
    def __init__(self,config,section):
        self.frames = config.getint(section,'frames')
        self.fps = config.getint(section,'fps')
        
        self.directions = dict()
        
        for index, dir in enumerate(['south','southwest','west','northwest','north','northeast','east','southeast']):
            try:
                val = config.get(section,dir)
                self.directions[index] = Direction(config,val,self.frames)
            except ConfigParser.NoOptionError:
                continue

class AnimatedObject():
    def __init__(self,fname):
        config = ConfigParser.ConfigParser()
        config.readfp(open(fname))
        
        self.animations = dict()
        
        for animation in config.items('animations'):
            self.animations[animation[0]] = Animation(config,animation[1])

class Game():
    def __init__(self):
        pygame.init()
        self._screen = pygame.display.set_mode((800,600), \
            pygame.DOUBLEBUF+pygame.HWSURFACE)

        self._ball = pygame.image.load("ball.png").convert_alpha()

        self._square = pygame.Surface((50,50))
        self._square.fill((255,255,0))
        self.time = gametime.GameTime()
        os.chdir('data/knight/')
        tstobj = AnimatedObject('object.ini')
        os.chdir('../..')

    def processInputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()

    def update(self):
        self.time.update()

    def draw(self):
        self._screen.fill((0,0,0))
        self._screen.blit(self._ball,self._ball.get_rect())
        self._screen.blit(self._square, (150,45))
        #flip
        pygame.display.flip()