import os
import filecmp
from maze import Maze, maze_to_tex

def test(fname):
    '''
    test file

    Arguments:
    - fname [string]

    Returns:
    - comparison [bool]: `True` if file content is as expected; otherwise `False`
    '''
    m = Maze(f'input_samples/{fname}.txt')
    output_path = f'output_samples/{fname}.test.tex'

    maze_to_tex(m, output_path)

    # file compare
    result = filecmp.cmp(f'output_samples/expected_{fname}.tex', output_path)

    if result: os.remove(output_path)
    return result

def maze_to_texTest():
    '''
    unit test for maze_to_tex(...)

    test files extracted from default scaffold and `more examples.zip`
    '''
    assert test('maze_1')
    assert test('maze_2')
    assert test('labyrinth')

    assert test('example1')
    assert test('example2')
    assert test('example3')
    assert test('example4')

    assert test('BiggestMaze')

    assert test('house')

def mazeDisplayTest():
    '''
    unit test for Maze.display(...)
    '''
    Maze('input_samples/maze_1.txt').display()
    assert filecmp.cmp('maze_1.tex', 'output_samples/expected_maze_1.tex')
    os.remove('maze_1.tex')

    Maze('input_samples/maze_2.txt').display()
    assert filecmp.cmp('maze_2.tex', 'output_samples/expected_maze_2.tex')
    os.remove('maze_2.tex')

    Maze('input_samples/labyrinth.txt').display()
    assert filecmp.cmp('labyrinth.tex', 'output_samples/expected_labyrinth.tex')
    os.remove('labyrinth.tex')

if __name__ == '__main__':
    print('begin unit test for maze_to_tex.py...')
    maze_to_texTest()
    mazeDisplayTest()
    print('all tests passed!')
