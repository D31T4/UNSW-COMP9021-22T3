from tokenize import isValidChar, tokenize
from test_helper import shouldRaise

def isValidCharTest():
    '''
    unit test for isValidChar
    '''
    assert isValidChar('_')
    assert isValidChar('A')
    assert isValidChar('a')
    
    assert not isValidChar('1')
    assert not isValidChar(' ')

def tokenizeTest():
    '''
    unit test for tokenize
    '''
    assert tuple(tokenize('asd')) == tuple(['asd'])
    assert tuple(tokenize('g f')) == ('g', 'f')
    assert tuple(tokenize('f()')) == ('f', '(', ')')
    assert tuple(tokenize('func(sd(x), y)')) == ('func', '(', 'sd', '(', 'x', ')', ',', 'y', ')')
    assert tuple(tokenize(' f( x )')) == ('f', '(', 'x', ')')

    assert shouldRaise(lambda: tokenize('f123'))

    assert len(tokenize('')) == 0

if __name__ == '__main__':
    print('Begin unit test on tokenize.py')
    isValidCharTest()
    tokenizeTest()
    print('All tests passed!')

