"""Contains the AnimatedObject class and subclasses.
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
        
        for index, dir in enumerate(['south','southwest','west','northwest', \
                                     'north','northeast','east','southeast']):
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

def createAnimatedObject(folder, fname):
    cwd = os.getcwd()
    os.chdir('data/knight/')
    aniobj = AnimatedObject('object.ini')
    os.chdir(cwd)
