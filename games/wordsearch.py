#/usr/bin/env python
# -*- coding: utf-8 -*-

# Starting with
#   https://codereview.stackexchange.com/questions/98247/wordsearch-generator
import itertools

from copy import deepcopy
from random import randint

# Set up fill letters, including those with diacritics.
# Should we done something with statistics?
# Check for bad words?

# These are upper case only.
adlam_upper_letters = u'𞤀𞤁𞤂𞤃𞤄𞤅𞤆𞤇𞤈𞤉𞤊𞤋𞤌𞤍𞤎𞤏𞤐𞤑𞤒𞤓𞤔𞤕𞤖𞤗𞤘𞤙𞤚𞤛𞤜𞤝𞤞𞤟𞤠𞤡𞤢𞤣'

letters = u'𐒰𐒱𐒲𐒳𐒴𐒵𐒶𐒷𐒸𐒹𐒺𐒻𐒼𐒽𐒾𐒿𐓀𐓁𐓂𐓃𐓄𐓅𐓆𐓇𐓈𐓉𐓊𐓋𐓌𐓍𐓎𐓏𐓐𐓑𐓒𐓓'
# letters = "qwertyuiopasdfghjklzxcvbnm"

# TODO: Fix this to be better
#letters = adlam_upper_letters


debug = False

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

    # Convert all the words to tokens first.
    tokenList = [getTokens(x) for x in words]
    tokens = ''
    if debug:
      for tokens in tokenList:
        print 'Tokens: %s' % tokens

    #Make sure that the board is bigger than even the biggest set of tokens
    sizeCap = (size[0] if size[0] >= size[1] else size[1])
    sizeCap -= 1
    if any(len(tokens) > sizeCap for tokens in tokenList):
        print "ERROR: Too small a grid for supplied words: %s" % tokens
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

    reverse_it = bool(randint(0,1))
    print 'Reverse_it = %s' % reverse_it

    start = [y, x, hori] #Saved in case of invalid placement
    #Now attempt to insert each letter
    for letter in tokens:
        if grid[y][x] in (' ', letter):  # Check if it's the letter or a blank.
            if grid[y][x] != ' ':
              print 'Created an overlap at [%s, %s]' % (y,x)
            line.append([y,x])
            if hori:
                x += 1
            else:
                y += 1
            # TODO: And handle diagonal, too!
        else:
            #We found a place the word can't fit
            #Mark the starting point as invalid
            invalid.append(start)
            return insertWord(word, grid, invalid)

    # If it didn't work, try the reversed word.

    #Since it's a valid place, write to the grid and return
    for i,cell in enumerate(line):
        grid[cell[0]][cell[1]] = tokens[i]
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
        item = ''
        v = ord(vals[index])

        if v >= 0xd800 and v <+ 0xdbff:
            item += vals[index] + vals[index+1]
            index += 2
        else:
            item += vals[index]
            index += 1
        while index < len(vals) and ord(vals[index]) >= 0x300 and ord(vals[index]) <= 0x365:
            # It's a combining character. Add to the growing item.
            item += vals[index]
            index += 1
        retval.append(item)
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

words = [u'𐓏𐒻𐒷𐒻𐒷', u'𐓀𐒰𐓓𐒻͘', u'𐓏𐒰𐓓𐒰𐓓𐒷', u'𐒻𐒷𐓏𐒻͘ ', u'𐓈𐒻𐓍𐒷', u'𐒹𐓂𐓏𐒷͘𐒼𐒻',
         u'𐓇𐓈𐓂͘𐓄𐒰𐓄𐒷', u'𐒰̄𐓍𐓣𐓟𐓸𐓟̄𐓛𐓣̄𐓬', u'𐒼𐒰𐓆𐒻𐓈𐒰͘', u'𐓏𐒰𐓇𐒵𐒻͘𐒿𐒰 ',
         u'𐒻𐓏𐒻𐒼𐒻', u'𐓂𐓍𐒰𐒰𐒾𐓎𐓓𐓎𐒼𐒰']


Oldwords = [u"𐒰̄𐓂͘𐒴𐓎̄͘𐓒", u'𐓇𐓈𐓂͘𐓄𐒰𐓄𐒷', "python", "itertools", "wordsearch","code","review","functions",
         "dimensional", "dictionary", "lacklustre", 'google', 'unicode', u'𐓏𐒻𐒷𐒻𐒷']

grid, answers = makeGrid(words, [11,11])
printGrid(grid)
printAnswers(answers)
