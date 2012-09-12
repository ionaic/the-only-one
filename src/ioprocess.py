# IO functions for use with pygame
# IOfunctions.py
import sys
import pygame
import movement
import operator
# how do you even...i don't...how should this work....
#from pygame import event.event_name as eventStr

eventStr = pygame.event.event_name
keyStr = pygame.key.name

class IOFunctions:
    callbacks = dict()
    keyDownCBs = dict()
    keyUpCBs = dict()
    quitCB = sys.exit

    # keyLeft = lambda self: self.game.tiger.setDirection(2)
    # keyRight = lambda self: self.game.tiger.setDirection(6)
    keyLeft = lambda self: self.moveLeft
    keyRight = lambda self: self.moveRight
    keyUp = keyRight
    #keyUp = lambda self: self.game.tiger.setDirection(4)
    keyDown = keyLeft
    #keyDown = lambda self: self.game.tiger.setDirection(0)


    # __init(self, Game)
    def __init__(self, gameobj):
        self.game = gameobj
        # register default callback functions
        self.registerCallback(eventStr(pygame.QUIT), self.quitCB)
        self.registerCallback(eventStr(pygame.KEYDOWN), self.keyDownCB)
        self.registerCallback(eventStr(pygame.KEYUP), self.keyUpCB)

        self.defaultKeys = (pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d, pygame.K_UP, pygame.K_w, pygame.K_DOWN, pygame.K_s)
        # self.defaultDownFuns = (self.keyLeft, self.keyLeft, self.keyRight, self.keyRight, self.keyUp, self.keyUp, self.keyDown, self.keyDown)
        self.defaultDownFuns = (self.moveLeft, self.moveLeft, self.moveRight, self.moveRight, self.moveUp, self.moveUp, self.moveDown, self.moveDown)
        self.defaultUpFuns = [self.stopMove for i in range(0, 8)]
        
        # movement state variable
        self.moveState = [-1, 10]

        # register default key press callbacks
        self.registerKeyPress(pygame.K_ESCAPE, self.quitCB)
        map(self.registerKeyPress, self.defaultKeys, self.defaultDownFuns)
        # register default key release callbacks
        self.registerKeyRelease(pygame.K_ESCAPE, self.quitCB)
        map(self.registerKeyRelease, self.defaultKeys, self.defaultUpFuns)
        self.registerKeyPress(pygame.K_LEFT, self.moveLeft)
   
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

    def moveChar(self, moveState):
        # direction of movement [x, y]
        direction = [0,0]
        if not moveState[0] == -1:
            moveMagnitude = [10,10]
        if moveState[0] == 0:
            # down (south)
            direction = [0, 1]
        elif moveState[0] == 1:
            # down/left (southwest)
            direction = [-1, 1]
        elif moveState[0] == 2:
            # left (west)
            direction = [-1, 0]
        elif moveState[0] == 3:
            # up/left (northwest)
            direction = [-1, 1]
        elif moveState[0] == 4:
            # up (north)
            direction = [0, -1]
        elif moveState[0] == 5:
            # up/right (northeast)
            direction = [1, -1]
        elif moveState[0] == 6:
            # right (east)
            direction = [1, 0]
        elif moveState[0] == 7:
            # down/right (southeast)
            direction = [1, 1]
        
        move = map(operator.mul, direction, moveMagnitude)
        move = map(operator.add, move, self.game.tiger.getPos())
        self.game.tiger.setNewPos(move[0], move[1])


    # movement functions: 0-Down, 2-Left, 4-up, 6-right
    # moveLeft function
    def moveLeft(self):
        # move state (in terms of animation) is now left
        print 'choose left animation!'
        self.game.tiger.setDirection(2)
        if self.moveState[0] in (0, 1, 7):
            self.moveState[0] = 1
        elif self.moveState[0] in (3, 4, 5):
            self.moveState[0] = 3 
        elif self.moveState[0] in (-1, 2, 6):
            self.moveState[0] = 2
        
        self.moveChar(self.moveState)
    
    # moveRight function
    def moveRight(self):
        # move state (in terms of animation) is now left
        print 'choose right animation!'
        self.game.tiger.setDirection(6)
        if self.moveState[0] == 0:
            # if going down, now right and down
            self.moveState[0] = 7
        elif self.moveState[0] == 1:
            # if going down and left, down and right
            self.moveState[0] == 7
        elif self.moveState[0] == 2:
            # if going left, go right
            self.moveState[0] = 6
        elif self.moveState[0] == 3:
            self.moveState[0] = 5
        elif self.moveState[0] == 4:
            self.moveState[0] = 5 
        # if 5, 6, 7, stay 5, 6, 7
        elif self.moveState[0] == -1:
            self.moveState[0] = 6

        self.moveChar(self.moveState)

    # moveUp function
    def moveUp(self):
        # move state (in terms of animation) is now left
        print 'choose up animation!'
        self.game.tiger.setDirection(2)
        if self.moveState[0] == 0:
            self.moveState[0] = 4
        elif self.moveState[0] == 1:
            self.moveState[0] == 3
        elif self.moveState[0] == 2:
            self.moveState[0] = 3
        elif self.moveState[0] == 6:
            self.moveState[0] = 5
        elif self.moveState[0] == 7:
            self.moveState[0] = 5
        elif self.moveState[0] == -1:
            self.moveState[0] = 4

        self.moveChar(self.moveState)

    # moveDown function
    def moveDown(self):
        # move state (in terms of animation) is now left
        print 'choose down animation!'
        self.game.tiger.setDirection(6)
        if self.moveState[0] == 2:
            self.moveState[0] = 1
        elif self.moveState[0] == 3:
            self.moveState[0] == 1
        elif self.moveState[0] == 4:
            self.moveState[0] = 0
        elif self.moveState[0] == 5:
            self.moveState[0] = 7
        elif self.moveState[0] == 6:
            self.moveState[0] = 7
        elif self.moveState[0] == -1:
            self.moveState[0] = 0

        self.moveChar(self.moveState)

    def stopMove(self):
        #stop motion
        self.moveState = [-1, 0]
