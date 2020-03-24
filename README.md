# Target Case Study
Noah Wong 


## Barren Land Analysis
For the case study I choose the Barren Land Analysis. I used python and created two files, Farmland.py, which holds the program that calculates the amount of fertile land and test_Farmland.py which provides unit testing on Farmland.py. 

Farmland holds two classes that interact, BarrenLand and FertileLand. BarrenLands holds the individual fields of fields of barren land. It has has only one method generatePoints, which will generate all the points representing the individual one-by-one tracts of land in the field. FertileLand hold information about the entire 400-by-600 field and which land is fertile and which is barren. When you initialize FertileLand it starts as the entire field being fertile, but when you pass a list of BarrenLand objects through the method removeBarren it keeps track of which points or one-by-one tracts of land are fertile and which are barren. This information is held in the class attribute fertilePoints. After you have set which tracts are fertile and barren you can use seperatePlots to find the individual plots of lands that are fertile. Plots are the connected fertile lands that are seperated by Barren land to the other plots. This method holds information about the number of plots and size of plots in the numberOfPlots and the array plotsOfLand respectively. Finally the method areaOfPlots counts the area of each individual plot and returns a list of their areas.



## Running FarmLand




