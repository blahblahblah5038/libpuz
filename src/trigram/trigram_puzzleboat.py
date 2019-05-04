#!/usr/bin/python3

# A solver for the puzzleboat style trigram puzzles
# see http://www.pandamagazine.com/island4/puzzles/pb4_what_a_great_place_to_start_iaaa.pdf

import argparse
from collections import defaultdict
import itertools
from collections import deque
from src.word.word_manipulations import *

def printToConsole(text):
    print(text)

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
    print("running with letterList:'"+str(letterListDirty)+"'")
    letterList = Trigram.preprocessLetterList(letterListDirty)
    wordLengthsDirty = args.wordLengths[0].split(delimiter)
    print("running with wordLengths:'"+str(wordLengthsDirty)+"'")
    wordLengths = Trigram.preprocessWordLengths(wordLengthsDirty)
    printIfLessThan = args.printIfLessThan
    Trigram.solve(dictionary,letterListDirty,letterList,wordLengths,printIfLessThan,printToConsole)

class Trigram:
    '''
    dictionaryFile = which dictionary to use? Needs one word per line
    letterBagSet = a set of word bags that correspond to the input text. Ex. ['abc','def']
    wordLengths = a deque of strings that correspond to the length of input words. Can have punctuation in the middle of a word. Ex. ['1','3\'1'] = I can't
    printIfLessThan = Print any failed solution with less than N characters remaining
    emitResult = a function that we'll call to send a result string. Must take a single string as an argument
    '''
    def solve(dictionaryFile,letterBagSet,wordLengths,printIfLessThan,emit):
        dictionary = defaultdict(list)
        with open(dictionaryFile,"r") as f:
            for row in f:
                patternBag = LetterPatternBag(row)
                dictionary[patternBag.pattern.pattern].append(patternBag)

        #A basic optimization to filter out words that shouldn't be recursed on
        Trigram.solveInternal([],dictionary,"",LetterBag(""),letterBagSet,wordLengths,printIfLessThan,emit)


    '''
    recursively backtrack through solutions
    
    result = the list of words we've built up
    dictionaryFile = A defaultdict that maps from a pattern like "3'1" to a list of all LetterPatternBags that match such as [LetternPatternBag("isn't"),LetterPaternBag("can't")]
    remainderRaw = the characters remaining from the next trigram
    remainderBag = the bag corresponding to remainderRaw 
    letterBagSet = a set of word bags that correspond to the input text. Ex. [LetterBag('abc'),LetterBag('def')]
    wordLengths = a deque of strings that correspond to the length of input words. Can have punctuation in the middle of a word. Ex. ['1','3\'1'] = I can't
    printIfLessThan = Print any failed solution with less than N characters remaining
    emitResult = a function that we'll call to send a result string. Must take a single string as an argument
    '''
    def solveInternal(result, dictionary,remainderRaw,remainderBag,letterBagSet,wordLengths,printIfLessThan,emit):
        if len(letterBagSet) == 0:
            return

        wordLengthsCopy = wordLengths.copy() # perform operations on a copy so backtracking works
        targetWord = wordLengthsCopy.pop()
        dictionarySubset = dictionary[targetWord]

        # if we have a remainder filter down by things that start with it
        if len(remainderRaw)>0:
            dictionarySubset = filter(lambda bag:bag.underlying.startswith(remainderRaw),dictionarySubset)

        if len(dictionarySubset) == 0:
            return

        nextRemainder,nextLetterBagSet,nextWord = Trigram.permuteBags(remainderRaw,remainderBag,letterBagSet,targetWord,dictionarySubset)

        resultCopy = result.copy()
        resultCopy.append(nextWord)
        if len(letterBagSet)<printIfLessThan:
            emit(resultCopy)

        Trigram.solveInternal(result,dictionary,nextRemainder,LetterBag(nextRemainder),wordLengths,printIfLessThan,emit)

    def permuteBags(remainderRaw,remainderBag,letterBagSet,targetWord,dictionarySubset):
        for combo in itertools.permutations(letterBagSet, 4):
            comboLetters = LetterBag.sum(combo).add(remainderBag)
            if comboLetters.contains(targetWord):
                constructed = remainderRaw
                bagsUsed = []
                for bag in combo:
                    bagsUsed.append(bag)
                    constructed = word + bag.underlying
                    for word in dictionarySubset:
                        if word == constructed:
                            letterBagSet = letterBagSet.difference(set(bagsUsed))
                            return "",letterBagSet,word
                        if constructed.startswith(word):
                            letterBagSet = letterBagSet.difference(set(bagsUsed))
                            return constructed.replace(word, "", 1),letterBagSet,word


    def preprocessWordLengths(wordLengths):
        result = deque()
        for wordLength in wordLengths:
            result.append(wordLength.strip(SpecialCharacters.ALL_SPECIALS))
        return result

    def preprocessLetterList(letterList):
        result = set()
        for letters in letterList:
            result.add(LetterBag(letters))
        return result

class LetterPatternBag:
    def __init__(self,underlying):
        self.pattern = LetterCountPattern(underlying)
        self.bag = LetterBag(underlying)

if __name__ == "__main__":
    main()
