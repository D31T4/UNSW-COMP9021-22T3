# COMP9021 22T3
# Quiz 2 *** Due Friday Week 4 @ 9.00pm
#        *** Late penalty 5% per day
#        *** Not accepted after Monday Week 5 @ 9.00pm

# DO *NOT* WRITE YOUR NAME TO MAINTAIN ANONYMITY FOR PLAGIARISM DETECTION


# Reading the number written in base 8 from right to left,
# keeping the leading 0's, if any:
# 0: move N     1: move NE    2: move E     3: move SE
# 4: move S     5: move SW    6: move W     7: move NW
#
# We start from a position that is the unique position
# where the switch is on.
#
# Moving to a position switches on to off, off to on there.

import sys

on = '\u26aa'
off = '\u26ab'
code = input('Enter a non-strictly negative integer: ').strip()
try:
    if code[0] == '-':
        raise ValueError
    int(code)
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
nb_of_leading_zeroes = 0
for i in range(len(code) - 1):
    if code[i] == '0':
        nb_of_leading_zeroes += 1
    else:
        break
print("Keeping leading 0's, if any, in base 8,", code, 'reads as',
      '0' * nb_of_leading_zeroes + f'{int(code):o}.'
     )

# INSERT YOUR CODE HERE
class Direction:
    '''
    A static class for directions
    '''
    N = '0'
    NE = '1'
    E = '2'
    SE = '3'
    S = '4'
    SW = '5'
    W = '6'
    NW = '7'

class ReadWriteHead:
    '''
    read write head of a 2d turing machine
    '''

    def __init__(self, position):
        '''
        Arguments:
        - position [(x: int, y: int)]: initial position
        '''
        self.position = list(position)

    def move(self, direction):
        '''
        move the read write head

        Arguments
        - position [char]: direction to be moved
        '''
        if direction == Direction.N:
            self.position[1] -= 1
        elif direction == Direction.NE:
            self.position[1] -= 1
            self.position[0] += 1
        elif direction == Direction.E:
            self.position[0] += 1
        elif direction == Direction.SE:
            self.position[0] += 1
            self.position[1] += 1
        elif direction == Direction.S:
            self.position[1] += 1
        elif direction == Direction.SW:
            self.position[0] -= 1
            self.position[1] += 1
        elif direction == Direction.W:
            self.position[0] -= 1
        elif direction == Direction.NW:
            self.position[0] -= 1
            self.position[1] -= 1
        else:
            raise ValueError('Unrecognized direction')

class TuringMachine2D:
    '''
    2d turing machine
    '''
    def __init__(self, gridSize, initialPosition):
        '''
        Arguments:
        - gridSize [(nrow: int, ncol: int)]: size of grid (2d tape)
        - initialPosition [(x: int, y: int)]: initial position of the read write head
        '''
        self.gridSize = tuple(gridSize)

        self.grid = [None for _ in range(gridSize[0])]

        for i in range(gridSize[0]):
            self.grid[i] = [False for _ in range(gridSize[1])]

        self.readWriteHead = ReadWriteHead(initialPosition)

    def write(self, value):
        '''
        write a value to the position of read write head

        Arguments:
        - value [bool]: value to be written
        '''
        x, y = self.readWriteHead.position
        self.grid[y][x] = value
    
    def read(self):
        '''
        read the value at the position of the read write head

        Returns:
        - value [bool]: value at read write head
        '''
        x, y = self.readWriteHead.position
        return self.grid[y][x]

    def move(self, direction):
        '''
        move the read write head

        Arguments:
        - direction [char]: direction to be moved
        '''
        self.readWriteHead.move(direction)
        x, y = self.readWriteHead.position

        assert 0 <= y and y < self.gridSize[0]
        assert 0 <= x and x < self.gridSize[1]

    def printVisibleGrid(self):
        '''
        print the minimul bounding box which contains every cells that has value 1
        '''
        bbox = BBox.fromTuringMachine2D(self)

        for row in range(bbox.minY, bbox.maxY + 1):
            string = ''

            for col in range(bbox.minX, bbox.maxX + 1):
                string += on if self.grid[row][col] else off

            print(string)

class BBox:
    def __init__(self, minX, minY, maxX, maxY):
        '''
        Arguments:
        - minX [num]
        - minY [num]
        - maxX [num]
        - maxY [num]
        '''
        self.minX = minX
        self.maxX = maxX
        self.minY = minY
        self.maxY = maxY

    def fromTuringMachine2D(tm):
        '''
        calculate the minimul bounding box containing all cells that has value `1`
        
        Arguments:
        - tm [TuringMachine2D]

        Returns:
        - bbox [BBox]
        '''
        minX = tm.gridSize[1] + 1
        maxX = -1
        minY = tm.gridSize[0] + 1
        maxY = -1

        for row in range(tm.gridSize[0]):
            for col in range(tm.gridSize[1]):
                if tm.grid[row][col]:
                    minX = min(col, minX)
                    maxX = max(col, maxX)
                    minY = min(row, minY)
                    maxY = max(row, maxY)

        return BBox(minX, minY, maxX, maxY)

    def fromInstructions(instructions):
        '''
        create a minimum bounding box which the read write head will traverse according to the instructions

        Arguments:
        - instructions [string]: instructions

        Returns:
        - bbox [BBox]:
        '''
        rwh = ReadWriteHead([0, 0])

        minX = 0
        maxX = 0
        minY = 0
        maxY = 0

        for step in instructions:
            rwh.move(step)
            
            x, y = rwh.position
            minX = min(minX, x)
            maxX = max(maxX, x)
            minY = min(minY, y)
            maxY = max(maxY, y)

        return BBox(minX, minY, maxX, maxY)

def printFinalState(instructions):
    '''
    print the *visible* final state of the 2d turing machine
    after the instructions are executed.

    the turing machine will:
    - write 1 to its initial position
    - for each step in the instructions: move to the direction and flip the value at that position

    finally, print the minimul bounding box which contains every cells that has value 1
    '''
    initialPosition = [0, 0]

    bbox = BBox.fromInstructions(instructions)

    initialPosition[0] -= bbox.minX
    initialPosition[1] -= bbox.minY

    bbox.maxX -= bbox.minX
    bbox.minX = 0
    bbox.maxY -= bbox.minY
    bbox.minY = 0

    tm = TuringMachine2D([bbox.maxY + 1, bbox.maxX + 1], initialPosition)
    tm.write(True)

    for step in instructions:
        tm.move(step)
        tm.write(not tm.read())

    tm.printVisibleGrid()

instructions = '0' * nb_of_leading_zeroes + f'{int(code):o}'
instructions = instructions[::-1]

print()
printFinalState(instructions)
