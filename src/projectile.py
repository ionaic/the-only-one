# projectiles
# author Ian Ooi
import pygame, sys, game, movement, operator, animatedobject

class Button():
    def __init__(self, x, y, direction):
        #self.surf = pygame.image.load('../assets/projectiles/button_placeholder/eeyore0001.png')
        self.tstobj = animatedobject.createAnimatedObject('../assets/projectiles/button_placeholder', 'object.ini')
        self.anim = animatedobject.AnimationState(self.tstobj)
        self.position = [x, y]
        self.direction = direction

    def get_rect(self):
        #return self.surf.get_rect()
        return self.getFrame.get_rect()

    def getFrame(self, time):
        return self.anim.getFrame(time)

class Projectiles:
    projectile_speed = [1,1]

    def __init__(self, game):
        self.projectiles = []
        self.game = game
        self.screen_rect = self.game._screen.get_rect()

    def spawnProjectile(self, x, y, direction):
        print "spawned at " + str((x, y)) + " with velocity " + str(direction)
        if direction < 0:
            self.projectiles.append(Button(x, y, self.game.tiger.getDirection()))
        else:
            self.projectiles.append(Button(x, y, direction))

    def moveAll(self):
        if self.projectiles == []:
            return
        self.collideAll()
        map(self.move, self.projectiles)

    def move(self, proj):
        speed = [movement.getSpeedState(proj.direction) * self.projectile_speed[i] \
            for i in range(0, len(self.projectile_speed))]
        proposed_pos = map(operator.mul, movement.dirToVec(proj.direction), speed)
        proposed_pos = map(operator.add, proposed_pos, proj.position)
        proj.position = proposed_pos

    def handleProjectiles(self, time):
        map(self.game._screen.blit, (self.projectiles[i].getFrame(time) for i in range(0, len(self.projectiles))), (self.projectiles[i].position for i in range(0, len(self.projectiles))))

    def collideAll(self):
        #map(self.collide, self.projectiles, self.game.objects)
        map(self.screen_collide, self.projectiles)

    def screen_collide(self, x):
        #if (self.screen_rect.contains(x.get_rect())) == False:
        if self.screen_rect.collidepoint(tuple(x.position)) == False or 0 in x.position:
            print "out of screen "
            if x in self.projectiles:
                print "removing " + str(x)
                self.projectiles.remove(x)

    def collide(self, x, y):
        if (x.get_rect().colliderect(y.get_rect()) == False or \
            x.get_rect().contains(y.get_rect) or \
            y.get_rect().contains(x.get_rect())): 
            print str(x) + " hit " + str(y)
            if x in self.projectiles:
                print "removing " + str(x)
                self.projectiles.remove(x)
            elif y in self.projectiles:
                print "removing " + str(y)
                self.projectiles.remove(y)
