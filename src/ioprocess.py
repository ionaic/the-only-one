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
    keyDownCBs = dict()
    keyUpCBs = dict()
    quitCB = sys.exit

    keyLeft = lambda self: self.game.knight.setDirection(2)
    keyRight = lambda self: self.game.knight.setDirection(6)
    keyUp = keyRight
    #keyUp = lambda self: self.game.knight.setDirection(4)
    keyDown = keyLeft
    #keyDown = lambda self: self.game.knight.setDirection(0)

    defaultKeys = (pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d, pygame.K_UP, pygame.K_w, pygame.K_DOWN, pygame.K_s)
    defaultDownFuns = (keyLeft, keyLeft, keyRight, keyRight, keyUp, keyUp, keyDown, keyDown)
    defaultUpFuns = [keyDown for i in range(0, 8)]

    # __init(self, Game)
    def __init__(self, gameobj):
        self.game = gameobj
        # register default callback functions
        self.registerCallback(eventStr(pygame.QUIT), self.quitCB)
        self.registerCallback(eventStr(pygame.KEYDOWN), self.keyDownCB)
        self.registerCallback(eventStr(pygame.KEYUP), self.keyUpCB)
        
        # movement state variable
        self.moveState = [False for i in range(0, 8)]

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
            self.keyDownCBs[keyname](self)

    # keyup callback function
    def keyUpCB(self, event):
        keyname = keyStr(event.key)
        if keyname in self.keyUpCBs:
            self.keyUpCBs[keyname](self)

    # movement functions: 0-Down, 2-Left, 4-up, 6-right
    # moveLeft function
    def moveLeft(self):
        # move state (in terms of animation) is now left
        print 'choose left animation!'
        if self.moveState[0] == True:
            # if going down, now left and down
            self.moveState[1] = True
            self.moveState[0] = False
            self.moveState[2] = False
        if self.moveState[4] == True:
            # if going up, now left and up
            self.moveState[3] = True
            self.moveState[2] = False
            self.moveState[4] = False
        if self.moveState[6] == True:
            # if going right, stop and go left
            self.moveState[2] = True
            self.moveState[6] = False

    # moveRight function
    def moveRight(self):
        # move state (in terms of animation) is now left
        print 'choose right animation!'
        if self.moveState[0] == True:
            # if going down, now right and down
            self.moveState[7] = True
            self.moveState[0] = False
            self.moveState[6] = False
        if self.moveState[2] == True:
            # if going left, stop and go right
            self.moveState[2] = False
            self.moveState[6] = True
        if self.moveState[4] == True:
            # if going up, now right and up
            self.moveState[5] = True
            self.moveState[4] = False
            self.moveState[6] = False
            
    # moveUp function
    def moveUp(self):
        # move state (in terms of animation) is now left
        print 'choose up animation!'
        if self.moveState[0] == True:
            # moving down, stop and go up
            self.moveState[2] = True
            self.moveState[6] = False
        if self.moveState[1] == True:
        if self.moveState[2] == True:
            # if going left, now up and left
            self.moveState[1] = True
            self.moveState[0] = False
            self.moveState[2] = False
        if self.moveState[3]:
        if self.moveState[6] == True:
            # if going up, now left and up
            self.moveState[3] = True
            self.moveState[2] = False
            self.moveState[4] = False
            
    # moveDown function
    def moveDown(self):
        # move state (in terms of animation) is now left
        print 'choose down animation!'
        if self.moveState[2] == True:
            # if going right, stop and go left
            self.moveState[6] = False
            self.moveState[2] = True
        if self.moveState[4] == True:
            # if going down, now left and down
            self.moveState[1] = True
            self.moveState[2] = False
            self.moveState[0] = False
        if self.moveState[6] == True:
            # if going up, now left and up
            self.moveState[3] = True
            self.moveState[2] = False
            self.moveState[4] = False
