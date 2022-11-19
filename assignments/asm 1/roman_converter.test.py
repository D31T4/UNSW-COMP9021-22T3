from roman_converter import digits, DigitParser, GeneralizedRomanNumeral, RomanNumeral
import test_helper as th

'''
unit tests for romanconverter.py
'''

def digitsTest():
    '''
    unit test for `digits`
    '''
    assert all(i == digit for i, digit in enumerate(digits(6543210)))

def DigitParserTest():
    '''
    unit test for `DigitParser`
    '''
    dp = DigitParser(['I', 'V', 'X'])

    assert dp.toArab('') == None and dp.toRoman(0) == ''
    assert dp.toArab('I') == 1 and dp.toRoman(1) == 'I'
    assert dp.toArab('II') == 2 and dp.toRoman(2) == 'II'
    assert dp.toArab('III') == 3 and dp.toRoman(3) == 'III'
    assert dp.toArab('IV') == 4 and dp.toRoman(4) == 'IV'
    assert dp.toArab('V') == 5 and dp.toRoman(5) == 'V'
    assert dp.toArab('VI') == 6 and dp.toRoman(6) == 'VI'
    assert dp.toArab('VII') == 7 and dp.toRoman(7) == 'VII'
    assert dp.toArab('VIII') == 8 and dp.toRoman(8) == 'VIII'
    assert dp.toArab('IX') == 9 and dp.toRoman(9) == 'IX'

    assert dp.tryMatchRoman('XVIII') == 'VIII'
    assert dp.tryMatchRoman('XIII') == 'III'
    assert dp.tryMatchRoman('IX') == 'IX'
    assert dp.tryMatchRoman('IV') == 'IV'


def isValidNumeralTest():
    '''
    unit test for `GeneralizedRomanNumeral.isValidNumeral`
    '''
    assert GeneralizedRomanNumeral.isValidNumeral('ABCDE')
    assert not GeneralizedRomanNumeral.isValidNumeral('_asd')
    assert not GeneralizedRomanNumeral.isValidNumeral('_')
    assert not GeneralizedRomanNumeral.isValidNumeral('AABCDE')

def GeneralizedRomanNumeralTest():
    '''
    unit test for `GeneralizedRomanNumeral`

    test cases extracted from `Assignment 1.pdf`
    '''
    assert RomanNumeral.toRoman(35) == 'XXXV'
    assert RomanNumeral.toRoman(1982) == 'MCMLXXXII'
    assert RomanNumeral.toRoman(3007) == 'MMMVII'

    assert RomanNumeral.toArab('MCMLXXXII') == 1982
    assert RomanNumeral.toArab('MMMVII') == 3007

    assert th.exceptionRaised(lambda: RomanNumeral.toArab('IIII'))
    assert th.exceptionRaised(lambda: RomanNumeral.toArab('IXI'))

    assert th.exceptionRaised(lambda : GeneralizedRomanNumeral('VI').toArab('XXXVI'))
    assert th.exceptionRaised(lambda : GeneralizedRomanNumeral('IVX').toArab('XXXVI'))
    assert th.exceptionRaised(lambda : GeneralizedRomanNumeral('XWVI').toArab('XXXVI'))

    assert GeneralizedRomanNumeral('XVI').toArab('XXXVI') == 36
    assert GeneralizedRomanNumeral('XABVI').toArab('XXXVI') == 306
    assert GeneralizedRomanNumeral('fFeEdDcCbBaA').toArab('EeDEBBBaA') == 49036
    assert GeneralizedRomanNumeral('AbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStT').toArab('ABCDEFGHIJKLMNOPQRST') == 11111111111111111111

    assert GeneralizedRomanNumeral('fFeEdDcCbBaA').toRoman(49036) == 'EeDEBBBaA'
    assert GeneralizedRomanNumeral('AaBbCcDdEeFfGgHhIiJjKkLl').toRoman(899999999999) == 'Aaaabacbdcedfegfhgihjikjlk'
    assert GeneralizedRomanNumeral('LAQMPVXYZIRSGN').toRoman(1900604) == 'AMAZING'

if __name__ == '__main__':
    print('----- Begin unit test on roman_converter.py -----')
    digitsTest()
    DigitParserTest()
    isValidNumeralTest()
    GeneralizedRomanNumeralTest()
    print('All tests passed!')
