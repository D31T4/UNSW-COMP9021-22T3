
def bin2dec(digits):
    '''
    convert a stream of bits into an integer

    Arguments:
    - digits [(1 | 0)[]]: binary stream

    Return:
    - integer [int]
    '''
    num = 0
    
    for i, d in enumerate(digits):
        num += d * (2 ** i)

    return num

def dec2bin(num):
    '''
    convert an integer into a binary stream

    Arguments:
    - num [int]

    Yields:
    - bit [1 | 0]
    '''
    if num == 0:
        yield 0
        return

    while num > 0:
        num, rem = divmod(num, 2)
        yield rem
