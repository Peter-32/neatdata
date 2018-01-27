import unittest
import pandas as pd
import numpy as np
from neatdata.y.missingyrowdropper import *
from neatdata.y.yconverter import *
from neatdata.y.ycleaner import *


class TestYConverter(unittest.TestCase):

    def testYConverter_ConvertToNumberAndString_SetYMappingsWithStrings(self):
        # Assemble
        strings = ['a', 'a', 'a', 'a', 'b', 'c', 'd']
        numbers = [0, 0, 0, 0, 1, 2, 3]
        # Act
        yConverter = YConverter()
        yConverter.setYMappings(strings)
        test1 = yConverter.convertToNumber(strings)
        test2 = yConverter.convertToString(strings)
        test3 = yConverter.convertToNumber(numbers)
        test4 = yConverter.convertToString(numbers)
        # Assert
        for i in range(len(strings)):
            self.assertEqual(test1[i], numbers[i])
            self.assertEqual(test2[i], strings[i])
            self.assertEqual(test3[i], numbers[i])
            self.assertEqual(test4[i], strings[i])

    def testYConverter_ConvertToNumberAndString_SetYMappingsWithNumbers(self):
        # Assemble
        strings = ['a', 'a', 'a', 'a', 'b', 'c', 'd']
        numbers = [0, 0, 0, 0, 1, 2, 3]
        # Act
        yConverter = YConverter()
        yConverter.setYMappings(numbers)
        test1 = yConverter.convertToNumber(strings)
        test2 = yConverter.convertToString(strings)
        test3 = yConverter.convertToNumber(numbers)
        test4 = yConverter.convertToString(numbers)
        # Assert
        for i in range(len(strings)):
            self.assertEqual(test1[i], numbers[i])
            self.assertEqual(test2[i], strings[i])
            self.assertEqual(test3[i], numbers[i])
            self.assertEqual(test4[i], strings[i])

    def testYConverter_SetMappingWithNanValuesSkipsNanMapping(self):
        # Assemble
        now = pd.datetime.now()
        x = pd.DataFrame({'col1': [1,1,1,1,1,1,1],
                               'col2': ['a','a','a','a','a','a','a'],
                               'col3': [now,now,now,now,now,now,now]})
        y = [0, 0, 0, 0, 1, 2, np.nan]
        y = castAsNumpy(y)
        x, y = MissingYRowDropper().execute(x, y)
        yConverter = YConverter()
        # Act
        yConverter.setYMappings(y)
        # Assert
        self.assertEqual(len(yConverter._trainYMappingsStrToNum), 4)
        self.assertEqual(len(yConverter._trainYMappingsNumToStr), 4)
        self.assertTrue(0 in yConverter._trainYMappingsNumToStr)
        self.assertTrue(1 in yConverter._trainYMappingsNumToStr)
        self.assertTrue(2 in yConverter._trainYMappingsNumToStr)
        self.assertTrue(-99 in yConverter._trainYMappingsNumToStr)
        self.assertTrue("0.0" in yConverter._trainYMappingsStrToNum)
        self.assertTrue("1.0" in yConverter._trainYMappingsStrToNum)
        self.assertTrue("2.0" in yConverter._trainYMappingsStrToNum)
        self.assertTrue("NotFound" in yConverter._trainYMappingsStrToNum)

    def testYConverter_SetMappingAutoIncrementsStrings(self):
        # Assemble
        y = ["a", "b", "c", "z"]
        yConverter = YConverter()
        # Act
        yConverter.setYMappings(y)
        # Assert
        self.assertEqual(len(yConverter._trainYMappingsStrToNum), 5)
        self.assertEqual(len(yConverter._trainYMappingsNumToStr), 5)
        self.assertTrue(0 in yConverter._trainYMappingsNumToStr)
        self.assertTrue(1 in yConverter._trainYMappingsNumToStr)
        self.assertTrue(2 in yConverter._trainYMappingsNumToStr)
        self.assertTrue(3 in yConverter._trainYMappingsNumToStr)
        self.assertTrue(-99 in yConverter._trainYMappingsNumToStr)
        self.assertTrue("a" in yConverter._trainYMappingsStrToNum)
        self.assertTrue("b" in yConverter._trainYMappingsStrToNum)
        self.assertTrue("c" in yConverter._trainYMappingsStrToNum)
        self.assertTrue("z" in yConverter._trainYMappingsStrToNum)
        self.assertTrue("NotFound" in yConverter._trainYMappingsStrToNum)
