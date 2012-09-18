import movement, animatedobject, animationstate

class Character(animatedobject.AnimationState):
    def __init__(self, obj, game, hp, ammo):
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
        self.neighborhood.left -= 30
        self.neighborhood.top -= 30
        self.neighborhood.right += 30
        self.neighborhood.bottom += 30
        self.direction = [1, 1]
        self.move.moveSpeed = [0.3, 0.3]

    def updateChar(self):
        #self.moveDirection()
        self.move.moveState[0] = movement.vecToDir(self.direction)
        self.move.moveState[1] = movement.getSpeedState(movement.vecToDir(self.direction))
        self.move.moveChar()

    def moveDirection(self):
        mark = {'left':False, 'right':False, 'top':False, 'bottom':False}
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
        if mark['left']:
            new_dir[0] = 1
        if mark['right']:
            new_dir[0] -= 1
        if mark['top']:
            new_dir[1] += 1
        if mark['bottom']:
            new_dir[1] -= 1

        if new_dir[0] != 0:
            self.direction[0] = new_dir
        if new_dir[1] != 0:
            self.direction[1] = new_dir
