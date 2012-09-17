# functions to handle game logic
# interactions.py
# Author: Ian Ooi

import animatedobject, movement, projectile

def collide(obj1, obj2):
    if obj1 != None:
        thing1 = obj1.object.tag
    else:
        thing1 = 'none'
    if obj2 != None:
        thing2 = obj2.object.tag
    else:
        thing2 = 'none'

    if thing1 == 'tiger':
        if thing2 == 'pig':
            piglet_onbump(obj2)
        elif thing2 == 'button':
            #tiger_onhit(obj1)
            ""
        elif thing2 == 'none':
            tiger_onwall(obj1)
    elif thing1 == 'pig':
        if thing2 == 'tiger':
            piglet_onbump(obj1)
        elif thing2 == 'button':
            piglet_onhit(obj1)
            button_onhit(obj2)
        elif thing2 == 'none':
            piglet_onwall(obj1)
    elif thing1 == 'button':
        if thing2 == 'pig':
            button_onhit(obj1)
            piglet_onhit(obj2)
        elif thing2 == 'tiger':
            #button_onhit(obj1)
            #tiger_onhit(obj2)
            ""
        elif thing2 == 'none':
            #button_onhit(obj1)
            ""
    elif thing1 == 'none':
        if thing2 == 'pig':
            piglet_onhit(obj2)
        elif thing2 == 'tiger':
            tiger_onwall(obj2)
        elif thing2 == 'button':
            #button_onhit(obj2)
            ""

class Character(animatedobject.AnimationState, movement.Movement):
    def __init__(self, obj, game, hp, ammo):
        animatedobject.AnimationState.__init__(self, obj)
        movement.Movement.__init__(self, game)
        self.health = hp
        self.ammo = ammo

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

########## TIGER ##########
# PC tiger hit by something
def tiger_onhit(self):
    # decrement health
    #self.health -= 1
    # play hit animation
    self.setAnimation('damaged')
    self.stopMove()
    # play hit sound
    # stop all in progress player actions
    # invulnerable for x amount of time
    # while invulnerable, can't shoot
    return

# PC tiger shoots/throws something
def tiger_onshoot(self):
    # check if tiger has enough ammo left
    if self.has_ammo():
        # launch projectile
        # reduce amount of available ammo
        self.ammo -= 1
        # play throwing animation
        if self.animName != 'move':
            self.setAnimation('shoot')
        else:
            self.setAnimation('moveshoot')
        # play throw sound
        # begin tracking aninmation
        return

# PC Tiger done shooting, back to either moving or standing
def tiger_shot(self):
    if self.animName != 'moveshoot':
        self.setAnimation('stopped')
    else:
        self.setAnimation('move')

# PC tiger uses walljump attack
def tiger_onwalljump(self):
    # move to closest wall
    # play launch animation/sound
    self.setAnimation('launch')
    # move tigger toward opposite wall
    # play land animation/sound
    # damage everything in straight line path that is a 
    #   rectangle with dim (pathlength, tiggerwidth)
    return

# PC tiger uses jump attack
def tiger_onjump(self):
    # play launching/jumping animation
    # launch into air (offscreen)
    self.setAnimation('rocket')
    # mark potential landing spot with shadow
    # move landing spot based on key inputs
    # land
    # damage everything in region surrounding tiger
    return

# PC tiger dies
def tiger_ondie(self):
    # play death animation
    # play death sound
    # stop everything onscreen
    # lose screen, retry
    return

# PC tiger moves
def tiger_onwalk(self):
    # set animation type
    #if self.moveState[0] != -1:
    if self.animName == 'stopped' and self.moveState[1] != 0:
        self.setAnimation('move')
    elif self.animName == 'moveshoot' and self.moveState[1] == 0:
        # TODO need to set this at a certain frame!
        # self.animation.cur_frame = self.oldanimation.last_played
        self.setAnimation('shoot')
    elif self.animName == 'move' and self.moveState[1] == 0:
        self.setAnimation('stopped')

# PC tiger hits a wall
def tiger_onwall(self):
    self.stopMove()
    if self.animName != 'stopped':
        self.setAnimation('stopped')

# PC tiger stops
# def tiger_onstop(self):
#     return

########## PROJECTILE ##########
# Button hits something
def button_onhit(self):
    # remove the button from the screen
    if self in projectile.Projectiles.projectiles:
        projectile.Projectiles.projectiles.remove(self)

########## tiglet ##########
# Tiglet hit by something
#TODO need tigglette object.ini's!
def tiglet_onhit(self):
    # 
    return

# Tiglet hits something (PC)
def tiglet_hit(self):
    return

# Tiglet dies
def tiglet_ondie(self):
    return

########## PIGLET ###########
# Piglet gets hit
def piglet_onhit(self):
    # set swinging
    self.health -= 1
    if self.animName != 'swing':
        self.setAnimation('swing')

# Piglet on bump
def piglet_onbump(self):
    if self.animName != 'swing':
        self.setAnimation('swing')

# Piglet done swinging
def piglet_swung(self):
    if self.animName != 'stopped':
        self.setAnimation('stopped')

# Piglet dies
def piglet_ondie(self):
    return

########### EEYORE ###########
# Eeyore gets hit
def eeyore_onhit(self):
    # decrement health
    # health -= 1
    return

# Eeyore dies
def eeyore_ondie(self):
    return
