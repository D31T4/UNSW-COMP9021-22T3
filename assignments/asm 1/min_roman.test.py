from min_roman import SymbolProposalEntry, SymbolProposal, minimalArab
from test_helper import exceptionRaised

def SymbolProposalEntryTest():
    e = SymbolProposalEntry('A', 10)
    assert e.symbol == 'A'
    assert e.value == 10
    assert e.count == 1

def SymbolProposalTest():
    def generateGuessesTest():
        p = SymbolProposal()

        p.tryPropose('I', 1)
        
        for g in p.generateGuesses('IX', 0):
            print(g, p.getValue('X'))

    def renderProposalTest():
        p = SymbolProposal()
        p.tryPropose('I', 1)
        p.tryPropose('V', 5)
        p.tryPropose('X', 10)
        p.tryPropose('L', 50)
        p.tryPropose('C', 100)
        p.tryPropose('D', 500)
        p.tryPropose('M', 1000)

        assert p.renderProposal() == 'MDCLXVI'

    def proposeWithdrawTest():
        p = SymbolProposal()

        assert p.tryPropose('A', 1)
        assert p.getValue('A') == 1
        assert p.tryPropose('B', 5)

        assert not p.tryPropose('A', 10)


    #generateGuessesTest()
    renderProposalTest()
    proposeWithdrawTest()

def minimalArabTest():
    '''
    unit test for `minimalArab`

    test cases extracted from `Assignment 1.pdf`
    '''
    assert exceptionRaised(lambda: minimalArab('0I'))
    assert exceptionRaised(lambda: minimalArab('ABAA'))
    assert exceptionRaised(lambda: minimalArab('ABCDEFA'))

    arab, numerals = minimalArab('MDCCLXXXVII')
    assert arab == 1787 and numerals == 'MDCLXVI'

    arab, numerals = minimalArab('MDCCLXXXIX')
    assert arab == 1789 and numerals == 'MDCLX_I'

    arab, numerals = minimalArab('MMMVII')
    assert arab == 37 and numerals == 'MVI'

    arab, numerals = minimalArab('VI')
    assert arab == 4 and numerals == 'IV'

    arab, numerals = minimalArab('ABCADDEFGF')
    assert arab == 49269 and numerals == 'BA_C_DEF_G'

    arab, numerals = minimalArab('ABCCDED')
    assert arab == 1719 and numerals == 'ABC_D_E'

    arab, numerals = minimalArab('AZERTY')
    assert arab == 444 and numerals == 'ZAREYT'

    arab, numerals = minimalArab('XXXVVVIII')
    assert arab == 333 and numerals == 'X_V_I'

    arab, numerals = minimalArab('AhZhJ')
    assert arab == 691 and numerals == 'Ah_Z_J'

    assert exceptionRaised(lambda: minimalArab('BCBC'))

if __name__ == '__main__':
    print('----- Begin unit test for min_roman.py -----')
    SymbolProposalEntryTest()
    SymbolProposalTest()
    minimalArabTest()
    print('All tests passed!')
