import re

def digits(num):
    '''
    yield all digits of an integer from right to left

    Arguments
    - num: integer

    Yields:
    - digit: integer
    '''
    num = abs(int(num))

    if not num: yield 0

    while num:
        num, rem = divmod(num, 10)
        yield rem

class DigitParser:
    '''
    translates from and to generalized roman numeral based digit,
    and arabic digit
    '''

    def __init__(self, numerals):
        '''
        Arguments:
        - numerals: tuple with length 3, represents roman numerals for [1, 5, 10]
        '''
        self.numerals = numerals

    def tryMatchRoman(self, string):
        '''
        match roman digit from right of string greedily

        Arguments:
        - string: string to be matched

        Returns
        - roman digit if matched; otherwise None
        '''
        if self.numerals[2]:
            if string.endswith(self.numerals[0] + self.numerals[2]):
                return self.numerals[0] + self.numerals[2]

        if self.numerals[1]:
            if string.endswith(self.numerals[0] + self.numerals[1]):
                return self.numerals[0] + self.numerals[1]

            for i in [3, 2, 1, 0]:
                if string.endswith(self.numerals[1] + self.numerals[0] * i):
                    return self.numerals[1] + self.numerals[0] * i

        if self.numerals[0]:
            for i in [3, 2, 1]:
                if string.endswith(self.numerals[0] * i):
                    return self.numerals[0] * i

        return None

    def toArab(self, roman):
        '''
        convert roman digit to arabic digit

        Arguments
        - roman: roman digit in string

        Returns:
        - arab digit in int if matched; otherwise None
        '''
        # I, II, II
        if self.numerals[0]:
            for i in [1, 2, 3]:
                if roman == self.numerals[0] * i:
                    return i

        if self.numerals[1]:
            # IV
            if roman == self.numerals[0] + self.numerals[1]:
                return 4

            # V, VI, VII, VIII
            for i in range(4):
                if roman == self.numerals[1] + self.numerals[0] * i:
                    return i + 5

        if self.numerals[2]:
            # IX
            if roman == self.numerals[0] + self.numerals[2]:
                return 9

        return None

    def toRoman(self, arab):
        '''
        convert arab digit to roman digit

        Arguments
        - arab: arab digit in integer

        Returns:
        - roman digit if matched; otherwise None
        '''
        arab = abs(int(arab)) % 10

        if arab == 0:
            return ''
        # I, II, III
        elif arab >= 1 and arab <= 3 and self.numerals[0]:
            return self.numerals[0] * arab
        # IV
        elif arab == 4 and self.numerals[1]:
            return self.numerals[0] + self.numerals[1]
        # V, VI, VII, VIII
        elif arab >= 5 and arab <= 8 and self.numerals[1]:
            return self.numerals[1] + (arab - 5) * self.numerals[0]
        # IX
        elif arab == 9 and self.numerals[2]:
            return self.numerals[0] + self.numerals[2]

        return None

class GeneralizedRomanNumeral:
    '''
    generalized roman numeral system

    where:
    the right-most char represents 1e0
    2nd right-most char represents 5e0
    3rd right-most char represents 1e1
    and so on...
    '''

    def isValidNumeral(numerals):
        '''
        check whether the string is a valid set of generalized roman numerals:
        1. each char must be unique
        2. each char must be a lower/upper case alphabet
        '''
        if not numerals:
            return False

        chars = set()

        for char in numerals:
            if not re.match(r'^[a-zA-Z]$', char):
                return False

            charCode = ord(char)

            if charCode in chars:
                return False
            
            chars.add(charCode)

        return True

    def __init__(self, numerals):
        '''
        create a generalized roman numeral
        '''
        assert GeneralizedRomanNumeral.isValidNumeral(numerals)
        self.numerals = numerals[::-1]

    def getNthOrderNumerals(self, n):
        '''
        get numerals representing 1eN, 5eN, 1e(N+1).

        Arguments:
        - n [int]: N

        Returns
        tuple of symbols of length 3. will use `None` to represent missing symbols.
        '''
        start = n * 2
        numerals = list(self.numerals[start:(start + 3)])

        # use `None` to represent missing symbols
        numerals += [None] * (3 - len(numerals))

        return tuple(numerals)

    def toArab(self, roman):
        '''
        convert roman string to int

        Arguments:
        - roman: roman number in string
        '''
        assert len(set(roman)) == len(set(roman) & set(self.numerals))

        num = 0

        index = len(roman) - 1

        order = 0
        MAX_ORDER = len(self.numerals) // 2

        while index >= 0:
            assert order <= MAX_ORDER

            chunk = roman[max(0, index - 4):(index + 1)]

            t = DigitParser(self.getNthOrderNumerals(order))
            romanDigit = t.tryMatchRoman(chunk)

            if romanDigit:
                num += t.toArab(romanDigit) * (10 ** order)
                index -= len(romanDigit)

            order += 1

        return num

    def toRoman(self, num):
        '''
        convert an integer to the specificed roman numeral

        Arguments
        - num: integer
        '''
        num = abs(int(num))

        roman = ''

        for order, digit in enumerate(digits(num)):
            t = DigitParser(self.getNthOrderNumerals(order))
            romanDigit = t.toRoman(digit)

            if romanDigit == None:
                raise ValueError('Out of bound')

            roman = t.toRoman(digit) + roman

        return roman

# standard roman numeral
RomanNumeral = GeneralizedRomanNumeral('MDCLXVI')
