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
import collisions
from collisions import ColBox
import character
import eventhandler
import enemies

#------------------------------------------------------------------------------
# Global Variables for Export ---------------------------------------

# Global Variables for use Inside the Module ------------------------

#------------------------------------------------------------------------------

class Game():
    universal = None
    def __init__(self):
        Game.universal = self
        pygame.init()
        self._screen = pygame.display.set_mode((800,600), \
            pygame.DOUBLEBUF+pygame.HWSURFACE)

        self.time = gametime.GameTime()
        self.tstobj = animatedobject.createAnimatedObject('../assets/tigger','object.ini')
        self.tstobj.setTag('tiger')
        #self.tiger = animatedobject.AnimationState(self.tstobj)
        self.tiger = character.Character(self.tstobj, self, 10, 10)
        self.tiger.setPosVec((40,80))
        self.tiger.stashPos=(40,80)
        #self.tiger.setAnimation('move')
        #self.tiger.setDirection(0)

        #self.pigobj = animatedobject.createAnimatedObject('../assets/piglet','object.ini')
        #self.pigobj.setTag('pig')
        #self.pig = animatedobject.AnimationState(self.pigobj)
        #self.pig = character.Character(self.pigobj, self, 10, 10)
        #self.pig.setAnimation('stopped')
        #self.pig.setDirection(0)
        #self.pig.setPos(300,200)

        self.stuffobj = animatedobject.createAnimatedObject('../assets/static/', 'object.ini')
        self.stuffobj.setTag('stuffing')
        self.stuffing = animatedobject.AnimationState(self.stuffobj)
        self.stuffing.setAnimation('stuffing')
        self.stuffing.setDirection(0)

        # handler for keyboard inputs, maps them to movements
        self.iohandler = ioprocess.IOFunctions(self)

        self.world = terrain.createWorld('../assets/terrain','world.ini')
        self.objects = list()
        #self.lettermap = terrain.createLetterMap('../assets/terrain','terrainObjects.ini')
        #self.tilemap = terrain.createCSVMap(self.lettermap,'../assets/terrain','test.csv',['overlay.csv'])
        #self._screen.blit(self.tilemap.surface,(0,0))

        # handler for projectiles
        self.bullets = projectile.Projectiles(self)

        self.enemies = enemies.Enemies(self)
        self.enemies.spawnTiglet()
        self.enemies.spawnTiglet()
        self.enemies.spawnTiglet()
        self.enemies.spawnTiglet()
        
        self.roomChange()

        interactions.registerCallbacks()

    def processInputs(self):
        self.iohandler.handleEvents(pygame.event.get())
    def roomChange(self):
        self.tilemap = self.world.getActiveMap()
        self._screen.blit(self.tilemap.surface,(0,0))
        for object in self.objects:
            object.invalidate()
        self.bullets.clear()

        self.objects = list()
        self.objects.append(self.tiger)
        self.objects.extend(self.tilemap.objects)
    def update(self):
        #room change
        if self.tiger.getFrame(self.time.time()).collisionArea.left+self.tiger.getX()>800:
            print "Out on the right"
            self.world.move((1,0))
            self.tiger.setX(self.tiger.getX()-800)
            self.roomChange()
        if self.tiger.getFrame(self.time.time()).collisionArea.right+self.tiger.getX()<0:
            print "Out on the left"
            self.world.move((-1,0))
            self.tiger.setX(self.tiger.getX()+800)
            self.roomChange()
        if self.tiger.getFrame(self.time.time()).collisionArea.bottom+self.tiger.getY()<0:
            print "Out on the top"
            self.world.moveUp((0,-1))
            self.tiger.setY(self.tiger.getY()+600)
            self.roomChange()
        if self.tiger.getFrame(self.time.time()).collisionArea.top+self.tiger.getY()>600:
            print "Out on the bottom"
            self.world.move((0,1))
            self.tiger.setY(self.tiger.getY()-600)
            self.roomChange()

        #housekeeping
        self.time.update()
        #self.iohandler.mover.updatePos()
        self.tiger.move.updatePos()
        for enemy in self.enemies.enemies:
            enemy.move.updatePos()
        #interactions.tiger_update(self.tiger)
        self.bullets.moveAll()
        #object list creation
        self.objlist = list(self.objects)
        self.objlist.extend(self.bullets.projectiles)
        self.objlist.extend(self.enemies.enemies)
        #collision
        colBoxes = self.bullets.getColRects(self.time.time())
        for obj in self.objlist:
            rect = obj.getFrame(self.time.time()).unionArea.move(obj.getPos())
            if rect != pygame.Rect(0,0,0,0):
                colBoxes.append(ColBox(rect,obj))
        for rect in self.tilemap.noGo:
            colBoxes.append(ColBox(rect,None))
        BB = pygame.Rect(0,0,800,600)
        collisions.collideRegion(BB,colBoxes,self.time.time())
        #frame events
        for object in self.objlist:
            event = object.getFrameEvent(self.time.time())
            if event != '':
                eventhandler.callEvent(event)
        
        
    def draw(self):
        for object in self.objects:
            object.undraw(self.tilemap.surface,self._screen,self.time)
        for object in self.bullets.projectiles:
            object.undraw(self.tilemap.surface,self._screen,self.time)
        for object in self.enemies.enemies:
            object.undraw(self.tilemap.surface,self._screen,self.time)
        self.objlist.sort(key=lambda o: o.getY()+o.getColAABB(self.time.time()).bottom)
        #map(lambda obj: obj.getColAABB(self.time.time()), objlist)
        map(lambda obj: obj.draw(self._screen,self.time), self.objlist)

        pygame.display.flip()
    
    def collideRects(self, obj, other):
        return obj.contains(other) or other.contains(obj) or obj.colliderect(other)
        #if obj == other:
        #    return False
        #elif isinstance(obj, pygame.Rect) and isinstance(other,pygame.Rect):
        #    return obj.contains(other) or other.contains(obj) or obj.colliderect(other)
        #else:
        #    print 'Arguments must both be of type pygame.Rect'
        
        #self.tiger.draw(self._screen,self.time)
        #self.pig.draw(self._screen,self.time)
        #self.bullets.handleProjectiles(self.time)
