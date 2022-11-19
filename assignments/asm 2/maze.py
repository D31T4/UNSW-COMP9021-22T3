 # COMP9021 22T3
# Assignment 2 *** Due Monday Week 11 @ 10.00am

# DO *NOT* WRITE YOUR NAME TO MAINTAIN ANONYMITY FOR PLAGIARISM DETECTION


# IMPORT ANY REQUIRED MODULE
import os
import csv
import re
from reader import MatrixReader

from test_helper import flatmap


class MazeError(Exception):
    def __init__(self, message):
        self.message = message

class Maze:
    '''
    Maze

    Properties
    - nrow [int]: no. of rows in maze grid
    - ncol [int]: no. of cols in maze grid
    - grid [int[][]]: maze grid
    - filename [string]: maze grid file name
    '''
    # min dim(y)
    MIN_ROW = 2
    # min dim(x)
    MIN_COL = 2

    # max dim(x)
    MAX_ROW = 41
    # max dim(y)
    MAX_COL = 31

    # no wall
    N_WALL = 0
    # top wall
    T_WALL = 1
    # left wall
    L_WALL = 2
    # top & left wall
    TL_WALL = 3

    # incorrect input error message
    INCORRECT_INPUT_MSG = 'Incorrect input.'
    # not a maze error message
    NOT_A_MAZE_MSG = 'Input does not represent a maze.'


    def __init__(self, filename):
        '''
        ctor.

        Arguments:
        - filename [string]: path to maze definition file. expects a `.txt` file
        '''
        # get filename
        directory, fname = os.path.split(filename)
        fname, ext = os.path.splitext(fname)

        self.filename = fname

        self.grid = []

        # read grid
        with open(filename, 'r') as f:
            for line in f:
                line = re.sub(r'\s+', '', line)
                if not line: continue

                try:
                    # try parse to int
                    self.grid.append([int(char) for char in line])
                except:
                    raise MazeError(Maze.INCORRECT_INPUT_MSG)


        self.n_row, self.n_col = Maze.validGrid(self.grid)

    
    def validGrid(grid):
        '''
        validate grid

        Arguments:
        - grid [int[][]]

        Returns:
        - n_row [int]: no. of row in grid
        - n_col [int]: no. of col in grid

        Raises:
        - MazeError
        '''
        # read and check dimension
        n_row = len(grid)

        if not n_row:
            raise MazeError(Maze.INCORRECT_INPUT_MSG)

        n_col = len(grid[0])
        validValues = [Maze.L_WALL, Maze.TL_WALL, Maze.T_WALL, Maze.N_WALL]

        for row in grid:
            if len(row) != n_col:
                raise MazeError(Maze.INCORRECT_INPUT_MSG)

            for cell in row:
                if cell not in validValues:
                    raise MazeError(Maze.INCORRECT_INPUT_MSG)

        if n_row < Maze.MIN_ROW or n_row > Maze.MAX_ROW:
            raise MazeError(Maze.INCORRECT_INPUT_MSG)

        if n_col < Maze.MIN_COL or n_col > Maze.MAX_COL:
            raise MazeError(Maze.INCORRECT_INPUT_MSG)


        # check cell value
        if grid[-1][-1] != Maze.N_WALL:
            raise MazeError(Maze.NOT_A_MAZE_MSG)

        if any(cell == Maze.L_WALL or cell == Maze.TL_WALL for cell in grid[-1][:n_col]):
            raise MazeError(Maze.NOT_A_MAZE_MSG)

        if any(row[-1] == Maze.T_WALL or row[-1] == Maze.TL_WALL for row in grid[:n_row]):
            raise MazeError(Maze.NOT_A_MAZE_MSG)
        
        return n_row, n_col

    def gates(self):
        '''
        enumerates all gates in the maze

        Yields:
        - row [int]
        - col [int]
        '''
        # top bound
        for col in range(self.n_col - 1):
            if self.grid[0][col] not in [Maze.T_WALL, Maze.TL_WALL]:
                yield -1, col

        # left bound
        for row in range(self.n_row - 1):
            if self.grid[row][0] not in [Maze.L_WALL, Maze.TL_WALL]:
                yield row, -1

            if self.grid[row][-1] != Maze.L_WALL:
                yield row, self.n_col - 1

        # bottom bound
        for col in range(self.n_col - 1):
            if self.grid[-1][col] != Maze.T_WALL:
                yield self.n_row - 1, col


    def countGates(self):
        '''
        count the no. of gates in the maze

        Returns:
        - no. of gates [int]
        '''
        return sum(1 for _ in self.gates())

    def points(self):
        '''
        Yields:
        - row [int]
        - col [int]
        - cell [int]
        '''
        for row in range(self.n_row):
            for col in range(self.n_col):
                yield row, col, self.grid[row][col]

    def countWalls(self):
        '''
        count the no. of connected components formed by walls

        Returns:
        - no. of connected components [int]
        '''
        # map: row, col => wall
        table = { 
            (row, col): None 
            for row, col, value in self.points() 
            if value in  [Maze.T_WALL, Maze.L_WALL, Maze.TL_WALL]
        }
                
        # counter for connected components,
        # also used as id of connected components
        count = 0

        reader = MatrixReader(self.grid)

        def neighborWalls(row, col):
            '''
            get neighboring walls at (row, col)

            Arguments:
            - row [int]
            - col [int]

            Yields:
            - row of neighboring walls [int]
            - col of neighboring walls [int]
            '''
            if reader[row, col] == Maze.L_WALL:
                if reader[row - 1, col] in [Maze.L_WALL, Maze.TL_WALL]:
                    yield row - 1, col

                if reader[row + 1, col] in [Maze.T_WALL, Maze.L_WALL, Maze.TL_WALL]:
                    yield row + 1, col

                if reader[row, col - 1] in [Maze.T_WALL, Maze.TL_WALL]:
                    yield row, col - 1

                if reader[row + 1, col - 1] in [Maze.T_WALL, Maze.TL_WALL]:
                    yield row + 1, col - 1

            elif reader[row, col] == Maze.T_WALL:
                if reader[row - 1, col] in [Maze.L_WALL, Maze.TL_WALL]:
                    yield row - 1, col

                if reader[row, col - 1] in [Maze.T_WALL, Maze.TL_WALL]:
                    yield row, col - 1

                if reader[row, col + 1] in [Maze.L_WALL, Maze.T_WALL, Maze.TL_WALL]:
                    yield row, col + 1

                if reader[row - 1, col + 1] in [Maze.L_WALL, Maze.TL_WALL]:
                    yield row - 1, col + 1

            elif reader[row, col] == Maze.TL_WALL:
                if reader[row - 1, col] in [Maze.L_WALL, Maze.TL_WALL]:
                    yield row - 1, col

                if reader[row + 1, col] in [Maze.L_WALL, Maze.T_WALL, Maze.TL_WALL]:
                    yield row + 1, col

                if reader[row, col + 1] in [Maze.L_WALL, Maze.T_WALL, Maze.TL_WALL]:
                    yield row, col + 1

                if reader[row, col - 1] in [Maze.T_WALL, Maze.TL_WALL]:
                    yield row, col - 1

                if reader[row - 1, col + 1] in [Maze.L_WALL, Maze.TL_WALL]:
                    yield row - 1, col + 1

                if reader[row + 1, col - 1] in [Maze.T_WALL, Maze.TL_WALL]:
                    yield row + 1, col - 1

        # dfs traversal
        for point in table.keys():
            if table[point] != None: 
                continue

            stack = [point]

            # visit 1 connected component
            while len(stack) > 0:
                row, col = stack.pop()
                table[(row, col)] = count

                for wp in neighborWalls(row, col):
                    if table[wp] == None:
                        stack.append(wp)
                
            count += 1

        return count

    def neighborCells(self, row, col):
        '''
        get neighboring cells of cell at (row, col)

        Arguments:
        - row [int]
        - col [int]

        Yields:
        - row of cell [int]
        - col of cell [int]
        '''
        if row < 0 or row > self.n_row - 2:
            return
        
        if col < 0 or col > self.n_col - 2:
            return

        # check top
        if row > 0 and self.grid[row][col] not in [Maze.T_WALL, Maze.TL_WALL]:
            yield row - 1, col

        # check left
        if col > 0 and self.grid[row][col] not in [Maze.L_WALL, Maze.TL_WALL]:
            yield row, col - 1

        # check right
        if col < self.n_col - 2 and self.grid[row][col + 1] not in [Maze.L_WALL, Maze.TL_WALL]:
            yield row, col + 1

        # check bottom
        if row < self.n_row - 2 and self.grid[row + 1][col] not in [Maze.T_WALL, Maze.TL_WALL]:
            yield row + 1, col

    # not visited mask
    NOT_VISITED_MASK = 0
    # cul-de-sac mask
    CDS_MASK = 1
    # path mask
    PATH_MASK = 2
    # visied mask
    VISITED_MASK = 3
    # n path mask
    N_PATH_MASK = 4

    def gatesAt(self, row, col):
        '''
        get gates at (row, col)

        Arguments:
        - row [int]
        - col [int]

        Yields:
        - gate coords [(row [int], col [int])]
        '''
        if row == 0 and self.grid[0][col] not in [Maze.T_WALL, Maze.TL_WALL]:
            yield -1, col

        if row == self.n_row - 2 and self.grid[-1][col] != Maze.T_WALL:
            yield self.n_row - 1, col

        if col == 0 and self.grid[row][col] not in [Maze.L_WALL, Maze.TL_WALL]:
            yield row, -1
            
        if col == self.n_col - 2 and self.grid[row][-1] not in [Maze.L_WALL, Maze.TL_WALL]:
            yield row, self.n_col - 1

    def countGatesAt(self, row, col):
        '''
        count gates at (row, col)

        Arguments:
        - row [int]
        - col [int]

        Returns:
        - no. of gates at (row, col) [int]
        '''
        return sum(1 for _ in self.gatesAt(row, col))

    def generateMask(self):
        '''
        generate mask.

        Returns:
        - no. of inaccessible inner points [int]
        - no. of cul de sacs [int]
        - no. of entry exit paths [int]
        - mask [int[][]]
        '''
        # init mask
        mask = [
            [Maze.NOT_VISITED_MASK] * (self.n_col - 1)
            for i in range(self.n_row - 1)
        ]

        # +-+-+-+--+
        # |     |  |
        # |  M  +  +
        # |     |  |
        # +-+-+-+  +
        # |    G   |
        # +-+-+-+--+
        #
        # valid coords for M: [0, n_row - 2], [0, n_col - 2]
        # valid coords for G: [0, n_row - 1], [0, n_col - 2]
        maskReader = MatrixReader(mask, Maze.NOT_VISITED_MASK)

        def repaint(row, col):
            stack = [(row, col)]

            while stack:
                row, col = stack.pop()

                if mask[row][col] != Maze.PATH_MASK: continue
                mask[row][col] = Maze.N_PATH_MASK

                for x, y in self.neighborCells(row, col):
                    stack.append((x, y))

        for erow, ecol in self.gates():
            # map gate coord to entry point coord
            row, col = enterMaze(erow, ecol, self.n_row, self.n_col)

            # callstack
            visited = set()

            def dfs(row, col, frow, fcol, begin = False):
                if (row, col) in visited: return 2

                # visited by previous traversals already
                if not begin and maskReader[row, col] != Maze.NOT_VISITED_MASK:
                    if maskReader[row, col] == Maze.PATH_MASK:
                        return 1
                    elif maskReader[row, col] == Maze.N_PATH_MASK:
                        return 2

                visited.add((row, col))

                gatesCount = self.countGatesAt(row, col)
                # minus 1 to compensate entry point
                if begin: gatesCount -= 1

                numPath = 0

                mask[row][col] = Maze.VISITED_MASK

                # write change if a gate is reached
                if begin or gatesCount == 0:
                    for y, x in self.neighborCells(row, col):
                        if y != frow or x != fcol:
                            numPath += dfs(y, x, row, col)

                visited.remove((row, col))

                numPath += gatesCount

                mask[row][col] = Maze.CDS_MASK if numPath == 0 else Maze.PATH_MASK
                
                return numPath

            # repaint mask to N_PATH
            if dfs(row, col, erow, ecol, begin=True) > 1:
                repaint(row, col)
            
        return mask

    def generateAnalysisReport(self):
        '''
        generate analysis report

        Returns:
        - n_gates [int]: no. of gates
        - n_walls [int]: no. of connected components formed by walls
        - n_inaccessible [int]: no. of inaccessible cells
        - n_accessible [int]: no. of connected components that are accessible
        - n_cds [int]: no. of connected components formed by cul-de-sacs
        - n_path [int]: no. of entry-exit path
        '''
        n_gates = self.countGates()
        n_walls = self.countWalls()

        mask = self.generateMask()

        n_inaccessible = sum(1 for el in flatmap(mask) if el == Maze.NOT_VISITED_MASK)

        n_accessible = 0
        n_cds = 0
        n_path = 0

        # dfs again...
        visited = set()

        for row, col in self.gates():
            row, col = enterMaze(row, col, self.n_row, self.n_col)
            if (row, col) in visited: continue

            n_accessible += 1

            if mask[row][col] == Maze.PATH_MASK:
                n_path += 1

            stack = [(row, col)]

            while stack:
                row, col = stack.pop()
                if (row, col) in visited: continue

                # count and visit cul-de-sac
                if mask[row][col] == Maze.CDS_MASK:
                    stack2 = [(row, col)]
                    visited.add((row, col))
                    n_cds += 1

                    while stack2:
                        row2, col2 = stack2.pop()

                        for point in self.neighborCells(row, col):
                            if point not in visited and mask[row][col] == Maze.CDS_MASK:
                                stack2.append(point)
                                visited.add(point)
                else:
                    visited.add((row, col))

                for point in self.neighborCells(row, col):
                    if point not in visited:
                        stack.append(point)

        return n_gates, n_walls, n_inaccessible, n_accessible, n_path, n_cds

    def analyse(self):
        '''
        analyse maze.

        Effects:
        - print to output
        '''
        n_gates, n_walls, n_inaccessible, n_accessible, n_path, n_cds = self.generateAnalysisReport()

        if n_gates == 0:
            print('The maze has no gate.')
        elif n_gates == 1:
            print('The maze has a single gate.')
        else:
            print(f'The maze has {n_gates} gates.')

        if n_walls == 0:
            print('The maze has no wall.')
        elif n_walls == 1:
            print('The maze has walls that are all connected.')
        else:
            print(f'The maze has {n_walls} sets of walls that are all connected.')

        if n_inaccessible == 0:
            print('The maze has no inaccessible inner point.')
        elif n_accessible == 1:
            print('The maze has a unique inaccessible inner point.')
        else:
            print(f'The maze has {n_inaccessible} inaccessible inner points.')

        if n_accessible == 0:
            print('The maze has no accessible area.')
        elif n_accessible == 1:
            print('The maze has a unique accessible area.')
        else:
            print(f'The maze has {n_accessible} accessible areas.')

        if n_cds == 0:
            print('The maze has no accessible cul-de-sac.')
        elif n_cds == 1:
            print('The maze has accessile cul-de-sacs that are all connected.')
        else:
            print(f'The maze has {n_cds} sets of accessible cul-de-sacs that are all connected.')

        if n_path == 0:
            print('The maze has no entry-exit path with no intersection not to cul-de-sacs.')
        elif n_path == 1:
            print('The maze has a unique entry-exit path with no intersection not to cul-de-sacs.')
        else:
            print(f'The maze has {n_path} entry-exit paths with no intersections not to cul-de-sacs.')

    
    def display(self):
        '''
        Effects:
        - write a .tex file
        '''
        maze_to_tex(self, f'{self.filename}.tex')

def enterMaze(row, col, n_row, n_col):
    '''
    maps gate coords to maze mask coords

    Arguments:
    - row [int]
    - col [int]
    - n_row [int]: no. of row in grid
    - n_col [int]: no. of row in grid

    Returns:
    - row [int]
    - col [int]
    '''  
    if row == -1:
        return 0, col
    if col == -1:
        return row, 0
    if row == n_row - 1:
        return n_row - 2, col
    if col == n_col - 1:
        return row, n_col - 2
    raise ValueError('input is not a gate')

'''
maze to tex
'''
def walls(maze):
    '''
    Arguments:
    - maze [Maze]
    
    Returns:
    - horizontal walls [row [int], col [int], len [int]]
    - vertical walls [row [int], col [int], len [int]]
    - pillars [(row [int], col [int])[]]
    '''
    # horizontal walls
    h_walls = []
    pillars = []

    # get horizontal wall segments and pillars
    for row in range(maze.n_row):
        for col in range(maze.n_col):
            if maze.grid[row][col] in [Maze.T_WALL, Maze.TL_WALL]:
                if h_walls and h_walls[-1][0] == row and h_walls[-1][1] + h_walls[-1][2] == col:
                    h_walls[-1][2] += 1
                else:
                    h_walls.append([row, col, 1])

            if maze.grid[row][col] == Maze.N_WALL:
                shouldAdd = True

                if row > 0:
                    shouldAdd = shouldAdd and maze.grid[row - 1][col] not in [Maze.L_WALL, Maze.TL_WALL]
                
                if col > 0:
                    shouldAdd = shouldAdd and maze.grid[row][col - 1] not in [Maze.T_WALL, Maze.TL_WALL]
                    
                if shouldAdd:
                    pillars.append((row, col))

    h_walls.sort(key=lambda el: tuple(el[:2]))

    # vertical walls
    v_walls = []

    for col in range(maze.n_col):
        for row in range(maze.n_row):
            if maze.grid[row][col] not in [Maze.L_WALL, Maze.TL_WALL]:
                continue

            if v_walls and v_walls[-1][1] == col and v_walls[-1][0] + v_walls[-1][2] == row:
                v_walls[-1][2] += 1
            else:
                v_walls.append([row, col, 1])

    v_walls.sort(key=lambda el: tuple(el[:2][::-1]))

    return h_walls, v_walls, pillars

def paths(maze, mask):
    '''
    split paths into horizontal segments and vertical segments

    Arguments
    - maze [Maze]: maze instance
    - mask [int[][]]: mask from Maze.generateMask(...)

    Returns:
    - h_segments [(row [int], col [int], len [int])[]]
    - v_segments [(row [int], col [int], len [int])[]]
    '''
    h_segments = []
    v_segments = []

    visited = [
        [False] * (maze.n_col - 1)
        for _ in range(maze.n_row - 1)
    ]

    gridReader = MatrixReader(maze.grid)

    def add2Segments(segment1, segment2):
        '''
        add a point to a segment

        Arguments:
        - point [row [int], col [int]]
        - segment [row [int], col [int], len [int]]

        Effects:
        - mutate segment

        Raises:
        - ValueError: if the point cannot be merged to the segment
        '''
        # horizontal segment
        if segment1[0] == segment2[0]:
            if segment1[1] + segment1[2] == segment2[1]:
                segment1[2] += segment2[2]
            elif segment1[1] == segment2[1] + segment2[2]:
                segment1[1] = segment2[1]
                segment1[2] += segment2[2]
            else:
                return False
        # vertial segment
        elif segment1[1] == segment2[1]:
            if segment1[0] + segment1[2] == segment2[0]:
                segment1[2] += segment2[2]
            elif segment1[0] == segment2[0] + segment2[2]:
                segment1[0] = segment2[0]
                segment1[2] += segment2[2]
            else:
                return False
        else:
            return False

        return True

    def step(row, col):
        '''
        step to next node in path

        Arguments
        - row [int]: row of current node
        - col [int]: col of current node

        Returns:
        - row [int]: row of next node
        - col [int]: col of next node
        '''
        for nrow, ncol in maze.neighborCells(row, col):
            if mask[nrow][ncol] == Maze.PATH_MASK and not visited[nrow][ncol]:
                return nrow, ncol

        return None, None

    # split paths into segments
    for erow, ecol in maze.gates():
        row, col = enterMaze(erow, ecol, maze.n_row, maze.n_col)
        if visited[row][col]: continue
        if mask[row][col] != Maze.PATH_MASK: continue

        visited[row][col] = True

        currentSegment = [min(row, erow), min(col, ecol), 1]
        segmentIsHorizontal = erow == row

        if segmentIsHorizontal:
            h_segments.append(currentSegment)
        else:
            v_segments.append(currentSegment)

        nrow, ncol = step(row, col)

        # traverse path and build segments
        while nrow != None and ncol != None:
            visited[nrow][ncol] = True
            newSegment = [min(row, nrow), min(col, ncol), 1]

            if not ((nrow == row and segmentIsHorizontal) or (ncol == col and not segmentIsHorizontal)) or not add2Segments(currentSegment, newSegment):
                segmentIsHorizontal = nrow == row
                currentSegment = newSegment

                if segmentIsHorizontal:
                    h_segments.append(currentSegment)
                else:
                    v_segments.append(currentSegment)

            row, col = nrow, ncol
            nrow, ncol = step(row, col)
        
        # add end gate
        for grow, gcol in maze.gatesAt(row, col):
            if grow == erow and gcol == ecol: continue

            newSegment = [min(row, grow), min(col, gcol), 1]

            if not ((grow == row and segmentIsHorizontal) or (gcol == col and not segmentIsHorizontal)) or not add2Segments(currentSegment, newSegment):
                segmentIsHorizontal = grow == row
                currentSegment = newSegment

                if segmentIsHorizontal:
                    h_segments.append(currentSegment)
                else:
                    v_segments.append(currentSegment)

            break

    h_segments.sort(key=lambda el: tuple(el[:2]))
    v_segments.sort(key=lambda el: tuple(el[:2][::-1]))
    return h_segments, v_segments

def maze_to_tex(maze, fname):
    '''
    print maze analysis result to a tex file

    Arguments:
    - maze [Maze]
    - fname [string]

    Effects:
    - file creation
    '''
    mask = maze.generateMask()

    with open(fname, 'w') as f:
        # write begin
        f.write('\\documentclass[10pt]{article}\n')
        f.write('\\usepackage{tikz}\n')
        f.write('\\usetikzlibrary{shapes.misc}\n')
        f.write('\\usepackage[margin=0cm]{geometry}\n')
        f.write('\\pagestyle{empty}\n')
        f.write('\\tikzstyle{every node}=[cross out, draw, red]\n\n')
        f.write('\\begin{document}\n\n')
        f.write('\\vspace*{\\fill}\n')
        f.write('\\begin{center}\n')
        f.write('\\begin{tikzpicture}[x=0.5cm, y=-0.5cm, ultra thick, blue]\n')

        f.write('% Walls\n')

        h_walls, v_walls, pillars = walls(maze)

        for y, x, l in h_walls:
            f.write(f'    \\draw ({x},{y}) -- ({x + l},{y});\n')

        for y, x, l in v_walls:
            f.write(f'    \\draw ({x},{y}) -- ({x},{y + l});\n')

        f.write('% Pillars\n')

        for y, x in pillars:
            f.write(f'    \\fill[green] ({x},{y}) circle(0.2);\n')

        f.write('% Inner points in accessible cul-de-sacs\n')

        for y, row in enumerate(mask):
            for x, val in enumerate(row):
                if val == Maze.CDS_MASK:
                    f.write(f'    \\node at ({x + 0.5},{y + 0.5}) {{}};\n')

        f.write('% Entry-exit paths without intersections\n')

        h_segments, v_segments = paths(maze, mask)

        # draw horizontal
        for y, x, l in h_segments:
            f.write(f'    \\draw[dashed, yellow] ({x + 0.5},{y + 0.5}) -- ({x + l + 0.5},{y + 0.5});\n')

        # draw vertical
        for y, x, l in v_segments:
            f.write(f'    \\draw[dashed, yellow] ({x + 0.5},{y + 0.5}) -- ({x + 0.5},{y + l + 0.5});\n')

        f.write('\\end{tikzpicture}\n')
        f.write('\\end{center}\n')
        f.write('\\vspace*{\\fill}\n\n')
        f.write('\\end{document}\n')
