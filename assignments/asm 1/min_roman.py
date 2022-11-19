import re
from roman_converter import DigitParser, GeneralizedRomanNumeral

class UnsafeGeneralizedRomanNumeral(GeneralizedRomanNumeral):
    '''
    generalized roman numerals without validation at ctor.

    used for `minimalArab` because the generated set of numerals can contain missing symbols
    '''
    def __init__(self, numerals):
        '''
        override parent ctor to skip numerals checking
        '''
        self.numerals = numerals[::-1]

class SymbolProposalEntry:
    '''
    Entry in `SymbolProposal.charTable`

    Properties
    - symbol [char]:
    - value [int]: value of symbol
    - count [int]: count of proposed times. we use this for recursive propositions
    '''
    def __init__(self, symbol, value):
        self.symbol = symbol
        self.value = abs(int(value))
        self.count = 1

class SymbolProposal:
    '''
    Proposed symbols for a generalized roman numeral system

    Properties:
    - charTable:
        an enum table for symbols, maps { symbol } U { value } to entry
    '''
    def __init__(self):
        self.charTable = dict()

    def renderProposal(self):
        '''
        render the set of proposed symbol into a string,
        missing symbols will be replaced with the placeholder '_'.
        '''
        currentValue = 1
        MAX_VALUE = max([v.value for v in self.charTable.values()])

        step = 5

        string = ''

        while currentValue <= MAX_VALUE:
            if currentValue in self.charTable:
                string = self.charTable[currentValue].symbol + string
            else:
                string = '_' + string

            currentValue *= step
            step = 5 if step != 5 else 2

        return string

    def tryPropose(self, symbol, value):
        '''
        attempt to propose a symbol to have the specified value

        Arguments:
        - symbol [char]:
        - value [int]:

        Returns
        `True` if attempt is successful; otherwise `False`
        '''
        # conflicted proposition: same symbol represents 2 different values
        if symbol in self.charTable and self.charTable[symbol].value != value:
            return False

        # conflicted proposition: same value is represented by 2 diferent symbols
        if value in self.charTable and self.charTable[value].symbol != symbol:
            return False

        if symbol in self.charTable:
            e = self.charTable[symbol]
            e.count += 1
        else:
            e = SymbolProposalEntry(symbol, value)
            self.charTable[value] = e
            self.charTable[symbol] = e

        return True

    def withdraw(self, symbol):
        '''
        withdraw a symbol proposal

        Arguments
        - symbol [char]:
        '''
        if symbol not in self.charTable: return

        e = self.charTable[symbol]
        e.count -= 1

        if not e.count:
            del self.charTable[symbol]
            del self.charTable[e.value]

    def getValue(self, symbol):
        '''
        get proposed value of a proposed symbol

        Arguments:
        - symbol [char]: proposed symbol

        Returns:
        proposed value of proposed symbol
        '''
        return self.charTable[symbol].value

    def generateGuesses(self, string, currentOrder):
        '''
        generate greedy guesses that is *locally correct*:
        - take smallest digit first
        - take as many chars as possible

        Arguments:
        - string [string]: input string. will only check the last 4 chars.
        - currentOrder [int]: order of the guessed digit
        '''
        n = len(string)
        if n == 0: return

        ch0 = string[-1]

        # invalid
        if string.endswith(ch0 * 4):
            return

        # yield guesses between [VII, VIII] and [II, III]
        # since only I can be repeated, we can use this to reduce the search space
        if ch0 not in self.charTable or self.getValue(ch0) == 10 ** currentOrder:
            for i in [3, 2]:
                if not string.endswith(ch0 * i):
                    continue

                if not self.tryPropose(ch0, 10 ** currentOrder):
                    break

                if i < n:
                    ch1 = string[-(i + 1)]

                    if self.tryPropose(ch1, 5 * 10 ** currentOrder):
                        yield ch1 + ch0 * i
                        self.withdraw(ch1)

                yield ch0 * i
                self.withdraw(ch0)
                break
        
        # yield greedy guesses in { IV, VI, IX }
        # i.e. in ascending order of digit value
        if n >= 2 and ch0 != string[-2]:
            ch1 = string[-2]

            # IV
            if self.tryPropose(ch0, 5 * 10 ** currentOrder):
                if self.tryPropose(ch1, 10 ** currentOrder):
                    yield ch1 + ch0
                    self.withdraw(ch1)

                self.withdraw(ch0)

            # VI
            if self.tryPropose(ch0, 10 ** currentOrder):
                if self.tryPropose(ch1, 5 * 10 ** currentOrder):
                    yield ch1 + ch0
                    self.withdraw(ch1)

                self.withdraw(ch0)

            # IX
            if self.tryPropose(ch0, 10 ** (currentOrder + 1)):
                if self.tryPropose(ch1, 10 ** currentOrder):
                    yield ch1 + ch0
                    self.withdraw(ch1)

                self.withdraw(ch0)

        # I, V
        # again, greedy guesses
        if (n == 1) or (n >= 2 and ch0 != string[-2]):
            # I
            if self.tryPropose(ch0, 10 ** currentOrder):
                yield ch0
                self.withdraw(ch0)

            # V
            if self.tryPropose(ch0, 5 * 10 ** currentOrder):
                yield ch0
                self.withdraw(ch0)


def minimalArab(string):
    '''
    search a set of generalized roman numerals such that:
    the arab conversion of the input string is minimum

    Arguments:
    - string [string]: input string

    Returns:
    - value [int]: arab conversion
    - numerals [string]: set of numerals. '_' represents missing symbols.

    Raises:
    - `ValueError` if no feasible solution is found
    '''
    # alphabet test
    assert re.match('^[a-zA-Z]+$', string)

    p = SymbolProposal()

    if __minimalArab(string, len(string) - 1, 0, p):
        numerals = p.renderProposal()
        MyNumeral = UnsafeGeneralizedRomanNumeral(numerals)
        return (MyNumeral.toArab(string), numerals)
    else:
        raise ValueError('Invalid roman numerals')

def __minimalArab(string, currentIndex, currentOrder, proposedSymbols):
    '''
    search for a solution recursively

    Arguments:
    - string [string]: input string
    - currentIndex [int]: current index in input string reached
    - currentOrder [int]: recursion depth
    - proposedSymbols [SymbolProposal]: set of proposed symbols

    Returns
    `True` if a solution is found; otherwise `False`
    '''
    for digit in proposedSymbols.generateGuesses(string[max(0, currentIndex - 4):(currentIndex + 1)], currentOrder):
        # end of string reached. success!
        if currentIndex - len(digit) < 0:
            return True

        # solution found by a child search task
        if __minimalArab(string, currentIndex - len(digit), currentOrder + 1, proposedSymbols):
            return True

    return False

