import re

def parseUserInput(userInput):
    '''
    parse user input

    Arguments
    - userInput: user input string

    Returns
    - case number: 
        0 if don't get what you want; 
        1 for convert roman to arab
        2 for convert arab to roman
        3 for convert generalized roman to arab
        4 for convert arab to generalized roman
        5 for minimal roman
    - arg1: generalized roman string (case 1, 3, 5) or integer (case 2, 4)
    - arg2: generalized roman numerals (only for case 3, 4)
    '''
    m = re.match('^Please convert ([^\s-]+)$', userInput)
    if m:
        caseno = 2 if re.match('^\d+$', m.group(1)) else 1
        return (caseno, m.group(1))

    m = re.match('^Please convert ([^\s-]+) using ([^\s-]+)$', userInput)
    if m:
        caseno = 4 if re.match('^\d+$', m.group(1)) else 3
        return (caseno, m.group(1), m.group(2))

    m = re.match('^Please convert ([^\s-]+) minimally$', userInput)
    if m: return (5, m.group(1))

    return tuple([0])
