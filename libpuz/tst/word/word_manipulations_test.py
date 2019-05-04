import unittest
from libpuz.word.word_manipulations import *

class TestLetterCountPattern(unittest.TestCase):
    def testLetterCountPatternBasic(self):
        cat = LetterCountPattern("Cat")
        self.assertEqual("Cat",cat.underlying)
        self.assertEqual("cat", cat.underlyingLower)
        self.assertEqual("3", cat.pattern)

    def testLetterCountPatternSpecial(self):
        catDogFish = LetterCountPattern("Cat'Dog:Fish#")
        self.assertEqual("Cat'Dog:Fish#",catDogFish.underlying)
        self.assertEqual("cat'dog:fish#",catDogFish.underlyingLower)
        self.assertEqual("3'3:4#", catDogFish.pattern)

class TestLetterBag(unittest.TestCase):
    def testLetterBagBasicCat(self):
        cat = LetterBag("Cat")
        self.assertEqual(3,len(cat))
        self.assertEqual("Cat",cat.underlying)
        self.assertEqual("cat", cat.underlyingLower)
        self.assertEqual(1, cat.counts.get('a'))
        self.assertEqual(1,cat.counts.get('c'))
        self.assertEqual(1, cat.counts.get('t'))

    def testLetterBagBasicRacecar(self):
        racecar = LetterBag("Racecar")
        self.assertEqual(7, len(racecar))
        self.assertEqual("Racecar", racecar.underlying)
        self.assertEqual("racecar", racecar.underlyingLower)
        self.assertEqual(2, racecar.counts.get('a'))
        self.assertEqual(2, racecar.counts.get('c'))
        self.assertEqual(1, racecar.counts.get('e'))
        self.assertEqual(2, racecar.counts.get('r'))

    def testLetterBagEqual(self):
        funeral = LetterBag("funeral")
        realFun = LetterBag("realfun")
        self.assertEqual(funeral,realFun)

    def testLetterBagNotEqual(self):
        funeral = LetterBag("funerals")
        realFun = LetterBag("realfun")
        self.assertNotEqual(funeral,realFun)

    def testLetterBagContains(self):
        funeral = LetterBag("funeral")
        funerals = LetterBag("funerals")
        self.assertTrue(funerals.contains(funeral))

    def testLetterBagContainsExact(self):
        funeral = LetterBag("funeral")
        realFun = LetterBag("realfun")
        self.assertTrue(funeral.contains(funeral))
        self.assertTrue(realFun.contains(realFun))
        self.assertTrue(funeral.contains(realFun))
        self.assertTrue(realFun.contains(funeral))

    def testLetterBagNotContains(self):
        funeral = LetterBag("funeral")
        funerals = LetterBag("funerals")
        self.assertFalse(funeral.contains(funerals))

    def testSubtract(self):
        funeral = LetterBag("funeral")
        real = LetterBag("real")
        fun = LetterBag("fun")
        self.assertEquals(fun,funeral.subtract(real))
        self.assertEquals(real,funeral.subtract(fun))
        self.assertTrue(funeral.subtract(real).contains(fun))
        self.assertTrue(funeral.subtract(fun).contains(real))

    def testAdd(self):
        funeral = LetterBag("funeral")
        real = LetterBag("real")
        fun = LetterBag("fun")
        self.assertFalse(fun.contains(funeral))
        self.assertFalse(real.contains(funeral))
        self.assertTrue(fun.add(real).contains(funeral))
        self.assertTrue(funeral.contains(fun.add(real)))

    def testSum(self):
        funeral = LetterBag("funeral")
        real = LetterBag("real")
        fun = LetterBag("fun")
        self.assertTrue(funeral.contains(LetterBag.sum([fun,real])))
