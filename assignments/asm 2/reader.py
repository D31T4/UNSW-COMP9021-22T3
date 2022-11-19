class MatrixReader:
    '''
    matrix reader. reused my own quiz 5 code.
    '''
    def __init__(self, mat, defaultValue = None):
        self.mat = mat
        self.n_row = len(mat)
        self.n_col = len(mat[0]) if self.n_row else 0
        self.defaultValue = defaultValue

    def read(self, row, col):
        '''
        read from grid

        Arguments:
        - row [int]
        - col [int]

        Returns:
        - value [int | None]: None if row, col is out of bound
        ''' 
        if row < 0 or row >= self.n_row:
            return self.defaultValue

        if col < 0 or col >= self.n_col:
            return self.defaultValue

        return self.mat[row][col]

    def __getitem__(self, index):
        '''
        read matrix entry at (row, col)

        Arguments:
        - point [[row: int, col: int]]

        Returns:
        - value at (row, col) [int | None]
        '''
        return self.read(index[0], index[1])
