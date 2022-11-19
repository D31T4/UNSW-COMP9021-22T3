from encode import encode, decode
from test_helper import shouldRaise

def encodeTest():
    '''
    unit test of encode

    test cases extracted from quiz_4.pdf
    '''
    assert encode([1]) == 3
    assert encode([4891]) == 51315663
    assert encode([11, 24]) == 424896
    assert encode([10, 20, 30]) == 857310204
    assert encode([2, 4, 8, 16, 32]) == 13609683913728

def decodeTest():
    '''
    unit test of decode

    test cases extracted from quiz_4.pdf
    '''
    assert tuple(decode(3)) == tuple([1])
    assert tuple(decode(51315663)) == tuple([4891])
    assert tuple(decode(424896)) == (11, 24)
    assert tuple(decode(857310204)) == (10, 20, 30)
    assert tuple(decode(13609683913728)) == (2, 4, 8, 16, 32)

    assert shouldRaise(lambda: decode(1))
    assert shouldRaise(lambda: decode(5))
    assert shouldRaise(lambda: decode(7))
    assert shouldRaise(lambda: decode(24))
    assert shouldRaise(lambda: decode(12345))

if __name__ == '__main__':
    print('Begin unit test on encode.py...')
    encodeTest()
    decodeTest()
    print('All tests passed!')
