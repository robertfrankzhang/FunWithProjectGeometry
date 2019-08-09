"""
Name:        main.py
Author:      Robert Zhang - Written at University of Pennsylvania
Contact:     robertzh@wharton.upenn.edu
Description: Main execution file to run code. Feel free to create new points, or lines here
"""

from Environment import *
import random

environment = Environment()

'''Create new shapes here as you please: Player starts with the origin
   at the center of the screen looking into the z-axis. Demo code for
   available functionality and documentation is below
   
'''

'''Generate 500 random points within a 2000x2000x2000 space around the origin
   Draw point with "environment.createPoint(X,Y,Z)"
'''
for i in range(500):
    randX = random.randint(-1000,1000)
    randY = random.randint(-1000,1000)
    randZ = random.randint(-1000,1000)
    environment.createPoint(randX,randY,randZ)

'''Generate 500 random line segments within a 2000x2000x2000 space around the origin
   Draw line with "environment.createLine(startX,startY,startZ,endX,endY,endZ)"
'''
for i in range(500):
    randX = random.randint(-1000,1000)
    randY = random.randint(-1000,1000)
    randZ = random.randint(-1000,1000)
    randX2 = random.randint(-1000,1000)
    randY2 = random.randint(-1000,1000)
    randZ2 = random.randint(-1000,1000)
    environment.createLine(randX,randY,randZ,randX2,randY2,randZ2)

'''Generate 100 random cubes of random sizes within a 2000x2000x2000 space around the origin
   Draw cube with "environment.createCube(centerX,centerY,centerZ,sideLength)"
'''
for i in range(100):
    randX = random.randint(-1000,1000)
    randY = random.randint(-1000,1000)
    randZ = random.randint(-1000,1000)
    randSL = random.randint(30,200)
    environment.createCube(randX,randY,randZ,randSL)

'''Generate a random 3D path of length 50
   Draw path with "environment.createRandomPath(startX,startY,startZ,minimum edge distance, maximum edge distance, path length"
'''
randX = random.randint(-1000,1000)
randY = random.randint(-1000,100)
randZ = random.randint(-1000,100)
environment.createRandomPath(randX,randY,randZ,50,200,50)

environment.launch()

