# functions to handle game logic
# interactions.py
# Author: Ian Ooi

import projectile, audio, math, random, animatedobject, animationstate, game, operator
import eventhandler, pygame, collisions, time

def gpActivate():
    self=game.Game.universal.tiger 
    game.Game.universal.groundpound.setPos(self.x+75-150,self.y+115-150)
    game.Game.universal.gpactive = True
def registerCallbacks():
    eventhandler.registerEvent('beefy_test',lambda x: beefyHi(x))
    eventhandler.registerEvent('tiger_test',lambda x: takeAStep(x))
    eventhandler.registerEvent('eeyoresniffle',lambda x: eeyoreSniffle(x))
    eventhandler.registerEvent('ropeSwing',lambda x: ropeSwing(x))
    eventhandler.registerEvent('tiger_sneak',lambda x: tigerSneak(x))
    eventhandler.registerEvent('tiger_sneak_stop',lambda x: tigerSneakStop(x))
    eventhandler.registerEvent('pig_sound',lambda x: pigSound(x))
    eventhandler.registerEvent('tigerShoot',lambda x: shootCB())
    eventhandler.registerEvent('gpShiftUp',lambda x: groundpoundShiftUp())
    eventhandler.registerEvent('gpShiftDown',lambda x: groundpoundShiftDown())
    eventhandler.registerEvent('beefPunch', lambda x: beefPunch())
    eventhandler.registerEvent('tiger_stop',lambda x: stopWalking(x))
    eventhandler.registerEvent('groundpound',lambda x: gpActivate())
    global sound
    global stepping
    global sneaking
    global sneak
    global counter
    global sniffling 
    sniffling = False
    counter = 0
    sneaking = False
    stepping = False
    sneak = pygame.mixer.Sound("../assets/audio/sfx/sneak.wav")
    sound = pygame.mixer.Sound("../assets/audio/sfx/step.wav")
    sound.play(-1)
    sneak.play(-1)
    sneak.stop()
    sound.stop()
    
def beefyHi(X):
    choice = random.randrange(1,16,1)
    if choice==1:
        audio.mySounds["beefydestroy"].play()
        
def pigSound(X):
    #play a sound 20% of the time, randomize between the three
    choice = random.randrange(1,16,1)
    if choice==1:
        audio.mySounds["pigsound"].play()
    elif choice==2:
        audio.mySounds["pigsound2"].play()
    elif choice==3:
        audio.mySounds["pigsound3"].play()
    #else:
        #print "no sound today, come again tomorrow"

    #print choice

def tigerSneak(X):
    global sneaking
    global sneak
    global counter
    if not sneaking:
        sneaking = True
        sneak.play(-1)
    elif counter %8 == 0:
        sneak.stop()
        sneaking = False
        audio.mySounds["swag"].play()
    counter += 1
        
        
def tigerSneakStop(X):
    global sneaking
    global sneak
    counter=0
    if sneaking:
        sneaking = False
        sneak.stop()
	
def ropeSwing(X):
	choice = random.randrange(1,5,1)
	if choice==1:
		audio.mySounds["rope"].play()
	elif choice==2:
		audio.mySounds["rope2"].play()
	elif choice==3:
		audio.mySounds["rope3"].play()
	elif choice==4:
		audio.mySounds["rope4"].play()
	else:
		print "FAIL"
	
	#print choice
	
def eeyoreSniffle(X):
    global sniffling
    if not sniffling:
        sniffling = True
        audio.mySounds["eeyoresniffle"].play(1)
	    	
def stopWalking(x):
    print "stopping"
    global stepping
    global sound
    counter = 0
    if stepping:
        stepping = False
        sound.stop()
	
def takeAStep(X):

    global counter
    global stepping
    global sound
    
    if not stepping:
        stepping = True
        sound.play(-1)
    elif counter %8 == 0:
        sound.stop()
        stepping = False
        audio.mySounds["swag"].play()
        
    counter += 1


	#time.sleep(3)
	#a.pause()
	#print a.playing
	
	
def collide(obj1, obj2):
    if not isinstance(obj1,pygame.Rect):
        thing1 = obj1.object.tag
    else:
        thing1 = 'none'
    if not isinstance(obj2,pygame.Rect):
        thing2 = obj2.object.tag
    else:
        thing2 = 'none'

    if thing1 == 'tiger':
        if thing2 == 'tiglet':
            tiglet_hit(obj2)
            tiger_onhit(obj1)
        elif thing2 == 'stuffing':
            tiger_pickupstuffing(obj1)
            stuffing_pickup(obj2, obj1.game)
        elif thing2 == 'none':
            tiger_onwall(obj1,obj2)
        elif thing2 == 'tree':
            tiger_onwall(obj1,obj2.getFrameByNumber(0).collisionArea.move(obj2.getPos()))
    elif thing1=='tree':
        if thing2=='tiger':
            tiger_onwall(obj2,obj1.getFrameByNumber(0).collisionArea.move(obj1.getPos()))
    elif thing1 == 'tiglet':
        if thing2 == 'tiger':
            tiglet_hit(obj1)
            tiger_onhit(obj2)
        elif thing2 == 'button':
            tiglet_onhit(obj1)
            button_onhit(obj2)
        elif thing2 == 'groundpound':
            tiglet_onhit(obj1)
        elif thing2 == 'punch':
            tiglet_onhit(obj1)
        elif thing2 == 'none':
            tiglet_onwall(obj1, obj2)
    elif thing1 == 'pig':
        if thing2 == 'button':
            piglet_onhit(obj1)
            button_onhit(obj2)
        elif thing2 == 'groundpound':
            piglet_onhit(obj1)
        elif thing2 == 'punch':
            piglet_onhit(obj1)
    elif thing1 == 'eeyore':
        if thing2 == 'button':
            eeyore_onhit(obj1)
            button_onhit(obj2)
        elif thing2 == 'groundpound':
            eeyore_onhit(obj1)
        elif thing2 == 'punch':
            eeyore_onhit(obj1)
    elif thing1 == 'button':
        if thing2 == 'pig':
            button_onhit(obj1)
            piglet_onhit(obj2)
        elif thing2 == 'tiglet':
            tiglet_onhit(obj2)
            button_onhit(obj1)
        elif thing2 == 'beefy':
            beefy_onhit(obj2)
            button_onhit(obj1)
        elif thing2 == 'eeyore':
            eeyore_onhit(obj2)
            button_onhit(obj1)
    elif thing1 == 'stuffing':
        if thing2 == 'tiger':
            stuffing_pickup(obj1, obj2.game)
            tiger_pickupstuffing(obj2)
    elif thing1 == 'beefy':
        if thing2 == 'button':
            beefy_onhit(obj1)
            button_onhit(obj2)
        elif thing2 == 'groundpound':
            beefy_onhit(obj1)
        elif thing2 == 'punch':
            beefy_onhit(obj1)
        elif thing2 == 'none':
            beefy_onwall(obj1, obj2)
    elif thing1 == 'none':
        if thing2 == 'pig':
            piglet_onhit(obj2)
        elif thing2 == 'tiger':
            tiger_onwall(obj2,obj1)
        elif thing2 == 'tiglet':
            tiglet_onwall(obj2, obj1)
        elif thing2 == 'beefy':
            beefy_onwall(obj2, obj1)
    elif thing1 == 'groundpound':
        if thing2 == 'tiglet':
            tiglet_onhit(obj2)
        elif thing2 == 'eeyore':
            eeyore_onhit(obj2)
        elif thing2 == 'beefy':
            beefy_onhit(obj2)
        elif thing2 == 'pig':
            piglet_onhit(obj2)
    elif thing1 == 'punch':
        if thing2 == 'tiglet':
            tiglet_onhit(obj2)
        elif thing2 == 'eeyore':
            eeyore_onhit(obj2)
        elif thing2 == 'beefy':
            beefy_onhit(obj2)
        elif thing2 == 'pig':
            piglet_onhit(obj2)

########## TIGER ##########
# PC tiger hit by something
def tiger_onhit(self):
    if self.animName == 'groundpound':
        return
    if self.LAST_HIT == 0:
        self.LAST_HIT = self.game.time.time()
    if self.game.time.time() - self.LAST_HIT > 700:
        self.LAST_HIT = self.game.time.time()
        # decrement health
        self.health -= 1
        # play hit animation
        self.setAnimation('damaged')
        #self.stopMove()
        # play hit sound
        choice = random.randrange(1,4,1)
        if choice==1:
            audio.mySounds["tigerdamage"].play()
        elif choice==2:
            audio.mySounds["tigerdamage2"].play()
        elif choice==3:
            audio.mySounds["tigerdamage3"].play()
        else:
            print "FAIL"
        #print choice    # stop all in progress player actions

        if self.health <= 0:
            print "YOU DIED!!!!!"
            tiger_ondie(self)
        # invulnerable for x amount of time
        # while invulnerable, can't shoot
    #else:
    #    print "Last hit: " + str(self.LAST_HIT) + "; Cur Time: " + str(self.game.time.time())

def shootCB():
    game.Game.universal.bullets.spawnProjectile(game.Game.universal.tiger.getX() + 30, game.Game.universal.tiger.getY() + 20, game.Game.universal.tiger.move.moveState[0])
    game.Game.universal.tiger.ammo -= 1

# PC tiger shoots/throws something
def tiger_onshoot(self):
    if self.LAST_THROW == 0:
        self.LAST_THROW = self.game.time.time()
    if self.game.time.time() - self.LAST_THROW > 500:
        self.LAST_THROW = self.game.time.time()
        # check if tiger has enough ammo left
        if self.animName == 'shoot':
            return
        if self.has_ammo():
            # launch projectile
            #self.game.bullets.spawnProjectile(self.getX() + 30, self.getY() + 20, self.move.moveState[0])
            self.throwing = True
            # reduce amount of available ammo
            #self.ammo -= 1
            # play throwing animation
            if self.animName != 'move':
                #print "should shoot!"
                self.setAnimationOnce('shoot')
            else:
                #print "should moveshoot!"
                self.setAnimationOnce('moveshoot')
            # play throw sound
            # begin tracking animation
        else:
            print "Out of ammo!"
    #else:
    #    print "Last throw: " + str(self.LAST_THROW) + "; Cur Time: " + str(self.game.time.time())

# PC tiger uses walljump attack
def tiger_onwalljump(self):
    # move to closest wall
    # play launch animation
    self.setAnimation('launch')
    # play spring jump sound
    audio.mySounds["spring"].play()
    # move tiger toward opposite wall
    # play land animation/sound
    # damage everything in straight line path that is a 
    #   rectangle with dim (pathlength, tigerwidth)
    return

def groundpoundShiftDown():
    print 'resetting to original spot'
    tigerPos = game.Game.universal.tiger.getPos()
    print 'shifted pos ' + str(tigerPos)
    newTigerPos = (tigerPos[0], tigerPos[1] + 80)
    print 'unshifted pos ' + str(newTigerPos)
    game.Game.universal.tiger.setPosVec(newTigerPos)
    game.Game.universal.tiger.stashPos = newTigerPos

def groundpoundShiftUp():
    tigerPos = game.Game.universal.tiger.getPos()
    newTigerPos = (tigerPos[0], tigerPos[1] - 80)
    game.Game.universal.tiger.setPosVec(newTigerPos)

# PC tiger uses jump attack
def tiger_onjump(self):
    # play launching/jumping animation
    # launch into air (offscreen)
    self.setAnimationOnce('groundpound')
    # damage nearby things
    neighborhood = pygame.Rect(self.x+75-150,self.y+115-150,300,300)
    topleft = (neighborhood.left, neighborhood.top)
    topright = (neighborhood.right, neighborhood.top)
    bottomleft = (neighborhood.left, neighborhood.bottom)
    bottomright = (neighborhood.right, neighborhood.bottom)
    #print "neighborhood " + str(neighborhood)
    #hurt_these = list()
    for obj in self.game.tilemap.objects:
        rect = obj.getFrame(self.game.time.time()).surface.get_rect()
        if neighborhood.colliderect(rect) or \
            neighborhood.contains(rect) or \
            rect.contains(neighborhood):
            obj.health -= 1
            collide(obj, self)
            #hurt_these.append(obj)

    #print 'things to damage ' + str(hurt_these)
            
    # play jump sound
    audio.mySounds["jump"].play()
    # mark potential landing spot with shadow
    # move landing spot based on key inputs
    # land
    # damage everything in region surrounding tiger
    return

# PC tiger dies
def tiger_ondie(self):
    # play death animation
    stuffing_create(self)
    self.game.enemies.remove(self)
    self.game.tilemap.enemies.remove(self)
    
    # play death sound
    audio.mySounds["selfdeath"].play()
    # stop everything onscreen
    # lose screen, retry
    return

# PC tiger moves
def tiger_onwalk(self):
    # set animation type
    #if self.moveState[0] != -1:
    if  self.move.moveState[1] != 0:
        if self.animName == 'shoot':
            self.setAnimation('moveshoot')
        elif self.animName == 'moveshoot':
            return
        elif self.animName == 'groundpound':
            return
        elif self.animName != 'move':
            self.setAnimation('move')
        #self.movePos()
    elif self.move.moveState[1] == 0:
        #if self.animName == 'moveshoot':
        #    # TODO need to set this at a certain frame!
        #    # self.animation.cur_frame = self.oldanimation.last_played
        #    self.setAnimation('shoot')
        #if self.animName == 'move':
        if self.animName == 'shoot':
            return
        elif self.animName == 'moveshoot':
            return
        elif self.animName == 'groundpound':
            return
            #self.setAnimationOnce('shoot')
        elif self.animName != 'stopped':
            self.setAnimation('stopped')
    #else:
    #    if self.animName != 'move':
    #        self.setAnimation('move')
        #self.movePos()

# PC tiger hits a wall
def tiger_onwall(self, wall):
    #self.stopMove()
    #self.setNewPos(self.getPos())
    #self.move.stopMove()
    self.x = self.stashPos[0]
    self.y = self.stashPos[1]
    time = self.game.time.time()
    frame = self.getFrame(time)
    colrect = collisions.getQRect(frame.collisionArea.move(self.getPos()))
    if wall.collidepoint(colrect.bottomleft) and wall.collidepoint(colrect.bottomright):
        print (colrect.bottom-wall.top)
        self.y = self.y - (colrect.bottom-wall.top)
    elif wall.collidepoint(colrect.topleft) and wall.collidepoint(colrect.topright):
        self.y = self.y + (wall.bottom-colrect.top)
    elif wall.collidepoint(colrect.topleft) and wall.collidepoint(colrect.bottomleft):
        self.x = self.x + (wall.right-colrect.left)
    elif wall.collidepoint(colrect.topright) and wall.collidepoint(colrect.bottomright):
        self.x = self.x - (colrect.right-wall.left)
    elif wall.collidepoint(colrect.topright):
        self.x = self.x - (colrect.right-wall.left)
        self.y = self.y + (wall.bottom-colrect.top)
    elif wall.collidepoint(colrect.bottomright):
        self.x = self.x - (colrect.right-wall.left)
        print (colrect.bottom-wall.top)
        self.y = self.y - (colrect.bottom-wall.top)
    elif wall.collidepoint(colrect.topleft):
        self.y = self.y + (wall.bottom-colrect.top)
        self.x = self.x + (wall.right-colrect.left)
    elif wall.collidepoint(colrect.bottomleft):
        self.y = self.y - (colrect.bottom-wall.top)
        self.x = self.x + (wall.right-colrect.left)

def tiger_update(self):
    self.moveChar()
    tiger_onwalk(self)

def tiger_pickupstuffing(self):
    tiger_pickupbutton(self)
    if self.health < self.MAX_HEALTH:
        self.health += 1
        print "Health: " + str(self.health)

def tiger_pickupbutton(self):
    self.ammo += 5
    print "Ammo: " + str(self.ammo)

########## PROJECTILE ##########
# Button hits something
def button_onhit(self):
    # play sound
    # remove the button from the screen
    if self in projectile.Projectiles.projectiles:
        projectile.remove(self)

########## tiglet ##########
# Tiglet hit by something
#TODO need tigglette object.ini's!
def tiglet_onhit(self):
    #print "tigletonhit " + str(self)
    # hit animation?
    # decrease health
    self.health -= 1
	
    #print "pig hit!!!"
    choice = random.randrange(1,3,1)
    if choice==1:
        audio.mySounds["pighit"].play()
    elif choice==2:
        audio.mySounds["pighit2"].play()
    else:
        print "Error choosing sound"

    #audio.mySounds["tigerdamage"].play()
    if self.health <= 0:
        tiglet_ondie(self)

# Tiglet hits something (PC)
def tiglet_hit(self):
    self.setAnimationOnce('falldown')
    self.move.stopMove()

# Tiglet dies
def tiglet_ondie(self):
    #print "tigletondie " + str(self)
    stuffing_create(self)
    self.game.enemies.remove(self)
    self.game.tilemap.enemies.remove(self)

# Tiglet moves
def tiglet_onmove(self):
    #mark = {'left':False, 'right':False, 'top':False, 'bottom':False}
    #self.getNeighborhood()
    #topleft = (self.neighborhood.left, self.neighborhood.top)
    #topright = (self.neighborhood.right, self.neighborhood.top)
    #bottomleft = (self.neighborhood.left, self.neighborhood.bottom)
    #bottomright = (self.neighborhood.right, self.neighborhood.bottom)
    #for rect in self.game.tilemap.noGo:
    #    if rect.collidepoint(topleft):
    #        mark['left'] = True
    #        mark['top'] = True
    #    if rect.collidepoint(bottomleft):
    #        mark['left'] = True
    #        mark['bottom'] = True
    #    if rect.collidepoint(topright):
    #        mark['top'] = True
    #        mark['right'] = True
    #    if rect.collidepoint(bottomright):
    #        mark['bottom'] = True
    #        mark['right'] = True
    #new_dir = [0, 0]
    #if mark['left']:
    #    if mark['right'] == False:
    #       new_dir[0] = 1
    #elif mark['right']:
    #    if mark['left'] == False:
    #        new_dir[0] = -1
    #if mark['top']:
    #    if mark['bottom'] == False:
    #        new_dir[1] = 1
    #elif mark['bottom']:
    #    if mark['top'] == False:
    #        new_dir[1] = -1

    #if new_dir != [0, 0]:
    #    self.direction = new_dir
    cur_time = self.game.time.time()
    if cur_time - self.last_time >= 800:
        print 'grabbing thingy ' + str(self.game.time.time()) + ' ' + str(self.last_time)
        self.dest = self.game.tiger.getPos()
        self.last_time = cur_time
    vel = map(operator.sub, self.dest, self.getPos())
    velMag = 1.0 * math.sqrt(vel[0]**2 + vel[1]**2)
    #print "velMag" + str(velMag)
    if velMag < 50:
        self.dest = (random.randint(200,400), random.randint(200,400))
        return
    if vel[0] < 0:
        newX = math.ceil(float(vel[0] / velMag * 2))
    else:
        newX = math.floor(float(vel[0] / velMag * 2))
        #vel = (math.floor(float(vel[0]) / velMag * 2), math.floor(float(vel[1]) / velMag * 2))
    if vel[1] < 0:
        newY = math.ceil(float(vel[1] / velMag * 2))
    else:
        newY = math.floor(float(vel[1] / velMag * 2))
        #vel = (math.floor(float(vel[0]) / velMag * 2), math.floor(float(vel[1]) / velMag * 2))
        
    self.direction = [newX, newY]
    print 'direction ' + str(self.direction)

def tiglet_onwall(self, wall):
    self.x = self.stashPos[0]
    self.y = self.stashPos[1]
    time = self.game.time.time()
    frame = self.getFrame(time)
    colrect = collisions.getQRect(frame.collisionArea.move(self.getPos()))
    if wall.collidepoint(colrect.bottomleft) and wall.collidepoint(colrect.bottomright):
        print (colrect.bottom-wall.top)
        self.y = self.y - (colrect.bottom-wall.top)
    elif wall.collidepoint(colrect.topleft) and wall.collidepoint(colrect.topright):
        self.y = self.y + (wall.bottom-colrect.top)
    elif wall.collidepoint(colrect.topleft) and wall.collidepoint(colrect.bottomleft):
        self.x = self.x + (wall.right-colrect.left)
    elif wall.collidepoint(colrect.topright) and wall.collidepoint(colrect.bottomright):
        self.x = self.x - (colrect.right-wall.left)
    elif wall.collidepoint(colrect.topright):
        self.x = self.x - (colrect.right-wall.left)
        self.y = self.y + (wall.bottom-colrect.top)
    elif wall.collidepoint(colrect.bottomright):
        self.x = self.x - (colrect.right-wall.left)
        print (colrect.bottom-wall.top)
        self.y = self.y - (colrect.bottom-wall.top)
    elif wall.collidepoint(colrect.topleft):
        self.y = self.y + (wall.bottom-colrect.top)
        self.x = self.x + (wall.right-colrect.left)
    elif wall.collidepoint(colrect.bottomleft):
        self.y = self.y - (colrect.bottom-wall.top)
        self.x = self.x + (wall.right-colrect.left)

########## PIGLET ###########
# Piglet gets hit
def piglet_onhit(self):
    # set swinging
    self.health -= 1
    if self.health <= 0:
        piglet_ondie(self)
    if self.animName != 'swing':
        self.setAnimationOnce('swing')

# Piglet on bump
def piglet_onbump(self):
    if self.animName != 'swing':
        self.setAnimationOnce('swing')

# Piglet dies
def piglet_ondie(self):
    return

########### EEYORE ###########
# Eeyore gets hit
def eeyore_onhit(self):
    # decrement health
    audio.mySounds["eeyorepain"].play()
    self.health -= 1
    if self.health <= 0:
        eeyore_ondie(self)

# Eeyore dies
def eeyore_ondie(self):
    audio.mySounds["eeyoresniffle"].stop()
    stuffing_create(self)
    if self in self.game.objects:
        self.visualDelete(self.game.tilemap.surface, self.game._screen)
        self.game.objects.remove(self)
    elif self in self.game.tilemap.objects:
        self.visualDelete(self.game.tilemap.surface, self.game._screen)
        self.game.tilemap.objects.remove(self)
    else:
        self.game.enemies.remove(self)
        self.game.tilemap.enemies.remove(self)

######### STUFFING ##########
# convert an object (self) to stuffing
def stuffing_create(self):
    stuffing = animationstate.AnimationState(self.game.stuffobj)
    stuffing.setAnimation('stuffing')
    tempPos = self.getPos()
    print tempPos
    stuffing.setPos(tempPos[0], tempPos[1] + self.getFrameByNumber(0).surface.get_height() - (self.getFrameByNumber(0).surface.get_height() - stuffing.getFrameByNumber(0).surface.get_height()))
    #self.game.tilemap.objects.append(stuffing)
    self.game.objects.append(stuffing)

def stuffing_pickup(self, game):
    if self in game.objects:
        self.visualDelete(game.tilemap.surface, game._screen)
        game.objects.remove(self)
    elif self in game.tilemap.objects:
        self.visualDelete(game.tilemap.surface, game._screen)
        game.tilemap.objects.remove(self)

########### BEEFY ##########
def beefy_onmove(self):
    tiglet_onmove(self)

def beefy_onhit(self):
    self.health -= 1
    audio.mySounds["beefydestroy"].play()
    if self.health <= 0:
        beefy_ondie(self)

def beefy_onwall(self, wall):
    tiglet_onwall(self, wall)

def beefPunch():
    game.Game.universal.tiger.health -= game.Game.universal.tiger.MAX_HEALTH / 5 
    audio.mySounds["beefypunch"].play()
    tiger_onhit(game.Game.universal.tiger)

def beefy_punch(self):
    audio.mySounds["beefypunch"].play()
    self.setAnimationOnce('punch')

def beefy_ondie(self):
    stuffing_create(self)
    if self in self.game.objects:
        self.visualDelete(self.game.tilemap.surface, self.game._screen)
        self.game.objects.remove(self)
    elif self in self.game.tilemap.objects:
        self.visualDelete(self.game.tilemap.surface, self.game._screen)
        self.game.objects.remove(self)
