import pygame, sys, math, operator

class Movement:
    def __init__(self, game, iofuncs):
        # movement state variable
        self.moveState = [-1, 10]
        self.game = game
        self.iofuncs = iofuncs
        self.moveSpeed = [0.2,0.2]

    def moveChar(self):
        # direction of movement [x, y]
        direction = [0,0]
        magnitude = self.moveState[1] * self.moveSpeed
        if not self.moveState[0] == -1:
            
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
        else:
            return
        
        move = map(operator.mul, direction, self.moveSpeed)
        move = map(operator.add, move, self.game.tiger.getPos())
        self.game.tiger.setNewPos(move[0], move[1])

    def updatePos(self):
        self.moveChar()
        proposedPos = self.game.tiger.getNewPos()
        if proposedPos != self.game.tiger.getPos():
            self.game.tiger.setPos(proposedPos[0], proposedPos[1])

    # movement functions: 0-Down, 2-Left, 4-up, 6-right
    # moveLeft function
    def moveLeft(self):
        # move state (in terms of animation) is now left
        self.moveState[1] = 10
        self.game.tiger.setDirection(2)
        if self.moveState[0] in (0, 1, 7):
            self.moveState[0] = 1
        elif self.moveState[0] in (3, 4, 5):
            self.moveState[0] = 3 
        elif self.moveState[0] in (-1, 2, 6):
            self.moveState[0] = 2
        
        self.moveChar()
    
    # moveRight function
    def moveRight(self):
        # move state (in terms of animation) is now left
        self.moveState[1] = 10
        self.game.tiger.setDirection(6)
        if self.moveState[0] in (0, 1, 7):
            self.moveState[0] = 7
        elif self.moveState[0] in (-1, 2, 6):
            self.moveState[0] = 6
        elif self.moveState[0] in (3, 4, 5):
            self.moveState[0] = 5

        self.moveChar()

    # moveUp function
    def moveUp(self):
        # move state (in terms of animation) is now left
        self.moveState[1] = 10
        self.game.tiger.setDirection(2)
        if self.moveState[0] in (-1, 0, 4):
            self.moveState[0] = 4
        elif self.moveState[0] in (1, 2, 3):
            self.moveState[0] == 3
        elif self.moveState[0] in (5, 6, 7):
            self.moveState[0] = 5

        self.moveChar()

    # moveDown function
    def moveDown(self):
        # move state (in terms of animation) is now left
        self.moveState[1] = 10
        self.game.tiger.setDirection(6)
        if self.moveState[0] in (-1, 0, 4):
            self.moveState[0] = 0
        elif self.moveState[0] == (1, 2, 3):
            self.moveState[0] = 1
        elif self.moveState[0] in (5, 6, 7):
            self.moveState[0] = 7
        self.moveChar()

    def stopMove(self):
        #stop motion
        self.moveState = [-1, 0]
