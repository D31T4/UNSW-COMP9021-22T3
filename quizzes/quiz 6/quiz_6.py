# COMP9021 22T3
# Quiz 6 *** Due Friday Week 9 @ 9.00pm
#        *** Late penalty 10% per day
#        *** Not accepted after Monday Week 10 @ 9.00pm

# DO *NOT* WRITE YOUR NAME TO MAINTAIN ANONYMITY FOR PLAGIARISM DETECTION


# Randomly generates a grid of 0s and 1s and determines
# the maximum number of "spikes" in a shape.
# A shape is made up of 1s connected horizontally or vertically (it can contain holes).
# A "spike" in a shape is a 1 that is part of this shape and "sticks out"
# (has exactly one neighbour in the shape).
# Neighbours are only considered vertically or horizontally (not diagonally).
# Note that a shape with a single 1 is also a spike.

from random import seed, randrange
import sys

from soln import maxSpikes

dim = 10


def display_grid():
    for row in grid:
        print('   ', *row) 


try: 
    for_seed, density = (int(x) for x in input('Enter two integers, the second '
                                               'one being strictly positive: '
                                              ).split()
                    )
    if density <= 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(for_seed)
grid = [[int(randrange(density) != 0) for _ in range(dim)]
            for _ in range(dim)
       ]
print('Here is the grid that has been generated:')
display_grid()
print('The maximum number of spikes of some shape is:',
      maxSpikes(grid, dim, dim)
     )
