# IO functions for use with pygame
# IOfunctions.py
import pygame, sys, movement
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
        self.mover = movement.Movement(self.game, self)
        # register default callback functions
        self.registerCallback(eventStr(pygame.QUIT), self.quitCB)
        self.registerCallback(eventStr(pygame.KEYDOWN), self.keyDownCB)
        self.registerCallback(eventStr(pygame.KEYUP), self.keyUpCB)

        self.defaultKeys = (pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d, pygame.K_UP, pygame.K_w, pygame.K_DOWN, pygame.K_s)
        self.defaultDownFuns = (self.mover.moveLeft, self.mover.moveLeft, self.mover.moveRight, self.mover.moveRight, self.mover.moveUp, self.mover.moveUp, self.mover.moveDown, self.mover.moveDown)
        self.defaultUpFuns = [self.mover.stopMove for i in range(0, 8)]
        
        # register default key press callbacks
        self.registerKeyPress(pygame.K_ESCAPE, self.quitCB)
        map(self.registerKeyPress, self.defaultKeys, self.defaultDownFuns)
        # register default key release callbacks
        self.registerKeyRelease(pygame.K_ESCAPE, self.quitCB)
        map(self.registerKeyRelease, self.defaultKeys, self.defaultUpFuns)
   
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
        #if type(key) is 'int':
        #    print 'registerkeypress ' + keyStr(key) + '\n'
        self.keyDownCBs[keyStr(key)] = func
        #elif type(key) is 'str':
        #    print 'registerkeypress ' + str(key) + '\n'
        #    self.keyDownCBs[key] = func
        #else:
        #    print "press " + str(type(key)) + '\n'
        #    self.keyDownCBs[str(key)] = func

    # unregisterKeyPress(self, string)
    def unregisterKeyPress(self, key):
        if key in self.keyDownCBs:
            del self.keyUpCBs[key]
   
    # registerKeyPress(self, string, function(pygame.Event))
    def registerKeyRelease(self, key, func):
        #if type(key) is 'int':
        #    print 'registerkeyrelease ' + keyStr(key) + '\n'
        self.keyUpCBs[keyStr(key)] = func
        #elif type(key) is 'str':
        #    print 'registerkeyrelease ' + str(key) + '\n'
        #    self.keyUpCBs[key] = func
        #else:
        #    print "release " + str(type(key)) + '\n'
        #    self.keyUpCBs[str(key)] = func

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
    # keyDownCB(pygame.Event)
    def keyDownCB(self, event):
        keyname = keyStr(event.key)
        if keyname in self.keyDownCBs:
            self.keyDownCBs[keyname]()

    # keyup callback function
    def keyUpCB(self, event):
        keyname = keyStr(event.key)
        if keyname in self.keyUpCBs:
            self.keyUpCBs[keyname]()
