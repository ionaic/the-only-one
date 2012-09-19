import animatedobject, pygame, sys, operator, os, ConfigParser, game
from pygame import Rect

class AnimationState():
    def __init__(self, obj, pos=(0,0)):
        self.object = obj
        self.dir = 0
        self.startTime = 0
        self.animName = 'stopped'
        self.x = pos[0]
        self.y = pos[1]
        self.newX = pos[0]
        self.newY = pos[1]
        # dirty dirty dirty
        self.stashPos=pos

        self.deleted = False
        # functions for play once animations
        # dirty animation
        self.stash = Rect(0,0,0,0)
        self.stashFrame = None
        self.dirty = False
        self.dirtyRegions = list()
        self.old = None
        self.oldOffset = None
        # event
        self.eventStash = None

        self.invalidated = False
    def invalidate(self):
        self.invalidated = True
    def setAnimation(self,animName):
        # if you're busy, set what happens next after
        #if self.busy:
        #    self.playOnceBackToAnim = animName
        #else:
        if self.animName!=animName:
            #if self.animName == 'shoot':
            #    print "######## Cancel Shooting"
            #    print animName
            self.animName = animName
            self.startTime = 0
        #self.startTime = startTime
    def setAnimationOnce(self, animName):
        # if you're not already busy
        if self.old==None:
            self.old = self.animName
            self.setAnimation(animName)
            nframe = self.getFrameByNumber(0)
            if nframe.surface.get_rect().height!=self.stashFrame.surface.get_rect().height:
                self.oldOffset = nframe.surface.get_rect().height-self.stashFrame.surface.get_rect().height
                self.y = self.y - self.oldOffset
            
    def setDirection(self,dir):
        self.dir = dir
    def setPosVec(self, vect):
        self.x = vect[0]
        self.y = vect[1]
    def setPos(self,x,y):
        self.x = x
        self.y = y
    #def setNewPos(self,(x,y)):
    #    self.newX = x
    #    self.newY = y
    def getDirection(self):
        return self.dir
    def getX(self):
        return self.x
    def setX(self,x):
        self.x = x
    def getY(self):
        return self.y
    def setY(self,y):
        self.y = y
    def getPos(self):
        return (self.x,self.y)
    #def movePos(self):
    #    self.x = self.newX
    #    self.y = self.newY
    def getFrameByNumber(self,frameNum):
        anim = self.object.animations[self.animName].directions[self.dir]
        frame = anim.frames[frameNum]
        return frame
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
            if self.oldOffset!=None:
                self.y = self.y + self.oldOffset
                self.stashPos = (self.stashPos[0],self.stashPos[1]+ self.oldOffset)
                self.oldOffset = None
                
            return self.getFrameNumber(gameTime)
        return frame%frames
    def getFrame(self,gameTime):
        anim = self.object.animations[self.animName].directions[self.dir]
        frame = anim.frames[self.getFrameNumber(gameTime)]
        return frame
    def getFrameEvent(self,gameTime):
        frame = self.getFrame(gameTime)
        if self.eventStash != frame:
            self.eventStash = frame
            return frame.event
        return ''
        
    def getColAABB(self,time):
        framenum = self.getFrameNumber(time)
        anim = self.object.animations[self.animName].directions[self.dir]
        return anim.frames[framenum].collisionArea
    def requiresDraw(self):
        frame = self.getFrame(game.Game.universal.time.time())
        major = frame==self.stashFrame and self.stashPos==(self.x,self.y) and self.invalidated==False
        return not (major and self.dirty==False)
    def draw(self,target,time):
        if self.deleted == True: return
        frame = self.getFrame(time.time())
        major = frame==self.stashFrame and self.stashPos==(self.x,self.y) and self.invalidated==False
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
        self.invalidated = False
    def undraw(self,source,target,time):
        if self.deleted == True: return
        frame = self.getFrame(time.time())
        if frame==self.stashFrame and self.stashPos==(self.x,self.y) and self.invalidated==False:
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
    def visualDelete(self,source,target):
        self.deleted = True
        target.blit(source,self.stash.topleft,self.stash)
        for region in self.dirtyRegions:
            region[2].invalidate()
        
        

def createAnimationState(obj, pos, dir, anim):
    state = AnimationState(obj,pos)
    state.setPosVec(pos)
    state.setDirection(dir)
    state.setAnimation(anim)
    return state

def GroupAnimationState():
    def __init__(self,objGrp,pos=(0,0)):
        self.pos = pos
        self.dir = 0
        self.objects = list()
        for object in objGrp:
            self.objects.append((object[0],AnimationState(object[1],pos)))
        self.objGrp = objGrp
        self.setAnim('stopped')
    def getObjectFrameNumber(self,object,time):
        return 0
    def getObjectFrame(self,object,time):
        anim = self.objGrp.animations[self.animName].directions[self.direction]
        frame = anim.frames[self.getFrameNumber(time)]
        return frame
    def setAnim(self,animName,time):
        self.animName = animName
        self.startTime = 0
        for object in self.objects:
            object[1].setAnimation(animName)

        
