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
from pygame import Rect

# Local Application/Library Specific Imports ------------------------

#------------------------------------------------------------------------------
# Global Variables for Export ---------------------------------------

# Global Variables for use Inside the Module ------------------------

#------------------------------------------------------------------------------

class Frame():
    def __init__(self,surface,drawn,col):
        self.surface = surface
        self.drawArea = drawn
        self.collisionArea = col

class Direction():
    def __init__(self,config,section,frames):
        self.frames = list()
        for n in range(1,frames+1):
            frame = pygame.image.load(config.get(section,str(n))).convert_alpha()
            #self.frames.append(frame)
            boundingRect = frame.get_bounding_rect()
            print boundingRect
            #self.drawn.append(boundingRect)
            option_name = str(n)+'_hitbox'
            if config.has_option(section,option_name):
                hbVal = config.get(section,option_name)
            else:
                hbVal = 'none'
            
            if hbVal=='none':
                aabb = Rect(0,0,0,0)
            elif hbVal=='full':
                aabb = frame.get_rect()
            elif hbVal=='drawn':
                aabb = boundingRect
            else:
                aabb = Rect(map(lambda X: int(X), hbVal.split(',')))

            self.frames.append(Frame(frame,boundingRect,aabb))

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
                self.directions[index] = self.directions[index-index%2]
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
        self.stash = Rect(0,0,0,0)
    def setAnimation(self,animName):
        self.animName = animName
        self.startTime = 0
    def setDirection(self,dir):
        self.dir = dir
    def setPosVec(self, vect):
        self.x = vect[0]
        self.y = vect[1]
    def setPos(self,x,y):
        self.x = x
        self.y = y
    def getDirection(self):
        return self.dir
    def getX(self):
        return self.x
    def getY(self):
        return self.y
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
    def getColAABB(self,time):
        framenum = self.getFrameNumber(time)
        anim = self.object.animations[self.animName].directions[self.dir]
        return anim.frames[framenum].collisionArea
    def draw(self,target,time):
        frame = self.getFrame(time.time())
        target.blit(frame.surface,self.getPos())
        self.stash = frame.drawArea.move(self.x,self.y)

def createAnimationState(obj, pos, dir, anim):
    state = AnimationState(obj)
    state.setPosVec(pos)
    state.setDirection(dir)
    state.setAnimation(anim)
    return state

