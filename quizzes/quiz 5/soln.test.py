from soln import MatrixReader, max_parallelogram, max_rectangle
from random import seed, randrange

def generateMatrix(s, dim, density):
    '''
    generate a matrix in the same way as quiz_5.py

    Arguments:
    - s [int]
    - dim [int]
    - density [int]

    Returns:
    - matrix [(1 | 0)[20, 20]]
    '''
    seed(s)

    return [
        [int(randrange(density) != 0) for _ in range(dim)]
        for _ in range(dim)
    ]

def matrixReaderTest():
    M = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8]
    ]

    assert MatrixReader(M).read(0, 0) == 0
    assert MatrixReader(M).read(2, 2) == 8

    assert MatrixReader(M).read(-1, 2) == None
    assert MatrixReader(M).read(10, 2) == None

    assert MatrixReader(M, 1)[0, 0] == 0
    assert MatrixReader(M, 1)[1, 0] == 4
    assert MatrixReader(M, 1)[2, 0] == 8

    assert MatrixReader(M, 1).x_span()[0] == -2
    assert MatrixReader(M, 1).x_span()[1] == 2

    assert MatrixReader(M, 1).read(2, 2) == None

    assert MatrixReader(M, -1).read(0, 2) == 2
    assert MatrixReader(M, -1).read(1, 2) == 4
    assert MatrixReader(M, -1).read(2, 2) == 6

    assert MatrixReader(M, -1).x_span()[0] == 0
    assert MatrixReader(M, -1).x_span()[1] == 4

    assert MatrixReader(M, -1).read(2, 0) == None
    
def max_parallelogramTest():
    '''
    unit test of max_parallelogram(...)

    test cases extracted from quiz_5.pdf
    '''
    assert max_parallelogram([
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]) == 0

    assert max_parallelogram([
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1]
    ]) == 9

    assert max_parallelogram([
        [0, 0, 0],
        [0, 1, 1],
        [0, 1, 1]
    ]) == 4

    assert max_parallelogram([
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
    ]) == 0

    assert max_parallelogram([
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0]
    ]) == 0

    assert max_parallelogram([
        [0, 0, 0],
        [1, 1, 1],
        [0, 0, 0]
    ]) == 0

    assert max_parallelogram(
        generateMatrix(0, 10, 1)
    ) == 0

    assert max_parallelogram(
        generateMatrix(0, 10, 2)
    ) == 4

    assert max_parallelogram(
        generateMatrix(0, 10, 3)
    ) == 12

    assert max_parallelogram(
        generateMatrix(0, 10, 4)
    ) == 12

    assert max_parallelogram(
        generateMatrix(1, 10, 4)
    ) == 16

    assert max_parallelogram(
        generateMatrix(0, 10, 5)
    ) == 15


def max_rectangleTest():
    assert max_rectangle(MatrixReader([
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ])) == 0

    assert max_rectangle(MatrixReader([
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ])) == 0

    assert max_rectangle(MatrixReader([
        [0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ])) == 0

    assert max_rectangle(MatrixReader([
        [1, 0, 1, 0, 0],
        [1, 0, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 0, 0, 1, 0]
    ])) == 6

    assert max_rectangle(MatrixReader(
        generateMatrix(0, 10, 2)
    )) == 4

    assert max_rectangle(MatrixReader(
        generateMatrix(0, 10, 3)
    )) == 12

    assert max_rectangle(MatrixReader(
        generateMatrix(0, 10, 4)
    )) == 12

    assert max_rectangle(MatrixReader(
        generateMatrix(1, 10, 4)
    )) == 12

    assert max_rectangle(MatrixReader(
        generateMatrix(0, 10, 5)
    )) == 14

if __name__ == '__main__':
    print('Begin unit test on soln.py...')
    matrixReaderTest()
    max_rectangleTest()
    max_parallelogramTest()
    print('All tests passed!')
