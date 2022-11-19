from base_conversion import dec2bin, bin2dec

def encode(nums):
    '''
    encode the list of integers into a single integer

    Arguments:
    - nums [int[]]

    Returns:
    - encoded value [int]
    '''
    def digitGenerator():
        '''
        stream the bits of the digit

        Yields:
        - bit [1 | 0]
        '''
        i = len(nums) - 1

        while i >= 0:
            # stream a element
            for d in dec2bin(nums[i]):
                yield d
                yield d

            # separator
            if i > 0:
                yield 0

            i -= 1

    return bin2dec(digitGenerator())

def decode(num):
    '''
    decode the integer into a list of integer

    Arguments:
    - num [int]

    Returns:
    - list [int[]]

    Raises:
    - ValueError: if num is not a valid encoding
    '''
    bits = list(dec2bin(num))[::-1]

    def readBits(i):
        '''
        read the i-th bit

        Arguments:
        - i [int]: index

        Returns:
        - i-th bit [1 | 0 | None]
        '''
        return bits[i] if 0 <= i and i < len(bits) else None

    l = []

    i = 0

    while True:
        j = i

        # read a element
        while readBits(j) != None and readBits(j) == readBits(j + 1):
            j += 2

        # ensure something is read
        if j != i:
            # convert chunk to int
            l.append(bin2dec(bits[i:j:2][::-1]))
            i = j

        if i < len(bits):
            # read separator
            if readBits(i) == 0 and readBits(i + 1) == 1:
                i += 1
                continue

            raise ValueError('invalid encoding')
        else:
            break

    return l

