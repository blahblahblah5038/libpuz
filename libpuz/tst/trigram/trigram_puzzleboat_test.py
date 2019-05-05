import unittest
from collections import deque
from libpuz.trigram.trigram_puzzleboat import Trigram
import pprint
pp = pprint.PrettyPrinter(indent=4)

class TestTrigramPuzzleBoat(unittest.TestCase):

    def setUp(self):
        self.results = []

class TestResult(TestTrigramPuzzleBoat):
    def testBasic(self):
        self.results = Trigram.solve('/usr/share/dict/words',['tim','e'],['4'],0)
        pp.pprint(self.results)
        self.assertEqual(['time'],self.results[0])
    def testLessBasic(self):
        self.results = Trigram.solve('/usr/share/dict/words',['it\'s','clo','bbe','rin','g','tim','e'],['2\'1','10','4'],0)
        pp.pprint(self.results)
        self.assertEqual(['it\'s','clobbering','time'],self.results[0])

    def testPreprocessWordLengths(self):
        dirty = "1 2,3 4^ $5".split(" ")
        clean = Trigram.preprocessWordLengths(dirty)
        self.assertEqual(4,len(clean))
        self.assertEqual(deque(['1','2,3','4','5']),clean)

    def testPreprocessLetterList(self):
        dirty = ["aaa"]
        clean = list(Trigram.preprocessLetterList(dirty))
        self.assertEqual(3,clean[0].counts['a'])
