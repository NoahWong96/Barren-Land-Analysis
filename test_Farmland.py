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
        #Testing invalid inputs
        with self.assertRaises(ValueError):
            BarrenLand(stringVertex = "-1 10 20 20")

        with self.assertRaises(ValueError):
            BarrenLand(stringVertex = "0 0 500 1000")

    def test_generatePoints(self):
        Grid1 = self.barren1.generatePoints()
        Grid2 = self.barren2.generatePoints()
        Grid3 = self.barren3.generatePoints()

        #checking if the correct points are the grid
        self.assertIn(self.testpoint1,Grid1)
        self.assertIn(self.testpoint2,Grid1)
        self.assertNotIn(self.testpoint3, Grid1)

        #Check if generatePoints returns the correct number
        self.assertEqual(self.barren1.area, len(Grid1))
        self.assertEqual(self.barren2.area, len(Grid2))
        self.assertEqual(self.barren3.area, len(Grid3))


class TestFertileLand(unittest.TestCase):

    def setUp(self):
        self.barren1 = BarrenLand(stringVertex = "0 292 399 307")
        self.barren2 = BarrenLand(stringVertex = "0 100 399 110")
        self.barren3 = BarrenLand(stringVertex = "192 0 207 599")

        self.testpoint1 = [0,292]
        self.testpoint2 = [0,307]
        self.testpoint3 = [20, 291]
        self.testpoint4 = [40, 400]

        self.FertileLand1 = FertileLand()
        self.FertileLand2 = FertileLand()

    def test_removeBarren(self):
        self.FertileLand1.removeBarren([self.barren1])
        self.FertileLand2.removeBarren([self.barren1, self.barren2, self.barren3])

        #testing if individual points have been coded correctly in FertilePoints
        self.assertEqual(0,self.FertileLand1.fertilePoints[self.testpoint1[0], self.testpoint1[1]])
        self.assertEqual(0,self.FertileLand1.fertilePoints[self.testpoint2[0], self.testpoint2[1]])
        self.assertEqual(1,self.FertileLand1.fertilePoints[self.testpoint3[0], self.testpoint3[1]])

        #Seeing if the totalArea matches the correct results
        self.assertEqual(233600, self.FertileLand1.totalArea)
        self.assertEqual(220032, self.FertileLand2.totalArea)

    def test_seperatePlots(self):
        self.FertileLand1.removeBarren([self.barren1])
        self.FertileLand2.removeBarren([self.barren1, self.barren2, self.barren3])

        self.FertileLand1.seperatePlots()
        self.FertileLand2.seperatePlots()

        #Testing the number of plots
        self.assertEqual(2, self.FertileLand1.number_of_Plots)
        self.assertEqual(6, self.FertileLand2.number_of_Plots)

        #Testing if points in different plots are associated with different numbers
        self.assertNotEqual(self.FertileLand1.plots_of_Land[self.testpoint3[0],self.testpoint3[1]],
                            self.FertileLand1.plots_of_Land[self.testpoint4[0],self.testpoint4[1]])











if __name__ == '__main__':
    unittest.main()
