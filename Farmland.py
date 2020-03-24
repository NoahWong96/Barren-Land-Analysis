#This contains the two classes of BarrenLand and FertileLand

import numpy.matlib
import numpy as np
import sys

#class BarrenLand holds information about the barren land,
class BarrenLand:

    #input is the string with four integers seperated by a space
    def __init__(self, lowerLeftVertex=-1, upperRightVertex=-1, stringVertex= '',fieldWidth = 400,fieldHeight = 600):
        if stringVertex != '':
            # vertex list seperates the string into a list of 4 integers
            self.vertexList = list(map(int, stringVertex.split()))
        else :
            self.vertexList = lowerLeftVertex + upperRightVertex

        if self.vertexList[0] < 0 or self.vertexList[1] < 0 or self.vertexList[2] >= fieldWidth or self.vertexList[3] >=fieldHeight:
            raise ValueError("The input of the vertex is out of bounds!")

        #saves the vertex locations as attributes
        self.lowerLeftX = self.vertexList[0]
        self.lowerLeftY = self.vertexList[1]
        self.upperRightX = self.vertexList[2]
        self.upperRightY = self.vertexList[3]

        #new attributes that describe the shape of the rectangle
        self.height = 1+self.upperRightY - self.lowerLeftY
        self.width = 1+self.upperRightX- self.lowerLeftX
        self.area = self.height * self.width


    #returns the individual squares of the barren land as points
    def generatePoints(self):
        points = []

        for i in range(0, self.width):
            for j in range(0, self.height):
                points.append( [self.lowerLeftX + i, self.lowerLeftY + j])

        return points


class FertileLand:

    def __init__(self,fieldwidth= 400,fieldheight = 600):

        #fertilePoints tells us if each 1 by 1 square is fertile or barren
        #1 represents fertile, 0 represents barren
        self.fertilePoints = np.matlib.ones((fieldwidth,fieldheight))
        self.width = fieldwidth
        self.height = fieldheight
        self.totalArea = self.width * self.height #Holds the area of all fertile land

        #seperated plots of land and number, we don't initialize this until removeBarren
        self.plotsOfLand =[]  #0 if barren, >0 for the number of plot
        self.numberOfPlots = 0 #counts the number of plots

    #changes FertilePoints to include barren land from a list of BarrenLand objects
    def removeBarren(self, barrenLandList):
        for barrenLand in barrenLandList:
            barrenPoints = barrenLand.generatePoints()
            for point in barrenPoints:
                if self.fertilePoints[point[0],point[1]]==1:
                    self.fertilePoints[point[0],point[1]]=0 #zero represents barren
                    self.totalArea = self.totalArea - 1
        return

    #This initializes both numberOfPlots and plotsOfLand which seperate our field into
    #different plots of fertile land
    def seperatePlots(self):
        #create an array with plots of land that have been counted, this will be filled with
        #1 for the first connected fertile land, then 2 for the second connected fertile land etc.
        alreadyCounted = np.matlib.zeros((self.width, self.height))

        #Keeps track of how much land has been accounted for, When alreadyCountedArea is equal to
        #totalArea then we can stop the arrays
        alreadyCountedArea =0

        #this holds the number of the seperated plot we have found, it starts at one and then
        #increments for each additional seperated plot of fertile land that is found
        numberOfPlot =0

        while (alreadyCountedArea < self.totalArea):
            numberOfPlot = numberOfPlot+1

            #This will find our first fertile land point that we haven't already counted
            for i in range(0,self.height):
                for j in range (0,self.width):
                    if self.fertilePoints[j,i]==1 and alreadyCounted[j,i] == 0:
                        firstPoint = j,i
                        alreadyCounted[firstPoint[0],firstPoint[1]] = numberOfPlot
                        alreadyCountedArea = alreadyCountedArea + 1
                        break #this is exit the loops
                else:
                    continue
                break

            #To find the points that are touching firstPoint, we start an iterative process
            #We explore the points touching firstPoint, if those points are fertile (fertilePoints == 1) and
            #unaccounted for (alreadyCounted == 0), then we add them to nextGeneration,
            #The points in nextGeneration then are explored in the same fashion our next step


            #this list will hold the points from the last step added as we search through this array
            lastGeneration =  [firstPoint]
            #this list will hold the new points we find
            nextGeneration = []

            while len(lastGeneration) != 0: #When we have counted every point lastGeneration will be empty
                for point in lastGeneration:
                    #Case 1, checking to see if South of point is fertile and unaccounted for
                    if point[1] > 0:     #check to see if the point is on the edge
                        if self.fertilePoints[point[0],point[1]-1] == 1 and alreadyCounted[point[0],point[1]-1] ==0:
                            nextGeneration.append([point[0],point[1]-1])
                            alreadyCounted[point[0],point[1]-1] = numberOfPlot
                            alreadyCountedArea = alreadyCountedArea + 1

                    #Case 2, checking if West of point is fertile and unaccounted for
                    if point[0]>0: #check to see if the point is on the edge
                        if self.fertilePoints[point[0]-1,point[1]] == 1 and alreadyCounted[point[0]-1,point[1]] ==0:
                            nextGeneration.append([point[0]-1,point[1]])
                            alreadyCounted[point[0]-1,point[1]] = numberOfPlot
                            alreadyCountedArea = alreadyCountedArea + 1

                    #Case 3, checking if South of point is fertileland and unaccounted for
                    if point[1] < self.height-1: #check to see if the point is on the edge
                        if self.fertilePoints[point[0],point[1]+1] == 1 and alreadyCounted[point[0],point[1]+1] ==0:
                            nextGeneration.append([point[0],point[1]+1])
                            alreadyCounted[point[0],point[1]+1] = numberOfPlot
                            alreadyCountedArea = alreadyCountedArea + 1

                    #Case 4, checking if East of point is fertile and unaccounted for
                    if point[0] < self.width-1: #check to see if the point is on the edge
                        if self.fertilePoints[point[0]+1,point[1]] == 1 and alreadyCounted[point[0]+1,point[1]] ==0:
                            nextGeneration.append([point[0]+1,point[1]])
                            alreadyCounted[point[0]+1,point[1]] = numberOfPlot
                            alreadyCountedArea = alreadyCountedArea + 1

                #Now we take the new points we found and set them as lastGeneration
                #These are points that will be explored in the next step
                lastGeneration = nextGeneration
                nextGeneration = []

        #initializes the class attributes
        self.numberOfPlots = numberOfPlot
        self.plotsOfLand = alreadyCounted
        return

    #This should only be called after seperatePlots, it counts the area of each plot
    def areaOfPlots(self):
        numberOfPlots = list(range(0,self.numberOfPlots+1))
        areas = np.zeros(len(numberOfPlots))

        #This counts the size of each plot including the size of barren land
        for i in range(0,self.height):
            for j in range (0,self.width):
                areas[int(self.plotsOfLand[j,i])] = areas[int(self.plotsOfLand[j,i])] + 1

        #Remove the barren land count
        areas = areas[1:]

        #sort the areas smallest to largest
        areas = np.sort(areas, kind ='mergesort')
        return areas

#given your list of vertices
def calculateAreas(verticesList):

    barrenLandList = []

    for vertex in verticesList:
        barrenLandList.append(BarrenLand(stringVertex = vertex))

    fertileLand = FertileLand()
    fertileLand.removeBarren(barrenLandList)
    fertileLand.seperatePlots()
    return fertileLand.areaOfPlots()



def readIn():
    barrenVertexList = []
    while True:

        data = input("Please enter a barren land in the format 0 0 20 20. Please enter Exit when done:\n")
        if 'Exit' == data:
            break
        else:
            barrenVertexList.append(data)


    return barrenVertexList




if __name__ == '__main__':
    barrenVertexList = readIn()
    print("The area of the plots are ", calculateAreas(barrenVertexList))

    #print(calculateAreas(["0 292 399 307"]))
    #print(calculateAreas(["48 192 351 207", "48 392 351 407", "120 52 135 547", "260 52 275 547"]))
    #print(calculateAreas(["0 292 399 307", "0 100 399 110", "192 0 207 599"]))
