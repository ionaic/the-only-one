# IO functions for use with pygame
# IOfunctions.py
import sys
import pygame
import movement

class IOFunctions:
    callbacks = dict()

    def __init__(self, gameobj):
        self.game = gameobj

        # register quit callback function
        self.callbacks[pygame.QUIT] = lambda: sys.exit()
        
    # keydown callback function
    def keyDownCB(event):
        if event.key in (K_LEFT, K_a):
            #velDir = (-1, velDir[1])
            print 'left down!'
        elif event.key in (K_RIGHT, K_d):
            #velDir = (1, velDir[1])
            print 'right down!'
        elif event.key in (K_UP, K_w):
            #velDir = (velDir[0], -1)
            print 'up down!'
        elif event.key in (K_DOWN, K_s):
            #velDir = (velDir[0], 1)
            print 'down down!'
        elif event.key == K_ESCAPE:
            quitCB()

    # keyup callback function
    def keyUpCB(event):
        if event.key in (K_LEFT, K_a):
            #velDir = (-1, velDir[1])
            print 'left up!'
        elif event.key in (K_RIGHT, K_d):
            #velDir = (1, velDir[1])
            print 'right up!'
        elif event.key in (K_UP, K_w):
            #velDir = (velDir[0], -1)
            print 'up up!'
        elif event.key in (K_DOWN, K_s):
            #velDir = (velDir[0], 1)
            print 'down up!'
        elif event.key == K_ESCAPE:
            quitCB()

    def NOOP():
        return

    def registerCallback(self, event, func):
        self.callbacks[event] = func
    
    def unregisterCallback(self, event):
        if event in self.callbacks:
            del self.callbacks[event]

    def retrieveEvent(self, event):
        if not event in self.callbacks:
            self.callbacks[event] = NOOP()
        return self.callbacks[event]

    def handleEvents(self, eventList):
        for event in eventList:
            if event in self.callbacks:
                self.callbacks[event]
            else:
                self.callbacks[event] = NOOP()
