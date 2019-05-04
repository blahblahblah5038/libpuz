from collections import defaultdict
from functools import reduce

class SpecialCharacters:
    ALL_SPECIALS = ' ,;:\'!."@#$%^&*()_-+=/\\`~[]{}'

# Take a word and split it into a representation as number of letters, keeping special characters in place
# For example cat=3 and isn't=3'1
class LetterCountPattern:
    def __init__(self,underlying,specials=SpecialCharacters.ALL_SPECIALS):
        self.underlying = underlying # the word used to generate this
        self.underlyingLower = underlying.lower()
        specialSet = set(specials)
        count = 0
        self.pattern = ""
        for letter in underlying:
            if letter not in specialSet:
                count = count + 1
            else:
                if(count>0):
                    self.pattern = self.pattern + str(count)
                count = 0
                self.pattern = self.pattern + letter
        if(count>0):
            self.pattern = self.pattern + str(count)

    def __hash__(self):
        return hash(self.pattern)


# store a word as a bag of letters. Gives an efficient way to compare anagram type questions
class LetterBag:

    # Generate LetterBag from override values. Only use if you're manipulating the internals deliberately. You prbobably don't want this one.
    def fromOverrides(underlyingOverride,underlyingLowerOveride,countsOverride):
        retval = LetterBag("")
        retval.underlying = underlyingOverride
        retval.underlyingLower = underlyingLowerOveride
        retval.counts = countsOverride
        return retval

    # Generate LetterBag from a string. This is the constructor you should use by default.
    def __init__(self,underlying):
        self.underlying = underlying # the word used to generate this
        self.underlyingLower = underlying.lower()
        self.counts = defaultdict(int)
        for letter in self.underlyingLower:
            count = self.counts[letter]
            count = count + 1
            self.counts[letter] = count

    def __len__(self):
        """Overrides the default implementation"""
        return sum(self.counts.values())

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, LetterBag):
            for letter in set(self.counts.keys()).union(set(other.counts.keys())):
                if self.counts[letter] != other.counts[letter]:
                    return False
            return True
        return False

    def __hash__(self):
        return hash(self.underlying)

    def contains(self, other):
        """Overrides the default implementation"""
        if isinstance(other, LetterBag):
            for letter in set(self.counts.keys()).union(set(other.counts.keys())):
                if self.counts[letter] < other.counts[letter]:
                    return False
            return True
        return False

    def add(self,other):
        """Overrides the default implementation"""
        if isinstance(other, LetterBag):
            counts = defaultdict(int)
            for letter in set(self.counts.keys()).union(set(other.counts.keys())):
                counts[letter] = self.counts[letter] + other.counts[letter]
            return LetterBag.fromOverrides(self.underlying+"+"+other.underlying,self.underlyingLower+"+"+other.underlyingLower,counts)
        raise Exception("Not a LetterBag")

    def subtract(self,other):
        """Overrides the default implementation"""
        if isinstance(other, LetterBag):
            counts = defaultdict(int)
            for letter in set(self.counts.keys()).union(set(other.counts.keys())):
                count = self.counts[letter] - other.counts[letter]
                if count < 0 :
                    raise Exception("Cannot have negative letter count, consider using contains() as a guard")
                if count > 0 :
                    counts[letter] = count
            return LetterBag.fromOverrides(self.underlying+"-"+other.underlying,self.underlyingLower+"-"+other.underlyingLower,counts)
        raise Exception("Not a LetterBag")

    def sum(bags):
        return reduce(lambda x,y:x.add(y), bags)


