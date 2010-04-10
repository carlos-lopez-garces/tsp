from math import *

class UnitCircle:
    def __init__(self):
        self.radius = 1
        self.center = [0,0]

    def getRadius(self):
        return self.radius

    def getCenter(self):
        return self.center

    def getYGivenX(self, x):
        return sqrt(pow(self.radius, 2) - pow(x, 2))

    def calculatePerimeter(self):
        return pi*2*self.radius

class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def setX(self, x):
        self.x = x
            
    def getX(self):
        return self.x
    
    def setY(self, y):
        self.y = y

    def getY(self):
        return self.y

    def getDistanceTo(self, p):
        return sqrt(pow(self.getX() - p.getX(), 2) + pow(self.getY() - p.getY(), 2))       

    def getTextRep(self):
        return "("+str(self.getX())+","+str(self.getY())+")"
