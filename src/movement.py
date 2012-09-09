import pygame, sys, math, ioprocess
from pygame.locals import *

blackColor = pygame.Color(0, 0, 0)
whiteColor = pygame.Color(255, 255, 255)

pygame.init() # init pygame
fpsClock = pygame.time.Clock() # setup a clock to cap FPS
screenSize = [800, 600] # set screen size
canvas = pygame.display.set_mode(screenSize)

circPos = (100, 200)
circVel = (5, 5)
velDir = (0, 0)
#circDecc = [0, 0]

iohandler = IOfunctions()

def abs(num):
    if (num < 0):
        return (-1) * num
    else:
        return num

def clamp0(num, numMax):
    return max(min(numMax, num), 0)

#def tupRClamp(num, 

def tupClamp0(nums, numMaxes):
    return tuple(map(clamp0, nums, numMaxes))

def tupAdd(tup1, tup2):
    return tuple(map(operator.add, tup1, tup2))

def tupMult(tup1, tup2):
    return tuple(map(operator.mul, tup1, tup2))

def moveCircle():
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

def keyDownHandler():
    event = pygame.event.get()
    if event.key in (K_LEFT, K_a):
        velDir = (-1, velDir[1])
    elif event.key in (K_RIGHT, K_d):
        velDir = (1, velDir[1])
    elif event.key in (K_UP, K_w):
        velDir = (velDir[0], -1)
    elif event.key in (K_DOWN, K_s):
        velDir = (velDir[0], 1)
    elif event.key == K_ESCAPE:
        pygame.quit()
        sys.exit()

while True:
    canvas.fill(pygame.Color(255, 255, 255))

    pygame.draw.circle(canvas, pygame.Color(0, 0, 0), circPos, 30)

                #velDir = (0, velDir[1])
                #velDir = (velDir[0], 0)


    pygame.display.flip()
    fpsClock.tick(30)
