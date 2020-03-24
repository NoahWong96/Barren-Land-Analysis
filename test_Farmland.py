import unittest
from Farmland import BarrenLand
from Farmland import FertileLand

class TestBarrenLand(unittest.TestCase):

    def setUp(self):
        self.barren1 = BarrenLand(stringVertex = "0 292 399 307")
        self.barren2 = BarrenLand(stringVertex = "0 100 399 110")
        self.barren3 = BarrenLand(stringVertex = "192 0 207 599")

        self.testpoint1 = [0,292]
        self.testpoint2 = [0,307]
        self.testpoint3 = [20, 291]

    def test_init(self):
        self.barren4 = BarrenLand(lowerLeftVertex = [0, 0], upperRightVertex = [20, 20])

        #Testing invalid inputs
        with self.assertRaises(ValueError):
            BarrenLand(stringVertex = "-1 10 20 20")

        with self.assertRaises(ValueError):
            BarrenLand(stringVertex = "0 0 500 1000")

    def test_generatePoints(self):
        grid1 = self.barren1.generatePoints()
        grid2 = self.barren2.generatePoints()
        grid3 = self.barren3.generatePoints()

        #checking if the correct points are the grid
        self.assertIn(self.testpoint1,grid1)
        self.assertIn(self.testpoint2,grid1)
        self.assertNotIn(self.testpoint3, grid1)

        #Check if generatePoints returns the correct number
        self.assertEqual(self.barren1.area, len(grid1))
        self.assertEqual(self.barren2.area, len(grid2))
        self.assertEqual(self.barren3.area, len(grid3))


class TestFertileLand(unittest.TestCase):

    def setUp(self):
        self.barren1 = BarrenLand(stringVertex = "0 292 399 307")
        self.barren2 = BarrenLand(stringVertex = "0 100 399 110")
        self.barren3 = BarrenLand(stringVertex = "192 0 207 599")

        self.testpoint1 = [0,292]
        self.testpoint2 = [0,307]
        self.testpoint3 = [20, 291]
        self.testpoint4 = [40, 400]

        self.fertileLand1 = FertileLand()
        self.fertileLand2 = FertileLand()

    def test_removeBarren(self):
        self.fertileLand1.removeBarren([self.barren1])
        self.fertileLand2.removeBarren([self.barren1, self.barren2, self.barren3])

        #testing if individual points have been coded correctly in FertilePoints
        self.assertEqual(0,self.fertileLand1.fertilePoints[self.testpoint1[0], self.testpoint1[1]])
        self.assertEqual(0,self.fertileLand1.fertilePoints[self.testpoint2[0], self.testpoint2[1]])
        self.assertEqual(1,self.fertileLand1.fertilePoints[self.testpoint3[0], self.testpoint3[1]])

        #Seeing if the totalArea matches the correct results
        self.assertEqual(233600, self.fertileLand1.totalArea)
        self.assertEqual(220032, self.fertileLand2.totalArea)

    def test_seperatePlots(self):
        self.fertileLand1.removeBarren([self.barren1])
        self.fertileLand2.removeBarren([self.barren1, self.barren2, self.barren3])

        self.fertileLand1.seperatePlots()
        self.fertileLand2.seperatePlots()

        #Testing the number of plots
        self.assertEqual(2, self.fertileLand1.numberOfPlots)
        self.assertEqual(6, self.fertileLand2.numberOfPlots)

        #Testing if points in different plots are associated with different numbers
        self.assertNotEqual(self.fertileLand1.plotsOfLand[self.testpoint3[0],self.testpoint3[1]],
                            self.fertileLand1.plotsOfLand[self.testpoint4[0],self.testpoint4[1]])


    def test_areaOfPlots(self):
        self.fertileLand1.removeBarren([self.barren1])
        self.fertileLand2.removeBarren([self.barren1, self.barren2, self.barren3])

        self.fertileLand1.seperatePlots()
        self.fertileLand2.seperatePlots()

        self.area1 = self.fertileLand1.areaOfPlots()
        self.area2 = self.fertileLand2.areaOfPlots()

        #Check if numberOfPlots matches the length of area
        self.assertEqual(len(self.area1), self.fertileLand1.numberOfPlots)
        self.assertEqual(len(self.area2), self.fertileLand2.numberOfPlots)



if __name__ == '__main__':
    unittest.main()
