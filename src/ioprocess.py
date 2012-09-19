# IO functions for use with pygame
# IOfunctions.py
# author Ian Ooi
import pygame, sys, movement, interactions
# how do you even...i don't...how should this work....
#from pygame import event.event_name as eventStr

eventStr = pygame.event.event_name
keyStr = pygame.key.name

class IOFunctions:
    callbacks = dict()
    keyDownCBs = dict()
    keyUpCBs = dict()
    quitCB = sys.exit

    # __init(self, Game)
    def __init__(self, gameobj):
        self.game = gameobj
        self.mover = self.game.tiger.move
        # register default callback functions
        self.registerCallback(eventStr(pygame.QUIT), self.quitCB)
        self.registerCallback(eventStr(pygame.KEYDOWN), self.defaultKeyDown)
        self.registerCallback(eventStr(pygame.KEYUP), self.defaultKeyUp)

        self.defaultKeys = (pygame.K_LEFT,  pygame.K_a, pygame.K_h, \
                            pygame.K_RIGHT, pygame.K_d, pygame.K_l, \
                            pygame.K_UP,    pygame.K_w, pygame.K_k, \
                            pygame.K_DOWN,  pygame.K_s, pygame.K_j)
        self.defaultDownFuns = (self.mover.moveLeft,  self.mover.moveLeft, \
                                self.mover.moveLeft, \
                                self.mover.moveRight, self.mover.moveRight, \
                                self.mover.moveRight, \
                                self.mover.moveUp,    self.mover.moveUp, \
                                self.mover.moveUp, \
                                self.mover.moveDown,  self.mover.moveDown, \
                                self.mover.moveDown)
        self.defaultUpFuns =   (self.mover.stopLeft,  self.mover.stopLeft, \
                                self.mover.stopLeft, \
                                self.mover.stopRight, self.mover.stopRight, \
                                self.mover.stopRight, \
                                self.mover.stopUp,    self.mover.stopUp, \
                                self.mover.stopUp, \
                                self.mover.stopDown,  self.mover.stopDown, \
                                self.mover.stopDown)
        
        # register default key press callbacks
        # escape to quit
        self.registerKeyPress(pygame.K_ESCAPE, self.quitCB)
        # space to shoot
        self.registerKeyPress(pygame.K_SPACE, self.shootCB)
        self.registerKeyPress(pygame.K_RETURN, self.shootCB)
        # shift to ground pound attack
        self.registerKeyPress(pygame.K_e, self.jumpCB)
        self.registerKeyPress(pygame.K_LSHIFT, self.jumpCB)
        self.registerKeyPress(pygame.K_RSHIFT, self.jumpCB)
        # wasd/arrow keys/hjkl to move
        map(self.registerKeyPress, self.defaultKeys, self.defaultDownFuns)
        # register default key release callbacks
        # escape to quit
        self.registerKeyRelease(pygame.K_ESCAPE, self.quitCB)
        # wasd/arrow keys/hjkl movement
        map(self.registerKeyRelease, self.defaultKeys, self.defaultUpFuns)
    
    def shootCB(self):
        #self.game.bullets.spawnProjectile(self.game.tiger.getX(), self.game.tiger.getY(), self.mover.moveState[0])
        interactions.tiger_onshoot(self.game.tiger)
    
    def launchCB(self):
        # find the nearest wall and launch off it
        interactions.tiger_onlaunch(self.game.tiger)
        
    def jumpCB(self):
        # jump and ground pound
        interactions.tiger_onjump(self.game.tiger)

    # registerCallback(self, string, function(pygame.Event)) 
    def registerCallback(self, event, func):
        self.callbacks[event] = func

    # unregisterCallback(self, string)
    def unregisterCallback(self, event):
        if event in self.callbacks:
            del self.callbacks[event]

    # retrieveEvent(self, string)
    def retrieveEvent(self, event):
        if not event in self.callbacks:
            self.callbacks[eventStr(event.type)] = lambda e: None
        return self.callbacks[eventStr(event.type)]

    # registerKeyPress(self, string, function(pygame.Event))
    def registerKeyPress(self, key, func):
        self.keyDownCBs[keyStr(key)] = func

    # unregisterKeyPress(self, string)
    def unregisterKeyPress(self, key):
        if key in self.keyDownCBs:
            del self.keyUpCBs[key]
   
    # registerKeyPress(self, string, function(pygame.Event))
    def registerKeyRelease(self, key, func):
        self.keyUpCBs[keyStr(key)] = func

    # unregisterKeyRelease(self, string)
    def unregisterKeyRelease(self, key):
        if key in self.keyUpCBs:
            del self.keyUpCBs[key]

    # handleEvents(self, [pygame.Event])
    def handleEvents(self, eventList):
        for event in eventList:
            if eventStr(event.type) in self.callbacks:
                self.callbacks[eventStr(event.type)](event)

    # CALLBACK FUNCTIONS
    # keydown callback function
    # defaultKeyDown(pygame.Event)
    def defaultKeyDown(self, event):
        keyname = keyStr(event.key)
        if keyname in self.keyDownCBs:
            self.keyDownCBs[keyname]()

    # keyup callback function
    def defaultKeyUp(self, event):
        keyname = keyStr(event.key)
        if keyname in self.keyUpCBs:
            self.keyUpCBs[keyname]()
