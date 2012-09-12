# IO functions for use with pygame
# IOfunctions.py
import sys
import pygame
import movement
# how do you even...i don't...how should this work....
#from pygame import event.event_name as eventStr

eventStr = pygame.event.event_name
keyStr = pygame.key.name

class IOFunctions:
    callbacks = dict()
    keyCBs = dict()
    quitCB = sys.exit
    knightPointDir = lambda x: self.game.knight.setDirection(x)

    # __init(self, Game)
    def __init__(self, gameobj):
        self.game = gameobj
        # register quit callback function
        print str(pygame.QUIT) + '\n'
        # register default callback functions
        self.registerCallback(eventStr(pygame.QUIT), self.quitCB)
        self.registerCallback(eventStr(pygame.KEYDOWN), self.keyDownCB)
        self.registerCallback(eventStr(pygame.KEYUP), self.keyUpCB)
        # register default key callbacks
        self.registerKey(keyStr(pygame.K_ESCAPE), self.quitCB)
   
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

    # registerKey(self, string, function(pygame.Event))
    def registerKey(self, key, func):
        if type(key) is 'int':
            self.keyCBs[keyStr(key)] = func
        elif type(key) is 'str':
            self.keyCBs[key] = func
        else:
            self.keyCBs[str(key)] = func

    # unregisterKey(self, string)
    def unregisterKey(self, key):
        if key in self.keyCBs:
            del self.callbacks[key]
   
    # keydown callback function
    # keyDownCB(pygame.Event)
    def keyDownCB(self, event):
        if event.key in (pygame.K_LEFT, pygame.K_a):
            # Left (or a)
            self.game.knight.setDirection(2)
            print 'left down!'
        elif event.key in (pygame.K_RIGHT, pygame.K_d):
            # Right (or d)
            self.game.knight.setDirection(6)
            print 'right down!'
        elif event.key in (pygame.K_UP, pygame.K_w):
            # Up (or w)
            self.game.knight.setDirection(4)
            print 'up down!'
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            # Down (or s)
            self.game.knight.setDirection(0)
            print 'down down!'
        elif event.key == pygame.K_ESCAPE:
            self.quitCB()

    # keyup callback function
    def keyUpCB(self, event):
        if event.key in (pygame.K_LEFT, pygame.K_a):
            # Left (or a)
            self.game.knight.setDirection(0)
            print 'left up!'
        elif event.key in (pygame.K_RIGHT, pygame.K_d):
            # Right (or d)
            self.game.knight.setDirection(0)
            print 'right up!'
        elif event.key in (pygame.K_UP, pygame.K_w):
            # Up (or w)
            self.game.knight.setDirection(0)
            print 'up up!'
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            # Down (or s)
            self.game.knight.setDirection(0)
            print 'down up!'
        elif event.key == pygame.K_ESCAPE:
            # Escape
            self.quitCB()

    # handleEvents(self, [pygame.Event])
    def handleEvents(self, eventList):
        for event in eventList:
            #print 'event is: ' + event.event_name(event.type) + '\n'
            if eventStr(event.type) in self.callbacks:
                self.callbacks[eventStr(event.type)](event)
