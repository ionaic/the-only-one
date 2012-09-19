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
import operator

# 3'rd Party Imports ------------------------------------------------
import pygame
from pygame import Rect

# Local Application/Library Specific Imports ------------------------
from animationstate import *

#------------------------------------------------------------------------------
# Global Variables for Export ---------------------------------------

# Global Variables for use Inside the Module ------------------------

#------------------------------------------------------------------------------

class Frame():
    def __init__(self,surface,drawn,col, shadowBound, event):
        self.surface = surface
        self.drawArea = drawn
        if shadowBound != None:
            # calculate the size and position of the shadow
            shadow_dim = (shadowBound.width, shadowBound.width / 3)
            shadow_pos = ((surface.get_width() - shadowBound.width)/2, shadowBound.height - shadow_dim[1] * 0.5)
            # find the appropriate surface size
            surf_size = map(operator.add, shadow_pos, shadow_dim)
            #surf_size = (max(surf_size[0], surface.get_width()), surf_size[1])
            surf_size = map(max, surf_size, surface.get_size())
            # create new surface of appropriate size for image and shadow
            self.surface = pygame.Surface(surf_size, pygame.SRCALPHA)
            # draw the shadow
            pygame.draw.ellipse(self.surface, pygame.Color(0, 0, 0, 100), pygame.Rect(shadow_pos, shadow_dim), 0)
            # draw the actual sprite
            self.surface.blit(surface, (0,0))
            # set the bounding area and collision area
            self.drawArea = self.surface.get_bounding_rect()
        self.collisionArea = col
        self.unionArea = self.drawArea.union(self.collisionArea)
        self.event = event

class Direction():
    def __init__(self,config,section,frames):
        self.frames = list()
        shadowBound = None
        if config.has_option(section,"shadowbox"):
            shadowBound = pygame.Rect(map(lambda X: int(X),config.get(section,'shadowbox').split(',')))
        for n in range(1,frames+1):
            frame = pygame.image.load(config.get(section,str(n))).convert_alpha()
            #self.frames.append(frame)
            boundingRect = frame.get_bounding_rect()

            #print boundingRect
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
            option_name = str(n)+'_event'
            if config.has_option(section,option_name):
                event = config.get(section,option_name)
            else:
                event = ''
            
            self.frames.append(Frame(frame,boundingRect,aabb, shadowBound, event))

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
                self.directions[index] = self.directions[index-1]
                continue

class AnimatedObject():
    def __init__(self,fname):
        config = ConfigParser.ConfigParser()
        config.readfp(open(fname))
        
        self.animations = dict()

        self.collide_func = lambda: None
        
        for animation in config.items('animations'):
            self.animations[animation[0]] = Animation(config,animation[1])
       
        print 'animations ' + str(self.animations)
 
        self.tag = ''

    def registerCollideCB(self, func):
        self.collide_func = func

    def setTag(self, tag):
        self.tag = tag
    
def createAnimatedObject(folder, fname):
    cwd = os.getcwd()
    os.chdir(folder)
    aniobj = AnimatedObject(fname)
    os.chdir(cwd)
    return aniobj

class GroupDirection():
    def __init__(self,config,section,frames):
        positions = list()
        for i in range(1,frames+1):
            positions.append(map(lambda x: int(x),config.get(section,str(i)).split(',')))

class GroupAnimation():
    def __init__(self,config,section,objects):
        self.frames = config.getint(section,'frames')
        self.fps = config.getint(section,'fps')
        
        self.directions = dict()
        
        for index, dir in enumerate(['south','southwest','west','northwest', \
                                     'north','northeast','east','southeast']):
            for obj in objects:
                key_name = dir+"_"+obj[0]
                if config.has_option(section,key_name):
                    val = config.get(section,key_name)
                    self.directions[str(index)+obj[0]] = GroupDirection(config,val,self.frames)

class ObjectGroup():
    def __init__(self,fname):
        config = ConfigParser.ConfigParser()
        config.readfp(open(fname))

        self.objects = list()
        for object in config.items('objects'):
            self.objects.append([object[0],AnimatedObject(object[1])])

        self.animations=dict()
        for animation in config.items('animations'):
            self.animations[animation[0]] = GroupAnimation(config,animation[1],self.objects)

def createObjectGroup(folder, fname):
    cwd = os.getcwd()
    os.chdir(folder)
    obj = ObjectGroup(fname)
    os.chdir(cwd)
    return obj
     
