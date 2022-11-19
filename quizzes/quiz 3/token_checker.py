from tokenize import Tokens, tokenize

class TokenChecker:
    '''
    token checker
    '''
    def __init__(self, tokens, arity):
        '''
        Arguments:
        - tokens [string[]]
        - arity [int]
        '''
        self.tokens = list(tokens)
        self.arity = arity

    def readToken(self):
        '''
        read current token

        Returns:
        - current token [string | None]
        '''
        if 0 <= self.currentIndex and self.currentIndex < len(self.tokens):
            return self.tokens[self.currentIndex]
        else:
            return None

    def reset(self):
        '''
        reset currentIndex to 0
        '''
        self.currentIndex = 0

    def consume(self):
        '''
        consume the current token
        '''
        self.currentIndex += 1

    def isValid(self):
        '''
        checks the set of token is valid

        Returns:
        - is valid [bool]
        '''
        if len(self.tokens) == 0:
            return False

        self.reset()
        return self.validateExpression(True) and not self.readToken()

    def validateExpression(self, topLevel = False):
        '''
        validate expression recursively

        Arguments:
        - topLevel [bool]: is top-level. required for top-level grammar checks

        Returns:
        - expression is valid [bool]
        '''
        if not Tokens.isSymbol(self.readToken()):
            return False

        self.consume()

        if self.arity == 0:
            return True
        
        if not topLevel and self.readToken() != Tokens.OpenParen:
            return True

        self.consume()

        # no. of arguments in the expression
        n_args = 0

        while self.readToken() and self.readToken() != Tokens.CloseParen:
            if not self.validateExpression():
                return False

            n_args += 1

            if self.readToken() == Tokens.CloseParen:
                break

            if self.readToken() != Tokens.Comma:
                return False

            self.consume()

        if n_args != self.arity:
            return False

        if self.readToken() != Tokens.CloseParen:
            return False

        self.consume()
        return True
        
def stringIsValid(string, arity):
    '''
    checks whether input string is valid

    Arguments:
    - string [string]
    - arity [int]

    Returns:
    - string is valid [bool]
    '''
    try:
        tokens = tokenize(string)
        return TokenChecker(tokens, arity).isValid()
    except:
        return False

