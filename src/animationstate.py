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
        self.newX = 0
        self.newY = 0
        # dirty dirty dirty
        self.stash = Rect(0,0,0,0)
        self.stashFrame = None
        self.stashPos = (-666,-666)
        self.dirty = False
        self.dirtyRegions = list()
        # functions for play once animations
        self.old = None
    def setAnimation(self,animName):
        # if you're busy, set what happens next after
        #if self.busy:
        #    self.playOnceBackToAnim = animName
        #else:
        if self.animName!=animName:
            self.animName = animName
            self.startTime = 0
        #self.startTime = startTime
    def setAnimationOnce(self, animName):
        # if you're not already busy
        if self.old==None:
            self.old = self.animName
            self.setAnimation(animName)
    def setDirection(self,dir):
        self.dir = dir
    def setPosVec(self, vect):
        self.x = vect[0]
        self.y = vect[1]
    def setPos(self,x,y):
        self.x = x
        self.y = y
    def setNewPos(self,(x,y)):
        self.newX = x
        self.newY = y
    def getDirection(self):
        return self.dir
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getPos(self):
        return (self.x,self.y)
    def movePos(self):
        self.x = self.newX
        self.y = self.newY
    def getFrameNumber(self,gameTime):
        if self.startTime == 0:
            self.startTime = gameTime
        timediff = gameTime - self.startTime
        fps = self.object.animations[self.animName].fps
        frames = self.object.animations[self.animName].frames
        msf = 1000 / fps
        frame = int((timediff / msf))
        if self.old!=None and frame>frames:
            self.setAnimation(self.old)
            self.old = None
            return self.getFrameNumber(gameTime)
        return frame%frames
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
        major = frame==self.stashFrame and self.stashPos==(self.x,self.y)
        if major and self.dirty==False:
            return
        self.stash = frame.drawArea.move(self.x,self.y)
        self.stashFrame = frame
        self.stashPos = (self.x,self.y)
        if major:
            for region in self.dirtyRegions:
                target.blit(frame.surface,region[0],region[0].move(-region[1][0],-region[1][1]))
        else:
            target.blit(frame.surface,self.stash,frame.drawArea)
        self.dirty = False
        self.dirtyRegions = list()
    def undraw(self,source,target,time):
        frame = self.getFrame(time.time())
        if frame==self.stashFrame and self.stashPos==(self.x,self.y):
            if self.dirty==False:
                return
            else:
                for region in self.dirtyRegions:
                    target.blit(source,region[0],region[0])
                return
        target.blit(source,self.stash.topleft,self.stash)
        if self.dirty:
            for region in self.dirtyRegions:
                for yolo in region[2].dirtyRegions:
                    if yolo[2]==self:
                        yolo[0] = self.stash.union(yolo[0])
        #if frame!=self.stashFrame or self.stashPos!=(self.x,self.y) or self.dirty!=False:
        #    target.blit(source,self.stash.topleft,self.stash)

def createAnimationState(obj, pos, dir, anim):
    state = AnimationState(obj)
    state.setPosVec(pos)
    state.setDirection(dir)
    state.setAnimation(anim)
    return state
