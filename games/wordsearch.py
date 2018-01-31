#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Starting with
#   https://codereview.stackexchange.com/questions/98247/wordsearch-generator
import itertools

# For handling regex of characters
import regex
from copy import deepcopy
from random import randint

# Set up fill letters, including those with diacritics.
# Should we done something with statistics?
# Check for bad words?
letters = "qwertyuiopasdfghjklzxcvbnm"

# TODO: add diagonals, too.
# TODO: add reversal of letters

def makeGrid(words, size=[10,10], attempts=10):
    '''Run attemptGrid trying attempts number of times.

    Size contains the height and width of the board.
    Word is a list of words it should contain.'''

    for _ in range(attempts):
        try:
            return attemptGrid(words, size)
        except RuntimeError as e:
            pass
    else:
        print "ERROR - Couldn't create valid board"
        raise e

def attemptGrid(words, size):
    '''Attempt a grid of letters to be a wordsearch

    Size contains the height and width of the board.
    Word is a list of words it should contain.
    Returns the 2D list grid and a dictionary of the words as keys and
    lists of their co-ordinates as values.'''

    #Make sure that the board is bigger than even the biggest word
    sizeCap = (size[0] if size[0] >= size[1] else size[1])
    sizeCap -= 1
    if any(len(word) > sizeCap for word in words):
        print "ERROR: Too small a grid for supplied words."
        return

    grid = [[' ' for _ in range(size[0])] for __ in range(size[1])]

    #Insert answers and store their locations
    answers = {}
    for word in words:
        grid, answer = insertWord(word,grid)
        answers[word] = answer

    #Add other characters to fill the empty space
    for i,j in itertools.product(range(size[1]),range(size[0])):
        if grid[i][j] == ' ':
            grid[i][j] = letters[randint(0,len(letters)-1)]

    return grid, answers

def insertWord(word, grid, invalid=None):
    '''Insert a word into the letter grid

    'word' will be inserted into the 2D list grid.
    invalid is either None or a list of coordinates
    These coordinates are denote starting points that don't work.
    Returns an updated grid as well as a list of the added word's indices.'''

    height, width = len(grid), len(grid[0])
    # TODO: Use the number of combined characters, not just length.
    tokens = getTokens(word)
    print tokens
    length = len(tokens)

    #Detect whether the word can fit horizontally or vertically.
    hori = width >= length + 1
    vert = height >= length + 1
    if hori and vert:
        #If both can be true, flip a coin to decide which it will be
        hori = bool(randint(0,1))
        vert = not hori
    # Try diagonal, too!

    line = [] #For storing the letters' locations
    if invalid is None:
        invalid = [[None,None,True],[None,None,False]]

    #Height * width is an approximation of how many attempts we need
    for _ in range(height*width):
        if hori:
            x = randint(0,width-1-length)
            y = randint(0,height-1)
        else:
            x = randint(0,width-1)
            y = randint(0,height-1-length)
        if [y,x,hori] not in invalid:
            break
    else:
        # Probably painted into a corner, raise an error to retry.
        raise(RuntimeError)

    start = [y, x, hori] #Saved in case of invalid placement
    #Now attempt to insert each letter
    for letter in tokens:
        if grid[y][x] in (' ', letter):  # Check if it's the letter or a blank.
            line.append([y,x])
            if hori:
                x += 1
            else:
                y += 1
            # And handle diagonal, too!
        else:
            #We found a place the word can't fit
            #Mark the starting point as invalid
            invalid.append(start)
            return insertWord(word, grid, invalid)

    # If it didn't work, try the reversed word.

    #Since it's a valid place, write to the grid and return
    for i,cell in enumerate(line):
        grid[cell[0]][cell[1]] = word[i]
    return grid, line

def tryPlacingWord(tokens, grid):
    for letter in tokens:
        if grid[y][x] in (' ', letter):  # Check if it's the letter or a blank.
            line.append([y, x])
            if hori:
                x += 1
            else:
                y += 1
                # And handle diagonal, too!
        else:
            # We found a place the word can't fit
            # Mark the starting point as invalid
            invalid.append(start)
            return insertWord(word, grid, invalid)

def getTokens(word):
    '''Get the tokens, not code points.'''
    # TODO: make this smarter utf-16 and diacritics.
    vals = list(word)
    retval = []
    index = 0
    while index < len(vals):
        if ord(vals[index]) >= 0xd800 and ord(vals[index]) <+ 0xdbff:

            retval.append((vals[index] + vals[index+1]))
            index += 2
        else:
            retval.append(vals[index])
            index += 1
    return retval


def printGrid(grid):
    '''Print the grid in a friendly format.'''

    width = len(grid[0])
    print ("+" + ('---+' * width))

    for i,line in enumerate(grid):
        #for item in line:
        #    print item.decode('utf-8')
        print ("| " + " | ".join(line) + " |")
        print ("+" + ('---+' * width))


def printAnswers(answers):
    for answer in answers:
        #print(' %s: %s' % answer, answers[answer])
        print answer, answers[answer]

# The Osage works, with diacritics
osageWords = [u'𐓏𐒻𐒷𐒻𐒷', u'𐓀𐒰𐓓𐒻͘', u'𐓏𐒰𐓓𐒰𐓓𐒷', u'𐒻𐒷𐓏𐒻͘ ', u'𐓈𐒻𐓍𐒷', u'𐒹𐓂𐓏𐒷͘𐒼𐒻', u'𐓇𐓈𐓂͘𐓄𐒰𐓄𐒷',
              u'𐒰̄𐓍𐓣𐓟𐓸𐓟̄𐓛𐓣̄𐓬']

# Test splitting of Osage.
def testOsageSplit():
    for word in osageWords:
        print('Word = %s' % word)
        print('  split = %s' % list(word))
        #print("\n".join(regex.findall(r'\X', word, regex.U)))


words = ["python", "itertools", "wordsearch","code","review","functions",
         "dimensional", "dictionary", "lacklustre", 'google', 'unicode', 'horizontal',
         'vertical', 'diagonal', u'𐓏𐒻𐒷𐒻𐒷']

grid, answers = makeGrid(words, [14,14])
printGrid(grid)
printAnswers(answers)
testOsageSplit()
