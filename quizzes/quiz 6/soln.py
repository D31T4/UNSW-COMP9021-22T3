

def generateMask(mat, nrow, ncol):
    '''
    generate a mask

    Arguments
    - mat [int[N, N]]: 2D matrix
    - nrow [int]: no. of rows of matrix
    - ncol [int]: no. of cols of matrix

    Returns:
    - mask [int[N, N]]: 2D mask showing each shape
    - shapes [int[]]: starting point of shape map: id => (row, col)
    '''
    mask = [
        [0] * ncol for i in range(nrow)
    ]

    shapeCount = 0
    shapes = []

    for row in range(nrow):
        for col in range(ncol):
            # already visited
            if mask[row][col]:
                continue

            # not a shape
            if not mat[row][col]:
                continue

            shapeCount += 1
            shapes.append((row, col))

            stack = [(row, col)]

            while stack:
                row, col = stack.pop()
                mask[row][col] = shapeCount

                if row > 0 and mat[row - 1][col] and not mask[row - 1][col]:
                    stack.append((row - 1, col))

                if col > 0 and mat[row][col - 1] and not mask[row][col - 1]:
                    stack.append((row, col - 1))

                if row < nrow - 1 and mat[row + 1][col] and not mask[row + 1][col]:
                    stack.append((row + 1, col))

                if col < ncol - 1 and mat[row][col + 1] and not mask[row][col + 1]:
                    stack.append((row, col + 1))

    return mask, shapes

def maxSpikes(mat, nrow, ncol):
    '''
    compute max no. of spikes in all shapes

    Arguments:
    - mat [int[N, N]]: 2D matrix
    - nrow [int]: no. of row in matrix
    - ncol [int]: no. of col in matrix

    Returns:
    - max no. of spikes [int]
    '''
    mask, shapes = generateMask(mat, nrow, ncol)
    maxSpike = 0

    visited = [
        [False] * ncol
        for _ in range(nrow)
    ]

    def neighbors(row, col):
        if row > 0 and mat[row - 1][col]:
            yield (row - 1, col)

        if col > 0 and mat[row][col - 1]:
            yield (row, col - 1)

        if row < nrow - 1 and mat[row + 1][col]:
            yield (row + 1, col)

        if col < ncol - 1 and mat[row][col + 1]:
            yield (row, col + 1)

    for point in shapes:
        stack = [point]
        nspike = 0

        while stack:
            point = stack.pop()
            proximity = list(neighbors(point[0], point[1]))
            visited[point[0]][point[1]] = True

            if len(proximity) == 1:
                nspike += 1

            for row, col in proximity:
                if not visited[row][col]:
                    stack.append((row, col))

        maxSpike = max(maxSpike, nspike)

    return maxSpike
    
