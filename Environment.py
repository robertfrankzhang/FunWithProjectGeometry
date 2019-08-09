"""
Name:        Environment.py
Author:      Robert Zhang - Written at University of Pennsylvania
Contact:     robertzh@wharton.upenn.edu
Description: Defines the environment
"""

import numpy as np
import pygame, sys, time, math, random
from pygame.locals import *

class Environment:   
    
    def __init__(self,w=100,speedScalar=1):
        self.points = np.array([]) #Stores all n points as an nx4 matrix
        self.rawPointsReference = np.array([]) #Saves the index of each raw point
        self.linePointsReference = np.array([]) #Saves the first index of each line pair
        self.w = w
        self.WINDOWWIDTH = 500
        self.WINDOWHEIGHT = 500
        self.isTranslatingX = 0
        self.isTranslatingY = 0
        self.isTranslatingZ = 0
        self.isRotatingX = 0
        self.isRotatingY = 0
        self.isRotatingZ = 0
        self.speedScalar = speedScalar
        
    def createPoint(self,x,y,z):
        newPoint = np.array([x,y,z,1],dtype='float64')
        if self.points.size == 0:
            self.points = np.array([newPoint])
        else:
            self.points = np.vstack([self.points,newPoint])
        self.rawPointsReference = np.append(self.rawPointsReference,self.points.shape[0]-1)            

    def createLine(self,x1,y1,z1,x2,y2,z2):
        newPoint1 = np.array([x1,y1,z1,1],dtype='float64')
        newPoint2 = np.array([x2,y2,z2,1],dtype='float64')
        if self.points.size == 0:
            self.points = np.array([newPoint1])
        else:
            self.points = np.vstack([self.points,newPoint1])
        self.points = np.vstack([self.points,newPoint2])
        self.linePointsReference = np.append(self.linePointsReference,self.points.shape[0]-2)

    def deleteLine(self,x1,y1,z1,x2,y2,z2):
        for pointIndex in range(self.points.shape[0]-1):
            if pointIndex in self.linePointsReference:
                if self.comparePoints(np.array([x1,y1,z1]),self.points[pointIndex]) and self.comparePoints(np.array([x2,y2,z2]),self.points[pointIndex+1]):
                    self.linePointsReference -= 2*(self.linePointsReference > pointIndex) #Decrement indexes by 2 for line points with indexes greater than the deleted index
                    self.rawPointsReference -= 2*(self.rawPointsReference > pointIndex)
                    self.points = np.delete(self.points,pointIndex)
                    self.points = np.delete(self.points,pointIndex)

    def deletePoint(self,x,y,z):
       for pointIndex in range(self.points.shape[0]):
           if pointIndex in self.rawPointsReference:
               if self.comparePoints(np.array([x,y,z]),self.points[pointIndex]):
                    self.linePointsReference -= (self.linePointsReference > pointIndex) #Decrement indexes by 1 for line points with indexes greater than the deleted index
                    self.rawPointsReference -= (self.rawPointsReference > pointIndex)
                    self.points = np.delete(self.points,pointIndex)

    def createCube(self,centerX,centerY,centerZ,sideLength):
        self.createLine(centerX+sideLength/2,centerY+sideLength/2,centerZ+sideLength/2,centerX-sideLength/2,centerY+sideLength/2,centerZ+sideLength/2)
        self.createLine(centerX+sideLength/2,centerY+sideLength/2,centerZ+sideLength/2,centerX+sideLength/2,centerY-sideLength/2,centerZ+sideLength/2)
        self.createLine(centerX+sideLength/2,centerY+sideLength/2,centerZ+sideLength/2,centerX+sideLength/2,centerY+sideLength/2,centerZ-sideLength/2)
        self.createLine(centerX-sideLength/2,centerY-sideLength/2,centerZ+sideLength/2,centerX+sideLength/2,centerY-sideLength/2,centerZ+sideLength/2)
        self.createLine(centerX-sideLength/2,centerY-sideLength/2,centerZ+sideLength/2,centerX-sideLength/2,centerY+sideLength/2,centerZ+sideLength/2)
        self.createLine(centerX-sideLength/2,centerY-sideLength/2,centerZ+sideLength/2,centerX-sideLength/2,centerY-sideLength/2,centerZ-sideLength/2)
        self.createLine(centerX-sideLength/2,centerY+sideLength/2,centerZ-sideLength/2,centerX+sideLength/2,centerY+sideLength/2,centerZ-sideLength/2)
        self.createLine(centerX-sideLength/2,centerY+sideLength/2,centerZ-sideLength/2,centerX-sideLength/2,centerY-sideLength/2,centerZ-sideLength/2)
        self.createLine(centerX-sideLength/2,centerY+sideLength/2,centerZ-sideLength/2,centerX-sideLength/2,centerY+sideLength/2,centerZ+sideLength/2)
        self.createLine(centerX+sideLength/2,centerY+sideLength/2,centerZ-sideLength/2,centerX+sideLength/2,centerY-sideLength/2,centerZ-sideLength/2)
        self.createLine(centerX-sideLength/2,centerY-sideLength/2,centerZ-sideLength/2,centerX+sideLength/2,centerY-sideLength/2,centerZ-sideLength/2)
        self.createLine(centerX+sideLength/2,centerY-sideLength/2,centerZ+sideLength/2,centerX+sideLength/2,centerY-sideLength/2,centerZ-sideLength/2)


    def createRandomPath(self,startX,startY,startZ,minTraverseDistance,maxTraverseDistance,numSegments):
        for segment in range(numSegments):
            traverseX = random.randint(-50,50)
            traverseY = random.randint(-50,50)
            traverseZ = random.randint(-50,50)

            norm = math.pow(math.pow(traverseX,2)+math.pow(traverseY,2)+math.pow(traverseZ,2),0.5)
            if norm == 0:
                norm = 1
            traverseDistance = random.randint(minTraverseDistance,maxTraverseDistance)
            traverseX *= traverseDistance/norm
            traverseY *= traverseDistance/norm
            traverseZ *= traverseDistance/norm
            
            self.createLine(startX,startY,startZ,startX+traverseX,startY+traverseY,startZ+traverseZ)
            startX += traverseX
            startY += traverseY
            startZ += traverseZ
            
    def comparePoints(self,p1,p2):
        if (p1.size != p2.size):
            return False
        for index in range(p1.size):
            if p1[index] != p2[index]:
                return False
        return True

    def draw(self):
        #Handle key events
        '''
        j: move left
        l: move right
        i: move up
        k: move down
        u: move forward
        o: move backward

        a: rotate to the left
        d: rotate to the right
        w: rotate forward
        s: rotate back
        q: spin CCW
        e: spin CW
        '''
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == ord('j'):
                    self.isTranslatingX = -1
                if event.key == ord('l'):
                    self.isTranslatingX = 1
                if event.key == ord('i'):
                    self.isTranslatingY = 1
                if event.key == ord('k'):
                    self.isTranslatingY = -1
                if event.key == ord('u'):
                    self.isTranslatingZ = 1
                if event.key == ord('o'):
                    self.isTranslatingZ = -1
                    
                if event.key == ord('a'):
                    self.isRotatingY = -1
                if event.key == ord('d'):
                    self.isRotatingY = 1
                if event.key == ord('w'):
                    self.isRotatingX = 1
                if event.key == ord('s'):
                    self.isRotatingX = -1
                if event.key == ord('q'):
                    self.isRotatingZ = -1
                if event.key == ord('e'):
                    self.isRotatingZ = 1

            if event.type == KEYUP:
                if event.key == ord('j') or event.key == ord('l'):
                    self.isTranslatingX = 0
                if event.key == ord('i') or event.key == ord('k'):
                    self.isTranslatingY = 0
                if event.key == ord('u') or event.key == ord('o'):
                    self.isTranslatingZ = 0

                if event.key == ord('a') or event.key == ord('d'):
                    self.isRotatingY = 0
                if event.key == ord('w') or event.key == ord('s'):
                    self.isRotatingX = 0
                if event.key == ord('q') or event.key == ord('e'):
                    self.isRotatingZ = 0

        if self.isTranslatingX == -1:
            self.translate(1)
        elif self.isTranslatingX == 1:
            self.translate(2)
        if self.isTranslatingY == 1:
            self.translate(3)
        elif self.isTranslatingY == -1:
            self.translate(4)
        if self.isTranslatingZ == 1:
            self.translate(5)
        elif self.isTranslatingZ == -1:
            self.translate(6)

        if self.isRotatingY == -1:
            self.rotate(1)
        elif self.isRotatingY == 1:
            self.rotate(2)
        if self.isRotatingX == 1:
            self.rotate(3)
        elif self.isRotatingX == -1:
            self.rotate(4)
        if self.isRotatingZ == -1:
            self.rotate(6)
        elif self.isRotatingZ == 1:
            self.rotate(5)

        #Draw geometry onto screen
        self.windowSurface.fill((241,241,241))
        for pointIndex in range(self.points.shape[0]):
            if pointIndex in self.rawPointsReference:
                if self.points[pointIndex,2] >= self.w: #Only draw point if it is in front of viewer
                    center = self.points[pointIndex]/self.points[pointIndex,2]*self.w ##Performs projection onto view plane
                    adjustedCenter = (int(center[0]+self.WINDOWWIDTH/2),int(center[1]+self.WINDOWHEIGHT/2))
                    pygame.draw.circle(self.windowSurface,(168,0,0),adjustedCenter,3)
            if pointIndex in self.linePointsReference:
                if self.points[pointIndex,2] >= self.w and self.points[pointIndex+1,2] >= self.w: #If both points in front of viewer
                    pos1 = self.points[pointIndex]/self.points[pointIndex,2]*self.w ##Performs projection onto view plane
                    pos2 = self.points[pointIndex+1]/self.points[pointIndex+1,2]*self.w ##Performs projection onto view plane
                    adjustedPos1 = (int(pos1[0]+self.WINDOWWIDTH/2),int(pos1[1]+self.WINDOWHEIGHT/2))
                    adjustedPos2 = (int(pos2[0]+self.WINDOWWIDTH/2),int(pos2[1]+self.WINDOWHEIGHT/2))
                    pygame.draw.line(self.windowSurface,(168,0,0),adjustedPos1,adjustedPos2,1)
                elif self.points[pointIndex,2] >= self.w: #If first point in front of viewer
                    slope = np.array([self.points[pointIndex,0]-self.points[pointIndex+1,0],self.points[pointIndex,1]-self.points[pointIndex+1,1],self.points[pointIndex,2]-self.points[pointIndex+1,2]])
                    slopeNorm = math.pow(math.pow(slope[0],2)+math.pow(slope[1],2)+math.pow(slope[2],2),0.5)
                    slope *= (self.points[pointIndex,2]-self.w)/slopeNorm #Normalize Slope
                    slope = np.append(slope,1)
                    
                    pos1 = self.points[pointIndex]/self.points[pointIndex,2]*self.w ##Performs projection onto view plane
                    pos2 = self.points[pointIndex]-slope

                    adjustedPos1 = (int(pos1[0]+self.WINDOWWIDTH/2),int(pos1[1]+self.WINDOWHEIGHT/2))
                    adjustedPos2 = (int(pos2[0]+self.WINDOWWIDTH/2),int(pos2[1]+self.WINDOWHEIGHT/2))

                    pygame.draw.line(self.windowSurface,(168,0,0),adjustedPos1,adjustedPos2,1)
                elif self.points[pointIndex+1,2] >= self.w: #If second point in front of viewer
                    slope = np.array([self.points[pointIndex+1,0]-self.points[pointIndex,0],self.points[pointIndex+1,1]-self.points[pointIndex,1],self.points[pointIndex+1,2]-self.points[pointIndex,2]])
                    slopeNorm = math.pow(math.pow(slope[0],2)+math.pow(slope[1],2)+math.pow(slope[2],2),0.5)
                    slope *= (self.points[pointIndex+1,2]-self.w)/slopeNorm #Normalize Slope
                    slope = np.append(slope,1)
                    
                    pos2 = self.points[pointIndex+1]/self.points[pointIndex+1,2]*self.w ##Performs projection onto view plane
                    pos1 = self.points[pointIndex+1]-slope

                    adjustedPos1 = (int(pos1[0]+self.WINDOWWIDTH/2),int(pos1[1]+self.WINDOWHEIGHT/2))
                    adjustedPos2 = (int(pos2[0]+self.WINDOWWIDTH/2),int(pos2[1]+self.WINDOWHEIGHT/2))

                    pygame.draw.line(self.windowSurface,(168,0,0),adjustedPos1,adjustedPos2,1)
        pygame.display.update()
        self.mainClock.tick(8000)

    def translate(self,direction):
        translateBy = 10*self.speedScalar
        if direction == 1: ##Pressed left, move everything 10 to the right
            T = np.array([[1,0,0,translateBy],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
            self.points = np.transpose(np.dot(T,np.transpose(self.points)))
        if direction == 2: ##Pressed right, move everything 10 to the left
            T = np.array([[1,0,0,-translateBy],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
            self.points = np.transpose(np.dot(T,np.transpose(self.points)))
        if direction == 3: ##Pressed up, move everything 10 down
            T = np.array([[1,0,0,0],[0,1,0,translateBy],[0,0,1,0],[0,0,0,1]])
            self.points = np.transpose(np.dot(T,np.transpose(self.points)))
        if direction == 4: ##Pressed down, move everything 10 up
            T = np.array([[1,0,0,0],[0,1,0,-translateBy],[0,0,1,0],[0,0,0,1]])
            self.points = np.transpose(np.dot(T,np.transpose(self.points)))
        if direction == 5: ##Pressed forward, move everything 10 towards you
            T = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,-translateBy],[0,0,0,1]])
            self.points = np.transpose(np.dot(T,np.transpose(self.points)))
        if direction == 6: ##Pressed backward, move everything 10 away from you
            T = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,translateBy],[0,0,0,1]])
            self.points = np.transpose(np.dot(T,np.transpose(self.points)))
            
    def rotate(self,direction):
        rotateBy = 3*self.speedScalar
        degrees = rotateBy*math.pi/180
        posCos = math.cos(degrees)
        negCos = math.cos(-degrees)
        posSin = math.sin(degrees)
        negSin = math.sin(-degrees)
        if direction == 1: ##Pressed left, rotate everything around y-axis to the right
            T = np.array([[negCos,0,-negSin,0],[0,1,0,0],[negSin,0,negCos,0],[0,0,0,1]])
            self.points = np.transpose(np.dot(T,np.transpose(self.points)))
        if direction == 2: ##Pressed right, rotate everything around y-axis to the left
            T = np.array([[posCos,0,-posSin,0],[0,1,0,0],[posSin,0,posCos,0],[0,0,0,1]])
            self.points = np.transpose(np.dot(T,np.transpose(self.points)))
        if direction == 3: ##Pressed forward, rotate everything around x-axis towards you
            T = np.array([[1,0,0,0],[0,negCos,negSin,0],[0,-negSin,negCos,0],[0,0,0,1]])
            self.points = np.transpose(np.dot(T,np.transpose(self.points)))
        if direction == 4: ##Pressed backward, rotate everything around x-axis away from you
           T = np.array([[1,0,0,0],[0,posCos,posSin,0],[0,-posSin,posCos,0],[0,0,0,1]])
           self.points = np.transpose(np.dot(T,np.transpose(self.points)))
        if direction == 5: ##Pressed CCW, rotate everything around z-axis CW
            T = np.array([[negCos,negSin,0,0],[-negSin,negCos,0,0],[0,0,1,0],[0,0,0,1]])
            self.points = np.transpose(np.dot(T,np.transpose(self.points)))
        if direction == 6: ##Pressed CW, rotate everything around z-axis CCW
            T = np.array([[posCos,posSin,0,0],[-posSin,posCos,0,0],[0,0,1,0],[0,0,0,1]])
            self.points = np.transpose(np.dot(T,np.transpose(self.points)))
            

    def launch(self):
        pygame.init()
        self.mainClock = pygame.time.Clock()
        self.windowSurface = pygame.display.set_mode((self.WINDOWWIDTH, self.WINDOWHEIGHT), 0, 32)
        pygame.display.set_caption('Math 312 Final Project')
        while True:
            self.draw()
                

            


            
