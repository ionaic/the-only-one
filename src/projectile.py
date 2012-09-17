# projectiles
# author Ian Ooi
import pygame, sys, game, movement, operator, animatedobject
from animatedobject import createAnimationState

class Projectiles:
    projectile_speed = [1,1]
    projectileObject = None

    def __init__(self, game):
        self.projectiles = []
        self.game = game
        self.screen_rect = self.game._screen.get_rect()
    
    def getDirty(self,time):
        rects = list()
        for object in self.projectiles:
            rects.append(object.stash)
        return rects

    def getColRects(self,time):
        rects = list()
        for object in self.projectiles:
            rects.append(game.ColBox(object.getFrame(time).collisionArea,object))
        return rects

    
    def spawnProjectile(self, x, y, direction):
        if Projectiles.projectileObject == None:
            Projectiles.projectileObject = animatedobject.createAnimatedObject('../assets/projectiles/button_placeholder', 'object.ini')
        #print "spawned at " + str((x, y)) + " with velocity " + str(direction)
        if direction < 0:
            self.projectiles.append(createAnimationState(Projectiles.projectileObject, (x, y), self.game.tiger.getDirection(),'stopped'))
        else:
            self.projectiles.append(createAnimationState(Projectiles.projectileObject, (x, y), direction,'stopped'))

    def moveAll(self):
        if self.projectiles == []:
            return
        self.collideAll()
        map(self.move, self.projectiles)

    def move(self, proj):
        speed = [movement.getSpeedState(proj.getDirection()) * self.projectile_speed[i] \
            for i in range(0, len(self.projectile_speed))]
        proposed_pos = map(operator.mul, movement.dirToVec(proj.getDirection()), speed)
        proposed_pos = map(operator.add, proposed_pos, proj.getPos())
        proj.setPos(proposed_pos[0],proposed_pos[1])

    def handleProjectiles(self, time):
        map(lambda projectile: projectile.draw(self.game._screen,time), self.projectiles)

    def collideAll(self):
        map(self.screen_collide, self.projectiles)

    def screen_collide(self, x):
        #if (self.screen_rect.contains(x.get_rect())) == False:
        if self.screen_rect.collidepoint(x.getPos()) == False or 0 in x.getPos():
            #print "out of screen "
            if x in self.projectiles:
                #print "removing " + str(x)
                self.projectiles.remove(x)
