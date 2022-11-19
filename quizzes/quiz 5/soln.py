class MatrixReader:
    '''
    matrix reader
    '''

    def __init__(self, matrix, shear = 0):
        '''
        ctor.

        If shear = 1:
         0 1 2          -2 1 0 1 2
         -----           ---------
        |1 0 0|         |0 0 1 0 0|
        |0 1 0| read as |0 0 1 0 0|
        |0 0 1|         |0 0 1 0 0|

        Arguments:
        - matrix [int[N, M]]
        - shear [int]: shear force applied to the matrix
        '''
        self.matrix = matrix
        self.shear = int(shear)

        self.n_row = len(matrix)
        assert self.n_row > 0

        self.n_col = len(matrix[0])
        assert self.n_col > 0

    def x_span(self):
        offset = abs(self.shear) * (self.n_row - 1)
        
        if self.shear > 0:
            return -offset, self.n_col - 1
        else:
            return 0, self.n_col + offset - 1

    def read(self, row, col):
        '''
        read matrix entry at (row, col)

        Arguments:
        - row [int]
        - col [int]

        Returns:
        - value [int | None]
        '''
        if row < 0 or row > self.n_row - 1:
            return None

        col += row * self.shear

        if col < 0 or col > self.n_col - 1:
            return None

        return self.matrix[row][col]

    def __getitem__(self, point):
        '''
        read matrix entry at (row, col)

        Arguments:
        - point [[row: int, col: int]]

        Returns:
        - value at (row, col) [int | None]
        '''
        return self.read(point[0], point[1])

def max_parallelogram(matrix):
    '''
    compute area of the largest parallelogram

    Arguments:
    - matrix [bool[N, M]]

    Returns:
    - area [int]
    '''
    return max(
        # rect
        max_rectangle(MatrixReader(matrix)), 
        # skew right
        max_rectangle(MatrixReader(matrix, 1)),
        # skew left 
        max_rectangle(MatrixReader(matrix, -1))
    )

def max_rectangle(reader):
    '''
    compute area of largest rectangle

    DP idea stolen from: 
    https://leetcode.com/problems/maximal-rectangle/discuss/29054/Share-my-DP-solution

    Arguments:
    - matrix reader [MatrixReader]

    Returns:
    - area [int]
    '''
    maxArea = 0

    min_col, max_col = reader.x_span()
    n_col = (max_col - min_col) + 1

    # height of the 'pillar' at col = i
    height = [0] * n_col

    # left bound of the 'pillar' at col = i
    # use 0 if there is no pillar at i, for easier update
    L = [min_col] * n_col

    # right bound of the 'pillar' at col = i
    # use max(col) if there is no pillar at i, for easier update
    R = [max_col] * n_col

    # dp
    for row in range(reader.n_row):
        L_bound = 0
        R_bound = max_col

        for offset in range(n_col):
            # update height and left bound
            if reader[row, min_col + offset] == 1:
                height[offset] += 1
                L[offset] = max(L[offset], L_bound)
            else:
                # reset height, left bound
                height[offset] = 0
                L[offset] = 0
                # update current left
                L_bound = offset + 1

        # update right bound
        for offset in range(n_col - 1, -1, -1):
            if reader[row, min_col + offset] == 1:
                R[offset] = min(R[offset], R_bound)
            else:
                # reset right bound and current right
                R[offset] = n_col - 1
                R_bound = offset - 1

        # update max(A)
        for offset in range(n_col):
            # assignment spec:
            # we only consider rects with height > 1 and width >= 2
            if height[offset] > 1 and R[offset] - L[offset] >= 1:
                maxArea = max(maxArea, height[offset] * (R[offset] - L[offset] + 1))

    return maxArea
        
