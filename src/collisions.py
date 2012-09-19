"""This is a template Python file.
Python Version: 2.7.3
Author: Matthew McMullan

Description: This template was made using best practices from...
http://www.python.org/dev/peps/pep-0008/
http://www.python.org/dev/peps/pep-0257/

"""
#------------------------------------------------------------------------------
# Standard Library Imports ------------------------------------------

# 3'rd Party Imports ------------------------------------------------
import pygame
import interactions
# Local Application/Library Specific Imports ------------------------

#------------------------------------------------------------------------------
# Global Variables for Export ---------------------------------------

# Global Variables for use Inside the Module ------------------------

#------------------------------------------------------------------------------

class ColBox():
    def __init__(self,rect,object,frame=None):
        self.frame = frame
        self.rect = rect
        self.object = object

def collideRects(obj, other):
    return obj.contains(other) or other.contains(obj) or obj.colliderect(other)
    
def rectIntersect(A,B):
    if A.contains(B): return B.copy()
    if B.contains(A): return A.copy()
    pointsInA = list()
    pointsInB = list()
    if A.collidepoint(B.topleft): pointsInA.append(B.topleft)
    if A.collidepoint(B.topright): pointsInA.append(B.topright)
    if A.collidepoint(B.bottomleft): pointsInA.append(B.bottomleft)
    if A.collidepoint(B.bottomright): pointsInA.append(B.bottomright)
    if B.collidepoint(A.topleft): pointsInB.append(A.topleft)
    if B.collidepoint(A.topright): pointsInB.append(A.topright)
    if B.collidepoint(A.bottomleft): pointsInB.append(A.bottomleft)
    if B.collidepoint(A.bottomright): pointsInB.append(A.bottomright)
    if len(pointsInA)==1 and len(pointsInB)==1:
        a = pointsInA[0]
        b = pointsInB[0]
        left = min(a[0],b[0])
        top = min(a[1],b[1])
        width = abs(a[0]-b[0])
        height = abs(a[1]-b[1])
        return pygame.Rect(left,top,width,height)
    if len(pointsInA)>len(pointsInB):
        outer = A
        inner = B
    else:
        outer = B
        inner = A
    if inner.left>outer.left: left = inner.left
    else: left = outer.left
    if inner.right<outer.right: right = inner.right
    else: right = outer.right
    if inner.top>outer.top: top = outer.top
    else: top = inner.top
    if inner.bottom<outer.bottom: bottom = inner.bottom
    else: bottom = outer.bottom
    return pygame.Rect(left,top,right-left,bottom-top)

def getEventRect(obj):
    if obj.frame!=None:
        return obj.frame.collisionArea
    return obj.rect
def getQRect(rect):
    return pygame.Rect(rect.left,rect.top+3*rect.height/4,rect.width,rect.height/4+1)
def collideColBoxes(A,B,time):
    if collideRects(A.rect,B.rect):
        if A.object!=None and B.object!=None:
            recta = A.object.getFrame(time).drawArea.move(A.object.getPos())
            rectb = B.object.getFrame(time).drawArea.move(B.object.getPos())
            overlap = rectIntersect(recta,rectb)
            if (A.object.requiresDraw() or B.object.requiresDraw()):
                A.object.dirty = True
                B.object.dirty = True
                #A.object.dirtyRegions.append(recta)
                #B.object.dirtyRegions.append(rectb)
                A.object.dirtyRegions.append([overlap,A.object.getPos(),B.object])
                B.object.dirtyRegions.append([overlap,B.object.getPos(),A.object])
            eventRectA = getEventRect(A)
            eventRectB = getEventRect(B)
            if collideRects(eventRectA,eventRectB):
                interactions.collide(A.object,B.object)
        elif A.object==None or B.object==None:
            if A.object==None:
                real=B
                virt=A
            else:
                real=A
                virt=B
            eventRectReal = getEventRect(real)
            eventRectVirt = getEventRect(virt)
            newRect = getQRect(eventRectReal)#pygame.Rect(eventRectReal.left,eventRectReal.top+3*eventRectReal.height/4,eventRectReal.width,eventRectReal.height/4)
            if collideRects(newRect,eventRectVirt):
                interactions.collide(real.object,virt.rect)
            
def collideRegion(BB,colBoxes,time):
    quads = list()
    quads.append([pygame.Rect(BB.left,BB.top,BB.width/2,BB.height/2),list()])
    quads.append([pygame.Rect(BB.centerx,BB.top,BB.width/2,BB.height/2),list()])
    quads.append([pygame.Rect(BB.left,BB.centery,BB.width/2,BB.height/2),list()])
    quads.append([pygame.Rect(BB.centerx,BB.centery,BB.width/2,BB.height/2),list()])
    other = list()
    for box in colBoxes:
        found = False
        for quad in quads:
            if quad[0].contains(box.rect):
                found = True
                quad[1].append(box)
                break
        if not found:
            other.append(box)
    for quad in quads:
        lst = quad[1]
        if len(lst)>=8:
            collideRegion(quad[0],quad[1],time)
            continue
        for i in range(0,len(lst)-1):
            for j in range(i+1,len(lst)):
                collideColBoxes(lst[i],lst[j],time)
    for i in range(0,len(other)):
        for j in range(i+1,len(other)):
            collideColBoxes(other[i],other[j],time)
        for quad in quads:
            if not quad[0].colliderect(other[i]):
                continue
            for box in quad[1]:
                collideColBoxes(other[i],box,time)
