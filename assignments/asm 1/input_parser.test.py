from input_parser import parseUserInput

def parseUserInputTest():
    '''
    unit test of `parseUserInput`

    test cases extracted from `Assignment 1.pdf`
    '''
    args = parseUserInput('Please do my assignment...')
    assert args[0] == 0

    args = parseUserInput('please convert 35')
    assert args[0] == 0

    args = parseUserInput('Please convert 035')
    assert args[0] == 2 and args[1] == '035'

    args = parseUserInput('Please convert 4000')
    assert args[0] == 2 and args[1] == '4000'

    args = parseUserInput('Please convert IIII')
    assert args[0] == 1 and args[1] == 'IIII'

    args = parseUserInput('Please convert 123 by using ABC')
    assert args[0] == 0

    args = parseUserInput('Please convert 123 ussing ABC')
    assert args[0] == 0

    args = parseUserInput('Please convert _ using _')
    assert args[0] == 3 and args[1] == '_' and args[2] == '_'

    args = parseUserInput('Please convert XXXVI using XABVI')
    assert args[0] == 3 and args[1] == 'XXXVI' and args[2] == 'XABVI'

    args = parseUserInput('Please convert 49036 using fFeEdDcCbBaA')
    assert args[0] == 4 and args[1] == '49036' and args[2] == 'fFeEdDcCbBaA'

    args = parseUserInput('Please convert ABCD minimally using ABCDE')
    assert args[0] == 0

    args = parseUserInput('Please convert ABCD minimaly')
    assert args[0] == 0

    args = parseUserInput('Please convert MDCCLXXXVII minimally')
    assert args[0] == 5 and args[1] == 'MDCCLXXXVII'

if __name__ == '__main__':
    print('----- Begin unit test on input_parser.py -----')
    parseUserInputTest()
    print('All tests passed!')
