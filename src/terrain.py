"""This is a template Python file.
Python Version: 2.7.3
Author: Matthew McMullan

Description: This template was made using best practices from...
http://www.python.org/dev/peps/pep-0008/
http://www.python.org/dev/peps/pep-0257/

"""
#------------------------------------------------------------------------------
# Standard Library Imports ------------------------------------------
import ConfigParser
import os
import fileinput
import csv

# 3'rd Party Imports ------------------------------------------------
import pygame
from pygame import Rect
# Local Application/Library Specific Imports ------------------------

#------------------------------------------------------------------------------
# Global Variables for Export ---------------------------------------

# Global Variables for use Inside the Module ------------------------

#------------------------------------------------------------------------------

class Tile():
    def __init__(self,config,section):
        self.image = pygame.image.load(config.get(section,'image')).convert_alpha()
        
        if config.has_option(section,"hitbox"):
                hbVal = config.get(section,"hitbox")
        else:
            hbVal = 'none'
            
        if hbVal=='none':
            self.aabb = Rect(0,0,0,0)
        elif hbVal=='full':
            self.aabb = self.image.get_rect()
        elif hbVal=='drawn':
            self.aabb = self.image.get_bounding_rect()
        else:
            self.aabb = Rect(map(lambda X: int(X), hbVal.split(',')))
        #self.aabb = Rect(map(lambda X: int(X), config.get(section,'hitbox').split(',')))

class LetterMap():
    def __init__(self,fname):
        config = ConfigParser.ConfigParser()
        config.readfp(open(fname))
        self.tiles=dict()
        for tile in config.items('tiles'):
            self.tiles[tile[0]] = Tile(config,tile[1])
            
def createLetterMap(folder, fname):
    cwd = os.getcwd()
    os.chdir(folder)
    letmap = LetterMap(fname)
    os.chdir(cwd)
    return letmap

class TiledMap():
    def __init__(self,letterMap,fname,overlays):
        with open(fname) as f:
            lines = f.readlines()
        dim_x = 40*len(lines[0])-40
        dim_y = 40*len(lines)
        self.surface = pygame.Surface((dim_x,dim_y)).convert_alpha()
        for line in enumerate(lines):
            for char in enumerate(line[1]):
                if char[1]=='\n': continue
                self.surface.blit(letterMap.tiles[char[1]].image,(40*char[0],40*line[0]))
        for overlay in overlays:
            with open(overlay) as f:
                lines = f.readlines()
            for line in enumerate(lines):
                for char in enumerate(line[1]):
                    if char[1]=='\n': continue
                    if char[1]=='.': continue
                    self.surface.blit(letterMap.tiles[char[1]].image,(40*char[0],40*line[0]))
        self.surface.convert()

def createTiledMap(letterMap, folder, fname,overlays):
    cwd = os.getcwd()
    os.chdir(folder)
    tiledMap = TiledMap(letterMap, fname,overlays)
    os.chdir(cwd)
    return tiledMap

class CSVMap():
    def __init__(self,letterMap,fname,overlays):
        reader = csv.reader(open(fname,'rb'),delimiter=',')
        self.noGo = list()
        self.surface = pygame.Surface((800,600)).convert_alpha()
        for line in enumerate(reader):
            for char in enumerate(line[1]):
                x = 40*char[0]
                y = 40*line[0]
                if char[1]=='\n': continue
                if char[1]=='': continue
                if char[1]=='0': continue
                self.surface.blit(letterMap.tiles[char[1]].image,(x,y))
                if letterMap.tiles[char[1]].aabb!=pygame.Rect(0,0,0,0):
                    self.noGo.append(letterMap.tiles[char[1]].aabb.move(x,y))
        for overlay in overlays:
            reader = csv.reader(open(overlay,'rb'),delimiter=',')
            for line in enumerate(reader):
                for char in enumerate(line[1]):
                    x = 40*char[0]
                    y = 40*line[0]
                    if char[1]=='.': continue
                    if char[1]=='0': continue
                    if char[1]=='': continue
                    self.surface.blit(letterMap.tiles[char[1]].image,(x,y))
                    if letterMap.tiles[char[1]].aabb!=pygame.Rect(0,0,0,0):
                        self.noGo.append(letterMap.tiles[char[1]].aabb.move(x,y))
        self.surface.convert()

def createCSVMap(letterMap, folder, fname,overlays):
    cwd = os.getcwd()
    os.chdir(folder)
    csvMap = CSVMap(letterMap, fname,overlays)
    os.chdir(cwd)
    return csvMap
