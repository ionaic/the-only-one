# functions to handle game logic
# interactions.py
# Author: Ian Ooi

import animatedobject, movement

class Character(animatedobject.AnimationState, movement.Movement):
    def __init_(self, obj, game, hp, ammo):
        AnimationState.__init__(obj)
        Movement.__init__(obj, game)
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
    self.health -= 1
    # play hit animation
    # play hit sound
    # stop all in progress player actions
    # invulnerable for x amount of time
    # while invulnerable, can't shoot
    return

# PC tiger shoots/throws something
def tiger_onshoot(self):
    # launch projectile
    # play launching animation
    # play launch sound
    # begin tracking aninmation
    return

# PC tiger uses walljump attack
def tiger_onwalljump(self):
    # move to closest wall
    # play launch animation/sound
    # move tigger toward opposite wall
    # play land animation/sound
    # damage everything in straight line path that is a 
    #   rectangle with dim (pathlength, tiggerwidth)
    return

# PC tiger uses jump attack
def tiger_onjump(self):
    # play launching/jumping animation
    # launch into air (offscreen)
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
    if self.moveState[0] != -1:
        self.setAnimation('move')
    else:
        self.setAnimation('stopped')

# PC tiger stops
# def tiger_onstop(self):
#     return

########## PROJECTILE ##########
# Button hits something
def button_onhit(self):
    # remove the button from the screen
    return

########## tiglet ##########
# Tiglet hit by something
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
    self.setAnimation('swing')
    return

# Piglet dies
def piglet_ondie(self):
    return

########### EEYORE ###########
# Eeyore gets hit
def eeyore_onhit(self):
    return

# Eeyore dies
def eeyore_ondie(self):
    return
