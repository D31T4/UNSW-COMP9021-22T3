from random import seed, randrange
from soln import generateMask, maxSpikes

def flatmap(x):
    '''
    flatten the list

    Arguments:
    - x [T[][]]

    Yields:
    list element [T]
    '''
    for l in x:
        for el in l:
            yield el

def generateMatrix(for_seed, density, dim):
    '''
    generate matrix

    Arguments:
    - for_seed [int]: rand seed
    - density [int]
    - dim: int

    Returns:
    [int[][]]
    '''
    seed(for_seed)
    return [
        [int(randrange(density) != 0) for _ in range(dim)]
        for _ in range(dim)
    ]

def matrixEq(m1, m2):
    assert len(m1) == len(m2) and all(tuple(r1) == tuple(r2) for r1, r2 in zip(m1, m2))

def printMatrix(mat):
    # space to allocate for each entry
    L = max(
        len(str(max(flatmap(mat)))),
        len(str(min(flatmap(mat))))
    )

    for row in mat:
        print(', '.join(
            str(entry).rjust(L, ' ')
            for entry in row
        ))

def generateMaskTest():
    '''
    unit test of generateMask(...)
    '''
    DIM = 10

    mask, shapes = generateMask(generateMatrix(0, 2, DIM), DIM, DIM)
    printMatrix(mask)

def maxSpikesTest():
    '''
    unit test of maxSpikes(...)

    Test cases extracted from quiz_6.pdf
    '''
    DIM = 10

    assert maxSpikes(
        generateMatrix(0, 8, DIM), DIM, DIM
    ) == 1

    assert maxSpikes(
        generateMatrix(0, 7, DIM), DIM, DIM
    ) == 3

    assert maxSpikes(
        generateMatrix(0, 2, DIM), DIM, DIM
    ) == 7

    assert maxSpikes(
        generateMatrix(0, 4, DIM), DIM, DIM
    ) == 8

    assert maxSpikes(
        generateMatrix(1, 2, DIM), DIM, DIM
    ) == 5

    assert maxSpikes(
        generateMatrix(2, 2, DIM), DIM, DIM
    ) == 4

    assert maxSpikes(
        generateMatrix(2, 1, DIM), DIM, DIM
    ) == 0

if __name__ == '__main__':
    print('begin unit test for soln.py...')
    #generateMaskTest()
    maxSpikesTest()
    print('all tests passed!')
