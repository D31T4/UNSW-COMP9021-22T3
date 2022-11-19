from maze import Maze, MazeError
from test_helper import catch, flatmap

class MazeMock(Maze):
    '''
    mock of `Maze`. allows construction by 2d matrix.
    '''
    def __init__(self, grid, fname='maze_mock'):
        '''
        Arguments:
        - grid [int[N, M]]: grid
        - fname [string]: filename
        '''
        self.grid = grid
        self.n_row, self.n_col = Maze.validGrid(grid)
        self.filename = fname

def validGridTest():
    '''
    unit test for Maze.validGrid(...)

    test cases extracted from default scaffold and `more examples.zip`
    '''
    # incorrect_input_1.txt (invalid dim)
    ex = catch(lambda: Maze.validGrid([
        [0, 0]
    ]))

    assert isinstance(ex, MazeError) and str(ex) == Maze.INCORRECT_INPUT_MSG

    # incorrect_input_2.txt (inconsistent dim)
    ex = catch(lambda: Maze.validGrid([
        [0, 0],
        [0, 0, 0]
    ]))

    assert isinstance(ex, MazeError) and str(ex) == Maze.INCORRECT_INPUT_MSG

    #  invalid cell value
    ex = catch(lambda: Maze.validGrid([
        [0, 0, 0],
        [0, 5, 0],
        [0, 0, 0]
    ]))

    assert isinstance(ex, MazeError) and str(ex) == Maze.INCORRECT_INPUT_MSG

    # not_a_maze_1.txt
    ex = catch(lambda: Maze.validGrid([
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 1]
    ]))

    assert isinstance(ex, MazeError) and str(ex) == Maze.NOT_A_MAZE_MSG

    # not_a_maze_2.txt
    ex = catch(lambda: Maze.validGrid([
        [3, 3, 3, 2],
        [2, 0, 0, 2],
        [1, 3, 0, 0]
    ]))

    assert isinstance(ex, MazeError) and str(ex) == Maze.NOT_A_MAZE_MSG

    # maze_1.txt
    n_row, n_col = Maze.validGrid([
        [1,  0,  2,  2,  1,  2,  3,  0],     
        [3,  2,  2,  1,  2,  0,  2,  2],     
        [3,  0,  1,  1,  3,  1,  0,  0],
        [2,  0,  3,  0,  0,  1,  2,  0],
        [3,  2,  2,  0,  1,  2,  3,  2],   
        [1,  0,  0,  1,  1,  0,  0,  0]
    ])

    assert n_row == 6 and n_col == 8

    # maze_2.txt
    n_row, n_col = Maze.validGrid([
        [0,2,2,3,0,2,1,2,0,2,2,2],
        [2,2,2,2,2,3,1,1,1,0,3,2],
        [3,0,1,3,2,2,1,3,0,3,0,2],
        [3,1,2,3,2,2,2,3,2,3,3,0],
        [0,0,1,0,0,0,1,0,0,0,0,0]
    ])

    assert n_row == 5 and n_col == 12  

    # labyrinth.txt
    n_row, n_col = Maze.validGrid([
        [3,1,1,1,1,1,1,1,1,3,2],
        [2,1,1,2,2,1,3,1,2,0,2],
        [3,3,0,2,3,0,2,2,1,1,2],
        [2,0,3,1,0,2,1,3,1,2,2],
        [3,1,0,1,1,1,2,0,2,0,2],
        [2,1,2,3,0,2,3,0,1,1,2],
        [3,0,2,2,3,0,3,1,3,0,2],
        [0,3,1,2,2,1,2,1,2,1,2],
        [2,2,2,0,3,1,1,0,3,2,2],
        [2,2,1,1,0,3,1,1,0,0,2],
        [1,1,1,1,1,1,0,1,1,1,0]
    ])

    assert n_row == 11 and n_col == 11

def countGatesTest():
    '''
    unit test for Maze.countGates(...)

    test cases extracted from default scaffold and `more examples.zip`
    '''
    assert Maze('input_samples/maze_1.txt').countGates() == 12
    assert Maze('input_samples/maze_2.txt').countGates() == 20
    assert Maze('input_samples/labyrinth.txt').countGates() == 2

def countWallsTest():
    '''
    unit test for Maze.countWalls(...)

    test cases extracted from default scaffold and `more examples.zip`
    '''
    assert Maze('input_samples/maze_1.txt').countWalls() == 8
    assert Maze('input_samples/maze_2.txt').countWalls() == 4
    assert Maze('input_samples/labyrinth.txt').countWalls() == 2
        

def matrixEq(m1, m2):
    '''
    equality comparison of 2 matrix

    Arguments:
    - m1 [any[][]]
    - m2 [any[][]]

    Returns:
    are equal [bool]
    '''
    l1 = list(flatmap(m1))
    l2 = list(flatmap(m2))

    return len(l1) == len(l2) and all(v1 == v2 for v1, v2 in zip(l1, l2))

def printMatrix(m):
    '''
    print matrix

    Arguments:
    - m [any[][]]

    Effects:
    - print matrix
    '''
    for row in m:
        print(''.join(str(cell) for cell in row))

def generateMaskTest():
    '''
    unit test for Maze.generateMask(...)

    test cases extracted from default scaffold and `more examples.zip`
    '''
    m = Maze('input_samples/maze_1.txt').generateMask()

    assert matrixEq(m, [
        [4, 4, 1, 2, 2, 2, 4],
        [0, 4, 1, 1, 2, 2, 4],
        [4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4],
        [0, 4, 4, 4, 1, 4, 1]
    ])

    m = Maze('input_samples/maze_2.txt').generateMask()

    assert matrixEq(m, [
        [2, 1, 1, 1, 2, 1, 1, 2, 2, 4, 1],
        [1, 1, 1, 1, 2, 4, 4, 4, 4, 4, 0],
        [1, 1, 1, 0, 2, 4, 1, 1, 4, 0, 0],
        [2, 2, 1, 1, 2, 4, 1, 1, 4, 1, 2]
    ])

    m = Maze('input_samples/labyrinth.txt').generateMask()

    assert matrixEq(m, [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 2, 2, 1, 1, 1, 1],
        [1, 1, 2, 2, 2, 2, 2, 1, 1, 1],
        [2, 2, 2, 1, 1, 1, 2, 2, 1, 1],
        [2, 2, 1, 1, 1, 1, 1, 2, 2, 2],
        [2, 2, 1, 1, 1, 1, 1, 1, 2, 2],
        [2, 1, 1, 1, 1, 1, 1, 1, 2, 2],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
        [1, 1, 1, 1, 1, 1, 2, 2, 2, 2],
    ])

    m = MazeMock([
        [1, 1, 1, 1, 2, 0],
        [1, 1, 2, 0, 2, 0],
        [0, 0, 2, 0, 2, 0],
        [0, 0, 2, 0, 1, 0],
        [0, 0, 1, 1, 1, 0]
    ]).generateMask()

    assert matrixEq(m, [
        [4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4]
    ])

    m = MazeMock([
        [0, 0],
        [0, 0]
    ]).generateMask()

    assert matrixEq(m, [
        [4]
    ])

    m = MazeMock([
        [1, 2],
        [1, 0]
    ]).generateMask()

    assert matrixEq(m, [
        [1]
    ])

    m = MazeMock([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]).generateMask()

    assert matrixEq(m, [
        [4, 4, 4],
        [4, 4, 4],
        [4, 4, 4]
    ])

    # from discussion #1126142
    m = MazeMock([
        [3, 1, 1, 2],
        [0, 0, 0, 2],
        [2, 0, 0, 2],
        [1, 1, 1, 0]
    ]).generateMask()

    assert matrixEq(m, [
        [4, 4, 4],
        [4, 4, 4],
        [4, 4, 4]
    ])


def generateAnalysisReportTest():
    '''
    unit test for Maze.generateAnalysisReport(...)

    test cases extracted from default scaffold and `more examples.zip`
    '''
    n_gates, n_walls, n_inaccessible, n_accessible, n_path, n_cds = Maze('input_samples/maze_1.txt').generateAnalysisReport()
    assert n_gates == 12
    assert n_walls == 8
    assert n_inaccessible == 2
    assert n_accessible == 4
    assert n_cds == 3
    assert n_path == 1

    n_gates, n_walls, n_inaccessible, n_accessible, n_path, n_cds = Maze('input_samples/maze_2.txt').generateAnalysisReport()
    assert n_gates == 20
    assert n_walls == 4
    assert n_inaccessible == 4
    assert n_accessible == 13
    assert n_cds == 11
    assert n_path == 5

    n_gates, n_walls, n_inaccessible, n_accessible, n_path, n_cds = Maze('input_samples/labyrinth.txt').generateAnalysisReport()
    assert n_gates == 2
    assert n_walls == 2
    assert n_inaccessible == 0
    assert n_accessible == 1
    assert n_cds == 8
    assert n_path == 1

    n_gates, n_walls, n_inaccessible, n_accessible, n_path, n_cds = MazeMock([
        [1, 1, 1, 1, 2, 0],
        [1, 1, 2, 0, 2, 0],
        [0, 0, 2, 0, 2, 0],
        [0, 0, 2, 0, 1, 0],
        [0, 0, 1, 1, 1, 0]
    ]).generateAnalysisReport()
    assert n_gates == 11
    assert n_walls == 2
    assert n_inaccessible == 0
    assert n_accessible == 3
    assert n_cds == 0
    assert n_path == 0

    n_gates, n_walls, n_inaccessible, n_accessible, n_path, n_cds = MazeMock([
        [0, 0],
        [0, 0]
    ]).generateAnalysisReport()
    assert n_gates == 4
    assert n_walls == 0
    assert n_inaccessible == 0
    assert n_accessible == 1
    assert n_cds == 0
    assert n_path == 0

    n_gates, n_walls, n_inaccessible, n_accessible, n_path, n_cds = MazeMock([
        [1, 2],
        [1, 0]
    ]).generateAnalysisReport()
    assert n_gates == 1
    assert n_walls == 1
    assert n_inaccessible == 0
    assert n_accessible == 1
    assert n_cds == 1
    assert n_path == 0

    n_gates, n_walls, n_inaccessible, n_accessible, n_path, n_cds = MazeMock([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]).generateAnalysisReport()
    assert n_gates == 12
    assert n_walls == 0
    assert n_inaccessible == 0
    assert n_accessible == 1
    assert n_cds == 0
    assert n_path == 0

    n_gates, n_walls, n_inaccessible, n_accessible, n_path, n_cds = MazeMock([
        [3, 1, 1, 2],
        [0, 0, 0, 2],
        [2, 0, 0, 2],
        [1, 1, 1, 0]
    ]).generateAnalysisReport()
    assert n_gates == 1
    assert n_walls == 1
    assert n_inaccessible == 0
    assert n_accessible == 1
    assert n_cds == 0
    assert n_path == 0

    n_gates, n_walls, n_inaccessible, n_accessible, n_path, n_cds = MazeMock([
        [1, 0],
        [1, 0]
    ]).generateAnalysisReport()
    assert n_gates == 2
    assert n_walls == 2
    assert n_inaccessible == 0
    assert n_accessible == 1
    assert n_cds == 0
    assert n_path == 1

    n_gates, n_walls, n_inaccessible, n_accessible, n_path, n_cds = MazeMock([
        [3, 1, 2],
        [2, 0, 2],
        [1, 1, 0]
    ]).generateAnalysisReport()
    assert n_gates == 0
    assert n_walls == 1
    assert n_inaccessible == 4
    assert n_accessible == 0
    assert n_cds == 0
    assert n_path == 0
    
    n_gates, n_walls, n_inaccessible, n_accessible, n_path, n_cds = MazeMock([
        [3, 1, 1, 2],
        [0, 3, 2, 2],
        [2, 1, 0, 2],
        [1, 1, 1, 0]
    ]).generateAnalysisReport()
    assert n_gates == 1
    assert n_walls == 2
    assert n_inaccessible == 1
    assert n_path == 0
    assert n_cds == 0

if __name__ == '__main__':   
    print('Begin unit test on maze.py...')
    validGridTest()
    countGatesTest()
    countWallsTest()
    generateMaskTest()
    generateAnalysisReportTest()
    print('All tests passed!')
