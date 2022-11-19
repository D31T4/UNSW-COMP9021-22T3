
class Tokens:
    '''
    static class for tokens
    '''
    # open parentheses
    OpenParen = '('
    # close parentheses
    CloseParen = ')'
    # comma
    Comma = ','

    def isSymbol(token):
        return token != Tokens.OpenParen and token != Tokens.CloseParen and token != Tokens.Comma

def tokenize(string):
    '''
    split the string into tokens

    Arguments:
    - string [string]

    Returns:
    - tokens [string[]]

    Raises:
    - ValueError: if string has invalid grammar
    '''
    string = string.strip()

    tokens = []

    N = len(string)
    i = 0

    while i < N:
        if not Tokens.isSymbol(string[i]):
            tokens.append(string[i])
            i += 1
        elif string[i] == ' ':
            i += 1
        elif isValidChar(string[i]):
            j = i

            while j < N and isValidChar(string[j]):
                j += 1

            tokens.append(string[i:j])
            i = j
        else:
            raise ValueError('invalid symbol')

    return tokens
            

def isValidChar(char):
    '''
    checks if char is valid

    Arguments:
    - char [char]

    Returns:
    - char is valid [bool]
    '''
    if char == '_':
        return True

    order = ord(char)

    return (65 <= order and order <= 90) or (97 <= order and order <= 122)

