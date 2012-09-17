import animatedobject, pygame, sys, operator, os, ConfigParser
from pygame import Rect

class AnimationState():
    def __init__(self, obj):
        self.object = obj
        self.dir = 0
        self.startTime = 0
        self.animName = 'stopped'
        self.x = 0
        self.y = 0
        self.stash = Rect(0,0,0,0)
    def setAnimation(self,animName):
        self.animName = animName
        self.startTime = 0
    def setDirection(self,dir):
        self.dir = dir
    def setPosVec(self, vect):
        self.x = vect[0]
        self.y = vect[1]
    def setPos(self,x,y):
        self.x = x
        self.y = y
    def getDirection(self):
        return self.dir
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getPos(self):
        return (self.x,self.y)
    def updatePos(self):
        self.x = newX
        self.y = newY
    def getFrameNumber(self,gameTime):
        if self.startTime == 0:
            self.startTime = gameTime
        timediff = gameTime - self.startTime
        fps = self.object.animations[self.animName].fps
        frames = self.object.animations[self.animName].frames
        msf = 1000 / fps
        frame = (timediff / msf)%frames
        return int(frame)
    def getFrame(self,gameTime):
        anim = self.object.animations[self.animName].directions[self.dir]
        frame = anim.frames[self.getFrameNumber(gameTime)]
        return frame
    def getColAABB(self,time):
        framenum = self.getFrameNumber(time)
        anim = self.object.animations[self.animName].directions[self.dir]
        return anim.frames[framenum].collisionArea
    def draw(self,target,time):
        frame = self.getFrame(time.time())
        target.blit(frame.surface,self.getPos())
        self.stash = frame.drawArea.move(self.x,self.y)

def createAnimationState(obj, pos, dir, anim):
    state = AnimationState(obj)
    state.setPosVec(pos)
    state.setDirection(dir)
    state.setAnimation(anim)
    return state
