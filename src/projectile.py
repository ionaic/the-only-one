# projectiles
# author Ian Ooi
import pygame, sys, game, movement, operator, animatedobject
from animatedobject import createAnimationState

class Projectiles:
    projectile_speed = [1,1]
    projectileObject = None

    def __init__(self, game):
        Projectiles.projectiles = []
        self.game = game
        self.screen_rect = self.game._screen.get_rect()
    
    def getDirty(self,time):
        rects = list()
        for object in Projectiles.projectiles:
            rects.append(object.stash)
        return rects

    def getColRects(self,time):
        rects = list()
        for object in Projectiles.projectiles:
            rects.append(game.ColBox(object.getFrame(time).collisionArea,object))
        return rects

    def spawnProjectile(self, x, y, direction):
        if Projectiles.projectileObject == None:
            Projectiles.projectileObject = animatedobject.createAnimatedObject('../assets/projectiles/button_placeholder', 'object.ini')
            Projectiles.projectileObject.setTag('button')
            
        # temp = createAnimationState(Projectiles.projectileObject, self.game, 1, 1)
        # temp.setPos(x, y)
        if direction < 0:
            temp = createAnimationState(Projectiles.projectileObject, (x, y), self.game.tiger.getDirection(),'stopped')
            #temp.setDirection(self.game.tiger.getDirection())
        else:
            temp = createAnimationState(Projectiles.projectileObject, (x, y), direction,'stopped')
            #temp.setDirection(direction)
        #temp.setAnimation('stopped')
        Projectiles.projectiles.append(temp)

    def moveAll(self):
        if Projectiles.projectiles == []:
            return
        self.collideAll()
        map(self.move, Projectiles.projectiles)

    def move(self, proj):
        speed = [movement.getSpeedState(proj.getDirection()) * self.projectile_speed[i] \
            for i in range(0, len(self.projectile_speed))]
        proposed_pos = map(operator.mul, movement.dirToVec(proj.getDirection()), speed)
        proposed_pos = map(operator.add, proposed_pos, proj.getPos())
        proj.setPos(proposed_pos[0],proposed_pos[1])

    def handleProjectiles(self, time):
        map(lambda projectile: projectile.draw(self.game._screen,time), Projectiles.projectiles)

    def collideAll(self):
        map(self.screen_collide, Projectiles.projectiles)

    def screen_collide(self, x):
        #if (self.screen_rect.contains(x.get_rect())) == False:
        if self.screen_rect.collidepoint(x.getPos()) == False or 0 in x.getPos():
            #print "out of screen "
            if x in Projectiles.projectiles:
                #print "removing " + str(x)
                Projectiles.projectiles.remove(x)
