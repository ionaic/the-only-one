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
from aabb import AABB

#------------------------------------------------------------------------------
# Global Variables for Export ---------------------------------------

# Global Variables for use Inside the Module ------------------------

#------------------------------------------------------------------------------

class Direction():
    def __init__(self,config,section,frames):
        self.frames = list()
        self.aabbs = list()
        for n in range(1,frames+1):
            self.frames.append(pygame.image.load(config.get(section,str(n))).convert_alpha())
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

def collideRects(obj, other):
    if obj == other:
        return False
    elif isinstance(obj, pygame.Rect):
        return obj.contains(other) or other.contains(obj) or obj.colliderect(other)
    else:
        print 'Arguments must both be of type pygame.Rect'

class AnimatedObject():
    def __init__(self,fname):
        config = ConfigParser.ConfigParser()
        config.readfp(open(fname))
        
        self.animations = dict()

        self.collide_func = lambda: None
        
        for animation in config.items('animations'):
            self.animations[animation[0]] = Animation(config,animation[1])

    def registerCollideCB(self, func):
        self.collide_func = func
    
def createAnimatedObject(folder, fname):
    cwd = os.getcwd()
    os.chdir(folder)
    aniobj = AnimatedObject(fname)
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
        self.newX = 0
        self.newY = 0
    def setAnimation(self,animName):
        self.animName = animName
        self.startTime = 0
    def setDirection(self,dir):
        self.dir = dir
    def setNewPosVec(self, vect):
        self.newX = vect[0]
        self.newY = vect[1]
    def setNewPos(self, x, y):
        self.newX = x
        self.newY = y
    def setPos(self,x,y):
        self.x = x
        self.y = y
    def getDirection(self):
        return self.dir
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getNewPos(self):
        return (self.newX, self.newY)
    def getPos(self):
        return (self.x,self.y)
    def updatePos(self):
        self.x = newX
        self.y = newY
    def getFrameNumber(self,gameTime):
        if self.startTime == 0:
            self.startTime = gameTime
        timediff = gameTime - self.startTime
        fps = self.object.animations[self.animName].fps
        frames = self.object.animations[self.animName].frames
        msf = 1000 / fps
        frame = (timediff / msf)%frames
        return int(frame)
    def getFrame(self,gameTime):
        anim = self.object.animations[self.animName].directions[self.dir]
        frame = anim.frames[self.getFrameNumber(gameTime)]
        return frame
