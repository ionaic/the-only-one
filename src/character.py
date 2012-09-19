import movement, animatedobject, animationstate, random, math

class Character(animatedobject.AnimationState):
    def __init__(self, obj, game, hp, ammo):
        self.center = self.getFrameByNum(5).collisionArea
        self.center = [self.center[i] * 0.5 for i in range(0, len(self.center))]
        animatedobject.AnimationState.__init__(self, obj)
        self.move = movement.Movement(self, game)
        self.health = hp
        self.ammo = ammo
        self.throwing = False
        self.path_blocked = False
        self.game = game

    # check if still has ammo
    def has_ammo(self):
        try:
            if self.ammo > 0:
                return True
            else:
                return False
        except TypeError:
            # this isn't a shooting enemy
            return False

class Enemy(Character):
    def __init__(self, obj, game, hp, ammo):
        Character.__init__(self, obj, game, hp, ammo)
        self.neighborhood = self.getFrame(self.game.time.time()).collisionArea
        self.neighborhood.right += 60
        self.neighborhood.bottom += 60
        self.getNeighborhood()
        self.direction = [1, 1]
        self.move.moveSpeed = [0.2, 0.2]

    def getNeighborhood(self):
        self.neighborhood.left = self.getX() - 30
        self.neighborhood.top = self.getY() - 30
        #self.neighborhood.left -= 30
        #self.neighborhood.top -= 30
        print 'neighborhood ' + str(self.neighborhood)

    def updateChar(self):
        print str(self.direction)
        self.moveDirection()
        self.move.moveState[0] = movement.vecToDir(self.direction)
        self.move.moveState[1] = movement.getSpeedState(movement.vecToDir(self.direction))
        self.setDirection(math.fabs(movement.vecToDir(self.direction)/2) * 2)
        self.move.moveChar()

    def moveDirection(self):
        mark = {'left':False, 'right':False, 'top':False, 'bottom':False}
        self.getNeighborhood()
        #self.neighborhood = self.getFrame(self.game.time.time()).collisionArea
        #self.topleft += self.getPos()
        topleft = (self.neighborhood.left, self.neighborhood.top)
        topright = (self.neighborhood.right, self.neighborhood.top)
        bottomleft = (self.neighborhood.left, self.neighborhood.bottom)
        bottomright = (self.neighborhood.right, self.neighborhood.bottom)
        for rect in self.game.tilemap.noGo:
            if rect.collidepoint(topleft):
                mark['left'] = True
                mark['top'] = True
            if rect.collidepoint(bottomleft):
                mark['left'] = True
                mark['bottom'] = True
            if rect.collidepoint(topright):
                mark['top'] = True
                mark['right'] = True
            if rect.collidepoint(bottomright):
                mark['bottom'] = True
                mark['right'] = True
        new_dir = [0, 0]
        #if True in mark.values() or not self.game._screen.get_rect().contains(self.neighborhood):
        if not self.game._screen.get_rect().contains(self.neighborhood):
            self.direction = [random.randint(-1, 1), random.randint(-1, 1)]
        if mark['left']:
            self.direction[0] = random.randint(0, 1)
            #new_dir[0] = 1
        if mark['right']:
            self.direction[0] = random.randint(-1, 0)
            #new_dir[0] -= 1
        if mark['top']:
            self.direction[1] = random.randint(0, 1)
            #new_dir[1] = 1
        if mark['bottom']:
            self.direction[1] = random.randint(-1, 0)
            #new_dir[1] -= 1
        #if new_dir[0] != 0:
        #    self.direction[0] = new_dir[0]
        #if new_dir[1] != 0:
        #    self.direction[1] = new_dir[1]
        #if self.direction == [0, 0]:
        #    self.direction = [random.randint(-1, 1), random.randint(-1, 1)]
        #if new_dir[0] != 0:
        #    self.direction[0] = new_dir
        #if new_dir[1] != 0:
        #    self.direction[1] = new_dir
