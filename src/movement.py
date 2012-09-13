import pygame, sys, math, operator

class Movement:
    def __init__(self, game, iofuncs):
        # movement state variable
        self.moveState = [-8, 10]
        self.game = game
        self.iofuncs = iofuncs
        self.moveSpeed = [0.2,0.2]

    def moveChar(self):
        # direction of movement [x, y]
        direction = [0,0]
        magnitude = self.moveState[1] * self.moveSpeed
        if not self.moveState[0] < 0:
            
            if self.moveState[0] == 0:
                # down (south)
                direction = [0, 1]
            elif self.moveState[0] == 1:
                # down/left (southwest)
                direction = [-1, 1]
            elif self.moveState[0] == 2:
                # left (west)
                direction = [-1, 0]
            elif self.moveState[0] == 3:
                # up/left (northwest)
                direction = [-1, -1]
            elif self.moveState[0] == 4:
                # up (north)
                direction = [0, -1]
            elif self.moveState[0] == 5:
                # up/right (northeast)
                direction = [1, -1]
            elif self.moveState[0] == 6:
                # right (east)
                direction = [1, 0]
            elif self.moveState[0] == 7:
                # down/right (southeast)
                direction = [1, 1]
                move = map(operator.mul, direction, self.moveSpeed)
                move = map(operator.add, move, self.game.tiger.getPos())
                self.game.tiger.setNewPos(move[0], move[1])
        else:
            return
        


    def updatePos(self):
        self.moveChar()
        proposedPos = self.game.tiger.getNewPos()
        if proposedPos != self.game.tiger.getPos():
            self.game.tiger.setPos(proposedPos[0], proposedPos[1])

    def getLeftState(self):
        if self.moveState[0] in (0, 1, 7):
            return 1
        elif self.moveState[0] in (3, 4, 5):
            return 3 
        elif self.moveState[0] in (-1, 2, 6):
            return 2

    def getRightState(self):
        if self.moveState[0] in (0, 1, 7):
            return 7
        elif self.moveState[0] in (-1, 2, 6):
            return 6
        elif self.moveState[0] in (3, 4, 5):
            return 5

    def getUpState(self):
        if self.moveState[0] in (-1, 0, 4):
            return 4
        elif self.moveState[0] in (1, 2, 3):
            return 3
        elif self.moveState[0] in (5, 6, 7):
            self.moveState[0] = 5

    def getDownState(self):
        if self.moveState[0] in (-1, 0, 4):
            return 0
        elif self.moveState[0] == (1, 2, 3):
            return 1
        elif self.moveState[0] in (5, 6, 7):
            return 7

    # movement functions: 0-Down, 2-Left, 4-up, 6-right
    # moveLeft function
    def moveLeft(self):
        # move state (in terms of animation) is now left
        self.moveState[1] = 10
        # self.game.tiger.setDirection(2)
        self.moveState[0] = self.getLeftState()
        self.moveChar()
        self.updateTiger()
    
    # moveRight function
    def moveRight(self):
        # move state (in terms of animation) is now left
        self.moveState[1] = 10
        # self.game.tiger.setDirection(6)
        self.moveState[0] = self.getRightState()
        self.moveChar()
        self.updateTiger()

    # moveUp function
    def moveUp(self):
        # move state (in terms of animation) is now left
        self.moveState[1] = 10
        #self.game.tiger.setDirection(2)
        self.moveState[0] = self.getUpState()
        self.moveChar()
        self.updateTiger()

    # moveDown function
    def moveDown(self):
        # move state (in terms of animation) is now left
        self.moveState[1] = 10
        #self.game.tiger.setDirection(6)
        self.moveState[0] = self.getDownState()
        self.moveChar()
        self.updateTiger()

    def stopMove(self):
        #stop motion
        self.moveState = [-8, 0]
        self.updateTiger()

    def stopLeft(self):
        if (self.moveState[0]==1):
            self.moveState[0]=0
        elif (self.movestate[0]==3):
            self.moveState[0]=4
        else:
            self.moveState[0] = -2
        self.updateTiger()

    def stopRight(self):
        if (self.moveState[0]==7):
            self.moveState[0]=0
        elif (self.movestate[0]==5):
            self.moveState[0]=4
        else:
            self.moveState[0] = -6
        self.updateTiger()

<<<<<<< HEAD
    def stopLeft():
        self.moveState[1] = 0
=======
    def stopDown(self):
        if (self.moveState[0]==1):
            self.moveState[0]=2
        elif (self.movestate[0]==7):
            self.moveState[0]=6
        else:
            self.moveState[0] = -8
        self.updateTiger()

    def stopUp(self):
        if (self.moveState[0]==3):
            self.moveState[0]=2
        elif (self.movestate[0]==5):
            self.moveState[0]=6
        else:
            self.moveState[0] = -4
        self.updateTiger()

    def updateTiger(self):
        if (self.moveState[0]>=0):
            self.game.tiger.setAnimation('move')
            self.game.tiger.setDirection(self.moveState[0])
        else:
            self.game.tiger.setAnimation('stopped')
            self.game.tiger.setDirection(0-self.moveState[0])
>>>>>>> 73a2d8effec660eed96395ed46da073beb3014ab
