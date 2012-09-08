import pygame, sys, math, ioprocess
from pygame.locals import *

class Game:
    blackColor = pygame.Color(0, 0, 0)
    whiteColor = pygame.Color(255, 255, 255)

    def __init__(self):
        self.super()
        pygame.init() # init pygame
        fpsClock = pygame.time.Clock() # setup a clock to cap FPS
        self.screenSize = [800, 600] # set screen size
        canvas = pygame.display.set_mode(screenSize)

    def gameLoop :
        while True:
            canvas.fill(pygame.Color(255, 255, 255))

            pygame.draw.circle(canvas, pygame.Color(0, 0, 0), circPos, 30)

                        #velDir = (0, velDir[1])
                        #velDir = (velDir[0], 0)

            if circVel != (0, 0):
                circPos = tupClamp0(tupAdd(tupMult(velDir, circVel), circPos), screenSize)
                circVel = (circVel[0] + circAccel[0], circVel[1] + circAccel[1])
            elif circVel[0] == 0
                if circAccel[0] != 0:
                    circAccel[0] = 0;
            elif circVel[1] == 0
                    circAccel[1] = 0;
            else:
                if circAccel != [0, 0]:
                    circAccel = [0, 0]:

            pygame.display.flip()
            fpsClock.tick(30)
