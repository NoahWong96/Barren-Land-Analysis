#This contains the two classes of BarrenLand and FertileLand

import numpy.matlib
import numpy as np

#class BarrenLand holds information about the barren land,
class BarrenLand:

    #input is the string with four integers seperated by a space
    def __init__(self, LowerLeftVertex=-1, UpperRightVertex=-1, stringVertex= '',fieldwidth = 400,fieldheight = 600):
        if stringVertex != '':
            # vertex list seperates the string into a list of 4 integers
            self.vertexList = list(map(int, stringVertex.split()))
        else :
            self.vertexList = [LowerLeftVertex[0],LowerLeftVertex[1], UpperRightVertex[0], UpperRightVertex[1]]

        if self.vertexList[0] < 0 or self.vertexList[1] < 0 or self.vertexList[2] >= fieldwidth or self.vertexList[3] >=fieldheight:
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
        Points = []

        for i in range(0, self.width):
            for j in range(0, self.height):
                Points.append( [self.lowerLeftX + i, self.lowerLeftY + j])

        return Points

    #Prints BarrenLand coordinates
    def getVertices(self):
        LowerLeftVertex = [self.lowerLeftX, self.lowerLeftY]
        UpperRightVertex = [self.upperRightX, self.upperRightY]

        print("The lower left vertex is ", LowerLeftVertex )
        print("The upper right vertex is ", UpperRightVertex)
        return


#This class is for the fertile land
class FertileLand:

    def __init__(self,fieldwidth= 400,fieldheight = 600):

        #FertilePoints tells us if each 1 by 1 square is fertile or barren
        #one represents fertile, zero represents barren
        self.fertilePoints = np.matlib.ones((fieldwidth,fieldheight))
        self.width = fieldwidth
        self.height = fieldheight
        self.totalArea = self.width * self.height #Holds the area of all fertile land

        #seperated plots of land and number, we don't initialize this until removeBarren
        self.plots_of_Land =[]  #0 if barren, >0 for the number of plot
        self.number_of_Plots = 0 #counts the number of plots

    #Prints FertilePoints
    def printLand(self):
        for i in range(self.height-1,0,-1):
            for j in range (0,self.width):
                print(self.fertilePoints[j,i], " ", end='')
            print()
        return


    #changes FertilePoints to include barren land from a list of BarrenLand objects
    def removeBarren(self, BarrenLandList):
        for BarrenLand in BarrenLandList:
            Barrenpoints = BarrenLand.generatePoints()
            for point in Barrenpoints:
                if self.fertilePoints[point[0],point[1]]==1:
                    self.fertilePoints[point[0],point[1]]=0 #zero represents barren
                    self.totalArea = self.totalArea - 1

        return

    #This should only be called after seperatePlots, it counts the area of each plot
    def Area_of_Plots(self):
        number_of_plot = list(range(0,self.number_of_Plots+1))
        areas = np.zeros(len(number_of_plot))


        #This counts the size of each plot including the size of barren land
        for i in range(0,self.height):
            for j in range (0,self.width):
                areas[int(self.plots_of_Land[j,i])] = areas[int(self.plots_of_Land[j,i])] + 1

        #Remove the barren land count
        areas = areas[1:]

        #sort the areas smallest to largest
        areas = np.sort(areas, kind ='mergesort')
        return areas


    #This initializes both Number_of_Plots and Plots_of_Land which seperate our field into
    #different plots of fertile land
    def seperatePlots(self):

        #create an array with plots of land that have been counted, this will be filled with
        #1 for the first connected fertile land, then 2 for the second connected fertile land etc.
        Alreadycounted = np.matlib.zeros((self.width, self.height))

        #Keeps track of how much land has been accounted for, When AlreadycountedArea is equal to
        #TotalArea then we can stop the arrays
        AlreadycountedArea =0

        #this holds the number of the seperated plot we have found, it starts at one and then
        #increments for each additional seperated plot of fertile land that is found
        number_of_plot =0

        while (AlreadycountedArea < self.totalArea):
            number_of_plot = number_of_plot+1

            #This will find our first fertile land point that we haven't already counted
            for i in range(0,self.height):
                for j in range (0,self.width):
                    if self.fertilePoints[j,i]==1 and Alreadycounted[j,i] == 0:
                        firstpoint = j,i
                        Alreadycounted[firstpoint[0],firstpoint[1]] = number_of_plot
                        AlreadycountedArea = AlreadycountedArea + 1
                        break #this is exit the loops
                else:
                    continue
                break

            #To find the points that are touching firstpoint, we start an iterative process
            #We explore the points touching firstpoint, if those points are fertile (FertilePoints == 1) and
            #unaccounted for (Alreadycounted == 0), then we add them to next_generation,
            #The points in next_generation then are explored in the same fashion our next step


            #this list will hold the points from the last step added as we search through this array
            last_generation =  [firstpoint]
            #this list will hold the new points we find
            next_generation = []

            while len(last_generation) != 0: #When we have counted every point last_generation will be empty
                for point in last_generation:
                    #Case 1, checking to see if South of point is fertile and unaccounted for
                    if point[1] > 0:     #check to see if the point is on the edge
                        if self.fertilePoints[point[0],point[1]-1] == 1 and Alreadycounted[point[0],point[1]-1] ==0:
                            next_generation.append([point[0],point[1]-1])
                            Alreadycounted[point[0],point[1]-1] = number_of_plot
                            AlreadycountedArea = AlreadycountedArea + 1

                    #Case 2, checking if West of point is fertile and unaccounted for
                    if point[0]>0: #check to see if the point is on the edge
                        if self.fertilePoints[point[0]-1,point[1]] == 1 and Alreadycounted[point[0]-1,point[1]] ==0:
                            next_generation.append([point[0]-1,point[1]])
                            Alreadycounted[point[0]-1,point[1]] = number_of_plot
                            AlreadycountedArea = AlreadycountedArea + 1

                    #Case 3, checking if South of point is fertileland and unaccounted for
                    if point[1] < self.height-1: #check to see if the point is on the edge
                        if self.fertilePoints[point[0],point[1]+1] == 1 and Alreadycounted[point[0],point[1]+1] ==0:
                            next_generation.append([point[0],point[1]+1])
                            Alreadycounted[point[0],point[1]+1] = number_of_plot
                            AlreadycountedArea = AlreadycountedArea + 1

                    #Case 4, checking if East of point is fertile and unaccounted for
                    if point[0] < self.width-1: #check to see if the point is on the edge
                        if self.fertilePoints[point[0]+1,point[1]] == 1 and Alreadycounted[point[0]+1,point[1]] ==0:
                            next_generation.append([point[0]+1,point[1]])
                            Alreadycounted[point[0]+1,point[1]] = number_of_plot
                            AlreadycountedArea = AlreadycountedArea + 1

                #Now we take the new points we found and set them as last_generation
                #These are points that will be explored in the next step
                last_generation = next_generation
                next_generation = []

        #initializes the class attributes
        self.number_of_Plots = number_of_plot
        self.plots_of_Land = Alreadycounted
        return

#given your list of vertices
def Calculate_Areas(vertices_list):

    BarrenLandList = []

    for vertex in vertices_list:
        BarrenLandList.append(BarrenLand(stringVertex = vertex))

    fertileLand = FertileLand()
    fertileLand.removeBarren(BarrenLandList)
    fertileLand.seperatePlots()
    return fertileLand.Area_of_Plots()

if __name__ == '__main__':
    print(Calculate_Areas(["0 292 399 307"]))
    print(Calculate_Areas(["48 192 351 207", "48 392 351 407", "120 52 135 547", "260 52 275 547"]))
    print(Calculate_Areas(["0 292 399 307", "0 100 399 110", "192 0 207 599"]))
