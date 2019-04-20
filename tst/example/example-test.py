# An example libpuz test
# TODO delete after a real libpuz class with test exists

import unittest
from src.example import example

class TestExample(unittest.TestCase):
    def setUp(self):
        self.example = example.Example()


class TestAddition(TestExample):
    def test_1_plus_1(self):
        result = self.example.plus(1,1)
        self.assertEqual(result,2)

    def test_2_plus_3(self):
        result = self.example.plus(2,3)
        self.assertEqual(result,5)

class TestMultiplication(TestExample):
    def test_2_times_2(self):
        result = self.example.multiply(2,2)
        self.assertEqual(result, 4)

    def test_2_times_2(self):
        result = self.example.multiply(3, 2)
        self.assertEqual(result, 6)