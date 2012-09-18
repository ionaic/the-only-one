import movement, animatedobject, animationstate

class Character(animatedobject.AnimationState, movement.Movement):
    def __init__(self, obj, game, hp, ammo):
        animatedobject.AnimationState.__init__(self, obj)
        self.move = movement.Movement(game)
        self.health = hp
        self.ammo = ammo
        self.throwing = False
        self.path_blocked = False

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

