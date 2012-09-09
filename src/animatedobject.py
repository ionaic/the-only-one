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

# Axis-Aligned Bounding Box
class AABB():
    def __init__(self,raw):
        split = raw.split(',')
        self.left = int(split[0])
        self.top = int(split[1])
        self.width = int(split[2])
        self.height = int(split[3])
    def __str__(self):
        return '{ left: ' + str(self.left) + ' top: ' + str(self.top) + \
                ' width: ' + str(self.width) + ' height: ' + str(self.height) \
                + '}'

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
    os.chdir(folder)
    aniobj = AnimatedObject('object.ini')
    os.chdir(cwd)
    return aniobj

class AnimationState():
    def __init__(self, obj):
        self.object = obj
        self.dir = 0
        self.startTime = 0
        self.animName = 'stopped'
        self.x = 0
        self.y = 0
    def changeAnimation(self,animName):
        self.animName = animName
        self.startTime = 0
    def changeDirection(self,dir):
        self.dir = dir
    def setPosition(self,x,y):
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getFrameNumber(self,gameTime):
        if self.startTime == 0:
            self.startTime = gameTime
        timediff = gameTime - self.startTime
        fps = self.object.animations[self.animName].fps
        frames = self.object.animations[self.animName].frames
        msf = (fps * 1000) / frames
        frame = (timediff / msf)%frames
        return int(frame)
    def getFrame(self,gameTime):
        anim = self.object.animations[self.animName].directions[self.dir]
        frame = anim.frames[self.getFrameNumber(gameTime)]
        return frame
