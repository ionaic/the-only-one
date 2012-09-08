# IO functions for use with pygame
# IOfunctions.py
import movement

class IOfunctions:
    callbacks = dict()

    def __init__(self):
        self.super()
        # register quit callback function
        self.callbacks[QUIT] = lambda:
            pygame.quit()
            sys.exit()

    def registerCallback(self, event, func):
        self.callbacks[event] = func
    
    def unregisterCallback(self, event):
        if event in self.callbacks:
            del self.callbacks[event]

    def retrieveEvent(self, event):
        return self.callbacks[event]

    def handleEvents(self, eventList):
        for event in eventList:
            self.callbacks[event]

# keydown callback function
# def keyDownCB(event):
#     if event.key in (K_LEFT, K_a):
#         velDir = (-1, velDir[1])
#     elif event.key in (K_RIGHT, K_d):
#         velDir = (1, velDir[1])
#     elif event.key in (K_UP, K_w):
#         velDir = (velDir[0], -1)
#     elif event.key in (K_DOWN, K_s):
#         velDir = (velDir[0], 1)
#     elif event.key == K_ESCAPE:
#         quitCB()

# keyup callback function
# def keyUpCB(event):
