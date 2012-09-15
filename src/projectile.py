# projectiles
import pygame, sys, game, movement, operator

class Button:
    def __init__(self, x, y, direction):
        self.surf = pygame.image.load('../assets/projectiles/button_placeholder/eeyore0001.png')
        self.position = [x, y]
        self.direction = direction

    def get_rect(self):
        return self.surf.get_rect()

class Projectiles:
    projectile_speed = [1,1]

    def __init__(self, game):
        self.projectiles = []
        self.game = game
        self.screen_rect = self.game._screen.get_rect()

    def spawnProjectile(self, x, y, direction):
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
        proposed_pos = map(operator.mul, movement.dirToVec(proj.direction), self.projectile_speed)
        proposed_pos = map(operator.add, proposed_pos, proj.position)
        proj.position = proposed_pos

    def handleProjectiles(self):
        map(self.game._screen.blit, (self.projectiles[i].surf for i in range(0, len(self.projectiles))), (self.projectiles[i].position for i in range(0, len(self.projectiles))))

    def collideAll(self):
        #map(self.collide, self.projectiles, self.game.objects)
        map(self.screen_collide, self.projectiles)

    def screen_collide(self, x):
        if not self.screen_rect.contains(x.get_rect()):
            if x in self.projectiles:
                self.projectiles.remove(x)

    def collide(self, x, y):
        if not (x.get_rect().colliderect(y.get_rect()) or \
            x.get_rect().contains(y.get_rect) or \
            y.get_rect().contains(x.get_rect())): 
            print str(x) + " hit " + str(y)
            if x in self.projectiles:
                self.projectiles.remove(x)
            elif y in self.projectiles:
                self.projectiles.remove(y)
