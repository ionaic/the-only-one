# functions for movement
# movement.py
# author Ian Ooi
import pygame, sys, math, operator, interactions

def dirToVec(direction):
    if direction == 0:
        # down (south)
        return [0, 1]
    elif direction == 1:
        # down/left (southwest)
        return [-1, 1]
    elif direction == 2:
        # left (west)
        return [-1, 0]
    elif direction == 3:
        # up/left (northwest)
        return [-1, -1]
    elif direction == 4:
        # up (north)
        return [0, -1]
    elif direction == 5:
        # up/right (northeast)
        return [1, -1]
    elif direction == 6:
        # right (east)
        return [1, 0]
    elif direction == 7:
        # down/right (southeast)
        return [1, 1]
    else:
        return [0, 0]

def vecToDir(vec):
    if vec[0] == -1:
        if vec[1] == -1:
            return 3
        elif vec[1] == 0:
            return 2
        elif vec[1] == 1:
            return 1
        else:
            return -1
    elif vec[0] == 0:
        if vec[1] == -1:
            return 4
        elif vec[1] == 0:
            return -1
        elif vec[1] == 1:
            return 0
        else:
            return -1
    elif vec[0] == 1:
        if vec[1] == -1:
            return 5
        elif vec[1] == 0:
            return 6
        elif vec[1] == 1:
            return 7
        else:
            return -1
    else:
        return -1
    
def getSpeedState(direction):
    if direction == -1:
        return 0
    elif direction % 2 == 1:
        return __DIAG_CONST
    else:
        return 1
        
__DIAG_CONST = math.sqrt(2) * 0.5 # 1/sqrt 2 == (sqrt 2)/2 for diagonals

class Movement:
    def __init__(self, obj, game):
        # movement state variable
        self.moveState = [-1, 0]
        self.game = game
        self.obj = obj
        self.moveSpeed = [0.2,0.2]

    def moveChar(self):
        # direction of movement [x, y]
        # get the direction and magnitude of velocity

        direction = dirToVec(self.moveState[0])
        magnitude = [self.moveState[1] * self.moveSpeed[i] \
            for i in range(0, len(self.moveSpeed))]
        # produce the velocity vector from direction and magnitude
        velocity = map(operator.mul, direction, magnitude)
        # produce the new position (proposed position) from current pos and
        #   velocity
        new_pos = [0,0]
        new_pos[0] = velocity[0] * (self.game.time.time() - self.game.time.lastTime()) + self.obj.getX()
        new_pos[1] = velocity[1] * (self.game.time.time() - self.game.time.lastTime()) + self.obj.getY()
        #new_pos = map(operator.mul, velocity, (self.game.time.time() - self.game.time.lastTime() for i in range(0, 2)))
        #new_pos = map(operator.add, velocity, self.obj.getPos())
        self.obj.setPosVec(new_pos)

    def updatePos(self):
        self.moveChar()
        self.updateTiger()
        #self.obj.movePos()

    def getLeftState(self):
        if self.moveState[0] in (0, 1, 7):
            return 1
        elif self.moveState[0] in (3, 4, 5):
            return 3 
        elif self.moveState[0] in (-1, 2, 6):
            return 2
        else:
            print 'getLeft unknown state: ' + str(self.moveState)
            return -1

    def getRightState(self):
        print "right state"
        if self.moveState[0] in (0, 1, 7):
            return 7
        elif self.moveState[0] in (-1, 2, 6):
            return 6
        elif self.moveState[0] in (3, 4, 5):
            return 5
        else:
            print 'getRight unknown state: ' + str(self.moveState)
            return -1

    def getUpState(self):
        if self.moveState[0] in (-1, 0, 4):
            return 4
        elif self.moveState[0] in (1, 2, 3):
            return 3
        elif self.moveState[0] in (5, 6, 7):
            return 5
        else:
            self.animation.cur_frame = self.oldanimation.last_played
            print 'getUp unknown state: ' + str(self.moveState)
            return -1

    def getDownState(self):
        if self.moveState[0] in (-1, 0, 4):
            return 0
        elif self.moveState[0] in (1, 2, 3):
            return 1
        elif self.moveState[0] in (5, 6, 7):
            return 7
        else:
            print 'getDown unknown state: ' + str(self.moveState)
            return -1


    # movement functions: 0-Down, 2-Left, 4-up, 6-right
    # moveLeft function
    def moveLeft(self):
        # move state (in terms of animation) is now left
        self.obj.setDirection(2)
        self.moveState[0] = self.getLeftState()
        self.moveState[1] = getSpeedState(self.moveState[0])
        self.moveChar()
        self.updateTiger()
    
    # moveRight function
    def moveRight(self):
        # move state (in terms of animation) is now left
        self.obj.setDirection(6)
        self.moveState[0] = self.getRightState()
        self.moveState[1] = getSpeedState(self.moveState[0])
        self.moveChar()
        self.updateTiger()

    # moveUp function
    def moveUp(self):
        # move state (in terms of animation) is now left
        self.obj.setDirection(4)
        self.moveState[0] = self.getUpState()
        self.moveState[1] = getSpeedState(self.moveState[0])
        self.moveChar()
        self.updateTiger()

    # moveDown function
    def moveDown(self):
        # move state (in terms of animation) is now left
        self.obj.setDirection(0)
        self.moveState[0] = self.getDownState()
        self.moveState[1] = getSpeedState(self.moveState[0])
        self.moveChar()
        self.updateTiger()

    def stopMove(self):
        #stop motion
        self.moveState[0] = -1
        self.moveState[1] = 0
        self.updateTiger()
        #self.moveState[1] = 0

    def stopLeft(self):
        if self.moveState[0] == 1:
            self.moveState[0] = 0
            self.obj.setDirection(0)
        elif self.moveState[0] == 2:
            self.stopMove()
            self.obj.setDirection(2)
        elif self.moveState[0] == 3:
            self.moveState[0] = 4
            self.obj.setDirection(4)
        self.moveState[1] = getSpeedState(self.moveState[0])
        self.updateTiger()

    def stopRight(self):
        if self.moveState[0] == 5:
            self.moveState[0] = 4
            self.obj.setDirection(4)
        elif self.moveState[0] == 6:
            self.stopMove()
            self.obj.setDirection(6)
        elif self.moveState[0] == 7:
            self.moveState[0] = 0
            self.obj.setDirection(0)
        self.moveState[1] = getSpeedState(self.moveState[0])
        self.updateTiger()

    def stopUp(self):
        if self.moveState[0] == 3:
            self.moveState[0] = 2
            self.obj.setDirection(2)
        elif self.moveState[0] == 4:
            self.stopMove()
            self.obj.setDirection(4)
        elif self.moveState[0] == 5:
            self.moveState[0] = 6
            self.obj.setDirection(6)
        self.moveState[1] = getSpeedState(self.moveState[0])
        self.updateTiger()

    def stopDown(self):
        if self.moveState[0] == 0:
            self.stopMove()
            self.obj.setDirection(0)
        elif self.moveState[0] == 1:
            self.moveState[0] = 2
            self.obj.setDirection(2)
        elif self.moveState[0] == 7:
            self.moveState[0] = 6
            self.obj.setDirection(6)
        self.moveState[1] = getSpeedState(self.moveState[0])
        self.updateTiger()

    def updateTiger(self):
        interactions.tiger_onwalk(self.obj)
        #if self.obj.animName == 'stopped' and self.moveState[1] != 0:
        #    self.obj.setAnimation('move')
        #elif self.obj.animName == 'moveshoot' and self.moveState[1] == 0:
        #    # TODO need to set this at a certain frame!
        #    # self.animation.cur_frame = self.oldanimation.last_played
        #    self.obj.setAnimationOnce('shoot')
        #elif self.obj.animName == 'move' and self.moveState[1] == 0:
        #    self.obj.setAnimation('stopped')
        #interactions.tiger_onwalk(self.obj)
        #if (self.moveState[0] != -1):
        #    self.obj.setAnimation('move')
        ##    #self.obj.setDirection(self.moveState[0])
        #else:
        #    self.obj.setAnimation('stopped')
        #    #self.obj.setDirection(operator.sub(0, (self.moveState[0])))
