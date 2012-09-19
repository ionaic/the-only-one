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
import animatedobject
import animationstate
import character
import game
import enemies

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

def _mergeRectList(rects):
    found = True
    while found:
        found = False
        for i in range(0,len(rects)-1):
            I = rects[i]
            for j in range(i+1,len(rects)):
                J = rects[j]
                num = 0
                if I.left==J.right: num = num+1
                if I.right==J.left: num = num+1
                if I.top==J.bottom: num = num+1
                if I.bottom==J.top: num = num+1
                if I.left==J.left: num = num+1
                if I.right==J.right: num = num+1
                if I.top==J.top: num = num+1
                if I.bottom==J.bottom: num = num+1
                if num>=3:
                    newrect = I.union(J)
                    rects.pop(j)
                    rects.pop(i)
                    rects.append(newrect)
                    found = True
                    break
            if found:
                break
    return rects

def mergeRectlist(rects):
    print len(rects)
    BB = rects[0].copy()
    BB.unionall_ip(rects)
    quadrants = list()
    quadrants.append([Rect(BB.left,BB.top,BB.width/2,BB.height/2),list()])
    quadrants.append([Rect(BB.centerx,BB.top,BB.width/2,BB.height/2),list()])
    quadrants.append([Rect(BB.left,BB.centery,BB.width/2,BB.height/2),list()])
    quadrants.append([Rect(BB.centerx,BB.centery,BB.width/2,BB.height/2),list()])
    other = list()
    for rect in rects:
        found = False
        for quad in quadrants:
            if quad[0].contains(rect):
                quad[1].append(rect)
                found = True
                break
        if not found:
            other.append(rect)
    print len(other)
    for quad in quadrants:
        _mergeRectList(quad[1])
        #quad.append(threading.Thread(target=lambda: _mergeRectList(quad[1])))
        #quad[2].start()
    for quad in quadrants:
        #while quad[2].isAlive():
        #    continue
        #quad[2].join()
        other.extend(quad[1])
    print len(other)
    return other

class CSVMap():
    objectData = None
    def __init__(self,letterMap,fname,overlays,dynamic):
        reader = csv.reader(open(fname,'rb'),delimiter=',')
        self.noGo = list()
        self.surface = pygame.Surface((800,600),flags=pygame.SRCALPHA)
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
        self.noGo = mergeRectlist(self.noGo)
        self.surface.convert()

        self.objects = list()
        self.enemies = enemies.Enemies(game.Game.universal)
        if CSVMap.objectData==None:
            CSVMap.objectData = dict()
            CSVMap.objectData['tree'] = animatedobject.createAnimatedObject('../piglet','tree.ini')
            CSVMap.objectData['tree'].setTag('tree')
            CSVMap.objectData['hpig'] = animatedobject.createAnimatedObject('../piglet','pig.ini')
            CSVMap.objectData['hpig'].setTag('pig')
            #CSVMap.objectData['eeyore'] = animatedobject.createAnimatedObject('../eeyore','object.ini')
            #CSVMap.objectData['eeyore'].setTag('eeyore')

        for dyn in dynamic:
            if dyn=='none': continue
            reader = csv.reader(open(dyn,'rb'),delimiter=',')
            for line in enumerate(reader):
                for char in enumerate(line[1]):
                    x = 40*char[0]
                    y = 40*line[0]
                    if char[1] == 'tree':
                        tmp = character.Character(CSVMap.objectData['tree'], game.Game.universal, 10, 10)
                        tmp.setAnimation('stopped')
                        tmp.setDirection(0)
                        tmp.setPos(x,y)
                        self.objects.append(tmp)
                    elif char[1] == 'hpig':
                        tmp = character.Character(CSVMap.objectData['hpig'], game.Game.universal, 10, 10)
                        tmp.setAnimation('stopped')
                        tmp.setDirection(0)
                        tmp.setPos(x,y)
                        self.objects.append(tmp)
                    elif char[1] == 'eeyore':
                        #tmp = character.Character(CSVMap.objectData['eeyore'], game.Game.universal, 10, 10)
                        #tmp.setAnimation('stopped')
                        #tmp.setDirection(0)
                        #tmp.setPos(x,y)
                        #self.objects.append(tmp)
                        self.enemies.spawnDonkey(x, y)
                    elif char[1] == 'nedl':
                        self.enemies.spawnTiglet(x,y)
                    elif char[1] == 'beefy':
                        self.enemies.spawnBeefy(x,y)
                    
def createCSVMap(letterMap, folder, fname,overlays):
    cwd = os.getcwd()
    os.chdir(folder)
    csvMap = CSVMap(letterMap, fname,overlays)
    os.chdir(cwd)
    return csvMap

class World():
    def __init__(self,fname):
        config = ConfigParser.ConfigParser()
        config.readfp(open(fname))
        # load lettermaps
        self.lettermaps = dict()
        for item in config.items('lettermaps'):
            self.lettermaps[item[0]] = LetterMap(item[1])
        # load rooms
        self.rooms = dict()
        for room in config.items('rooms'):
            lettermap = self.lettermaps[config.get(room[1],'lettermap')]
            base = config.get(room[1],'base')
            overlays = config.get(room[1],'overlays').split(',')
            dynamic = config.get(room[1],'dynamic').split(',')
            self.rooms[room[0]] = CSVMap(lettermap,base,overlays,dynamic)
        # load worldmap
        self.pos = map(lambda X: int(X), config.get('worldmap','start').split(','))
        reader = csv.reader(open(config.get('worldmap','file')),delimiter=',')
        self.grid = list()
        for line in enumerate(reader):
            data = list()
            for element in enumerate(line[1]):
                data.append(element[1])
            self.grid.append(data)
    def getPos(self):
        return (self.grid[self.pos[1]])[self.pos[0]]
    def getActiveMap(self):
        return self.rooms[(self.grid[self.pos[1]])[self.pos[0]]]
    def move(self,displacement):
        self.pos[0] = self.pos[0]+displacement[0]
        self.pos[1] = self.pos[1]+displacement[1]
        print self.pos
        print self.getPos()
        

def createWorld(folder, fname):
    cwd = os.getcwd()
    os.chdir(folder)
    world = World(fname)
    os.chdir(cwd)
    return world
