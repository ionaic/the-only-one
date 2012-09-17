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
import interactions

#------------------------------------------------------------------------------
# Global Variables for Export ---------------------------------------

# Global Variables for use Inside the Module ------------------------

#------------------------------------------------------------------------------

class ColBox():
    def __init__(self,rect,object):
        self.rect = rect
        self.object = object

class Game():
    def __init__(self):
        pygame.init()
        self._screen = pygame.display.set_mode((800,600), \
            pygame.DOUBLEBUF+pygame.HWSURFACE)

        self.time = gametime.GameTime()
        self.tstobj = animatedobject.createAnimatedObject('../assets/tigger','object.ini')
        self.tstobj.setTag('tiger')
        self.tiger = animatedobject.AnimationState(self.tstobj)
        #self.tiger.setAnimation('move')
        #self.tiger.setDirection(0)

        self.pigobj = animatedobject.createAnimatedObject('../assets/piglet','object.ini')
        self.pigobj.setTag('pig')
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
        #for object in self.objects:
        #    self._screen.blit(self.tilemap.surface,object.stash.topleft,object.stash)
        for rect in self.bullets.getDirty(self.time):
            self._screen.blit(self.tilemap.surface,(rect.left,rect.top),rect)
        
    def draw(self):
        for object in self.objects:
            object.undraw(self.tilemap.surface,self._screen,self.time)
        objlist = list(self.objects)
        objlist.extend(self.bullets.projectiles)
        objlist.sort(key=lambda o: o.getY()+o.getColAABB(self.time.time()).bottom)
        #map(lambda obj: obj.getColAABB(self.time.time()), objlist)
        map(lambda obj: obj.draw(self._screen,self.time), objlist)

        colBoxes = self.bullets.getColRects(self.time.time())
        for obj in objlist:
            rect = obj.getFrame(self.time.time()).collisionArea.move(obj.getPos())
            if rect != pygame.Rect(0,0,0,0):
                colBoxes.append(ColBox(rect,obj))
        for i in range(0,len(colBoxes)-1):
            for j in range(i+1,len(colBoxes)):
                if self.collideRects(colBoxes[i].rect, colBoxes[j].rect):
                    print "colBoxes[i] " + str(colBoxes[i]) + " colBoxes[j] " + str(colBoxes[j])
                    self.collide(colBoxes[i].object, colBoxes[j].object)
                    colBoxes[i].object.dirty = True
                    colBoxes[j].object.dirty = True
        pygame.display.flip()
    
    def collideRects(self, obj, other):
        if obj == other:
            return False
        elif isinstance(obj, pygame.Rect):
            return obj.contains(other) or other.contains(obj) or obj.colliderect(other)
        else:
            print 'Arguments must both be of type pygame.Rect'

        #elif thing1 == 'projectile':
        #    if thing2 == 'tiger':
        #    elif thing2 == 'pig':
        #elif thing1 == None:
            
        
        #self.tiger.draw(self._screen,self.time)
        #self.pig.draw(self._screen,self.time)
        #self.bullets.handleProjectiles(self.time)
