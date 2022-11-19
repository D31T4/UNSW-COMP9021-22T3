from base_conversion import bin2dec, dec2bin

def bin2decTest():
    '''
    unit test for bin2dec
    '''
    assert bin2dec([0][::-1]) == 0
    assert bin2dec([0, 0][::-1]) == 0

    assert bin2dec([1][::-1]) == 1
    assert bin2dec([1, 0][::-1]) == 2

def dec2binTest():
    '''
    unit test for dec2bin
    '''
    assert tuple(dec2bin(0)) == tuple([0][::-1])
    assert tuple(dec2bin(1)) == tuple([1][::-1])

    assert tuple(dec2bin(2)) == tuple([1, 0][::-1])


if __name__ == '__main__':
    print('Begin unit test for base_conversion.py...')
    bin2decTest()
    dec2binTest()
    print('All tests passed!')
