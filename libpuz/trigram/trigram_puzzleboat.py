#!/usr/bin/python3

# A solver for the puzzleboat style trigram puzzles
# see http://www.pandamagazine.com/island4/puzzles/pb4_what_a_great_place_to_start_iaaa.pdf

import argparse
from collections import defaultdict
import itertools
from collections import deque
from libpuz.word.word_manipulations import *
import pprint
pp = pprint.PrettyPrinter(indent=4)


def main():
    parser = argparse.ArgumentParser(description='A solver for trigrams in the style of http://www.pandamagazine.com/island4/puzzles/pb4_what_a_great_place_to_start_iaaa.pdf')
    parser.add_argument('--delimiter', default=',',metavar='d', type=str, nargs='?', help='The delimiter to use, default ","')
    parser.add_argument('--dictionary', default='/usr/share/dict/words',metavar='dict', type=str, nargs='?', help='Dictionary file to use, default is /usr/share/dict/words')
    parser.add_argument('--letterList', metavar='abc,def', type=str, nargs=1, help='The list of letters (typically in triples) separated by delimiter. Ex: abc,def,ghi')
    parser.add_argument('--wordLengths', metavar='1,2,3', type=str, nargs=1, help='The list of numbers separated by delimiter. *=proper noun. punctuation is left in. Ex: 2\'1,10,____!=It\'s clobbering ____!')
    parser.add_argument('--printIfLessThan', metavar='123', type=int, nargs='?', default='10', help='Print any failed solution with less than N characters remaining (to handle non-dict words) Default:10')

    args = parser.parse_args()

    delimiter = args.delimiter
    print("running with delimiter:'"+delimiter+"'")
    dictionary = args.dictionary
    print("running with dictionary:'"+dictionary+"'")
    letterListDirty = args.letterList[0].split(delimiter)
    letterList = Trigram.preprocessLetterList(letterListDirty)
    print("running with letterList:'"+str(letterList)+"'")
    wordLengthsDirty = args.wordLengths[0].split(delimiter)
    wordLengths = Trigram.preprocessWordLengths(wordLengthsDirty)
    print("running with wordLengths:'"+str(wordLengths)+"'")
    printIfLessThan = args.printIfLessThan
    #TODO pretty print result better
    result=Trigram.solve(dictionary,letterList,wordLengths,printIfLessThan)
    pp.pprint(result)


class Trigram:
    '''
    dictionaryFile = which dictionary to use? Needs one word per line
    letterBagSet = a set of word bags that correspond to the input text. Ex. ['abc','def']
    wordLengths = a deque of strings that correspond to the length of input words. Can have punctuation in the middle of a word. Ex. ['1','3\'1'] = I can't
    printIfLessThan = Print any failed solution with less than N characters remaining
    emitResult = a function that we'll call to send a result string. Must take a single string as an argument
    '''
    def solve(dictionaryFile,letterBagSet,wordLengths,printIfLessThan):
        dictionary = defaultdict(list)
        with open(dictionaryFile,"r") as f:
            for row in f:
                patternBag = LetterPatternBag(row.strip())
                dictionary[patternBag.pattern.pattern].append(patternBag)

        return Trigram.solveInternal([],dictionary,letterBagSet,wordLengths,printIfLessThan,True)


    '''
    recursively backtrack through solutions
    
    result = the list of words we've built up
    dictionaryFile = A defaultdict that maps from a pattern like "3'1" to a list of all LetterPatternBags that match such as [LetternPatternBag("isn't"),LetterPaternBag("can't")]
    remainderRaw = the characters remaining from the next trigram
    remainderBag = the bag corresponding to remainderRaw 
    letterBagSet = a set of word bags that correspond to the input text. Ex. [LetterBag('abc'),LetterBag('def')]
    wordLengths = a deque of strings that correspond to the length of input words. Can have punctuation in the middle of a word. Ex. ['1','3\'1'] = I can't
    printIfLessThan = Print any failed solution with less than N characters remaining
    '''
    def solveInternal(result, dictionary,letterBagSet,wordLengths,printIfLessThan,top):
        if len(letterBagSet) == 0:
            return []

        wordLengthsCopy = wordLengths.copy() # perform operations on a copy so backtracking works
        targetWord = wordLengthsCopy.pop()
        dictionarySubset = dictionary[targetWord]

        if len(dictionarySubset) == 0:
            return []

        #TODO handle quote only for now..
        rightLength=sum(int(x) for x in targetWord.split("'"))+len(targetWord.split("'"))-1
        #Find subsets of the letterbagset that are the right length
        sets = Trigram.findSets(letterBagSet,rightLength)
        #Grab the dictionary set
        possibleDictonary = {x.bag.underlyingLower for x in dictionarySubset}

        #We need integer lengths to check word length if we are the top
        if top:
            wordLengthsInt=[sum(int(x) for x in targetWord.split("'"))+len(targetWord.split("'"))-1 for targetWord in wordLengths]

        for s in sets:
            #Find possible orderings of the subsets
            possible = {"".join(x) for x in itertools.permutations(s,len(s))}
            #Get the intersection of the set
            targetsInDict=possible.intersection(possibleDictonary)
            lbs=letterBagSet.copy()
            #Remove used letter bags
            for x in s:
                lbs.remove(x)
            #Call self with reduced options
            nextresult = Trigram.solveInternal([],dictionary,lbs,wordLengthsCopy,printIfLessThan,False)
            if top:
                #TODO This is probably not where we should filter results
                topResult = [nextresult+list(targetsInDict)]
                #Make sure we actually filter down to just matching word lengths
                if all(map(lambda l, s: len(s)==l,wordLengthsInt,topResult[0] )) and len(wordLengthsInt) == len(topResult[0]):
                    result.extend(topResult)
            else:
                result.extend(nextresult+list(targetsInDict))

        return result       
    
    #Finds sets of the correct length
    def findSets(lbSet,length:int):
        result = [[]]
        for lb in lbSet:
            result.extend([x + [lb] for x in result if len("".join(x+[lb])) <= length])
        return list(filter(lambda x: len("".join(x))==length,result))

    def preprocessWordLengths(wordLengths):
        result = deque()
        for wordLength in wordLengths:
            result.append(wordLength.strip(SpecialCharacters.ALL_SPECIALS))
        return result

    def preprocessLetterList(letterList):
        result = set()
        for letters in letterList:
            result.add(letters.lower())
            #result.add(LetterBag(letters))
        return result

class LetterPatternBag:
    def __init__(self,underlying):
        self.pattern = LetterCountPattern(underlying)
        self.bag = LetterBag(underlying)

if __name__ == "__main__":
    main()
