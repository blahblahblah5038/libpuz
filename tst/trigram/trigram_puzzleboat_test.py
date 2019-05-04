import unittest
from collections import deque
from src.trigram.trigram_puzzleboat import Trigram

class TestTrigramPuzzleBoat(unittest.TestCase):

    def setUp(self):
        self.results = []

    def appendResult(self,result):
        self.results.append(result)

class TestResult(TestTrigramPuzzleBoat):
    def testBasic(self):
        Trigram.solve('/usr/share/dict/words',['its','clo','bbe','rin','g'],['2\'1','10','4!'],0,self.appendResult)
        print(self.results)
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
