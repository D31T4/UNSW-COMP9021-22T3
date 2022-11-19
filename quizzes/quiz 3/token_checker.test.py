from tokenize import tokenize
from token_checker import TokenChecker, stringIsValid

def TokenCheckerTest():
    '''
    unit test for TokenChecker.
    '''
    assert not TokenChecker(tokenize(''), 0).isValid()
    assert not TokenChecker(tokenize('f()'), 0).isValid()

    assert TokenChecker(tokenize('asd'), 0).isValid()
    assert not TokenChecker(tokenize('asd'), 3).isValid()

    assert TokenChecker(tokenize('f(xd)'), 1).isValid()
    assert TokenChecker(tokenize('f(x, g(i, j))'), 2).isValid()

    assert not TokenChecker(tokenize('f(x, y)'), 1).isValid()

    assert not TokenChecker(tokenize('f)'), 0).isValid()
    assert not TokenChecker(tokenize('f(x)()'), 1).isValid()
    assert not TokenChecker(tokenize('f(x))'), 1).isValid()
    assert not TokenChecker(tokenize('f(x)('), 1).isValid()
    assert not TokenChecker(tokenize('(f(x))'), 1).isValid()

def stringIsValidTest():
    '''
    unit test of stringIsValid

    test cases extracted from quiz_3.pdf and relevant ed forum posts
    '''
    assert not stringIsValid('f_1', 0)
    assert not stringIsValid('()', 0)
    assert not stringIsValid('function_of_arity_one(hello)', 0)
    assert not stringIsValid('f)', 0)
    assert not stringIsValid('f[a]', 1)
    
    assert not stringIsValid('f(a, g(b))', 2)
    assert not stringIsValid('constant', 3)
    assert not stringIsValid('f((a, b, c))', 3)
    assert not stringIsValid('f(g(a, a), f(a, b))', 3)
    assert not stringIsValid('f(g(a,b,c),g(a,b,c),g(a,b,c)', 3)
    assert not stringIsValid('f(a, g(a, b, f(a,b,c)), b, c)', 3)

    assert stringIsValid('a', 0)
    assert stringIsValid('function_of_arity_one(hello)', 1)
    assert stringIsValid('F(g(a, a), f(a, b))', 2)
    assert stringIsValid('ff(ff(ff(a,b,ff(aa,bb,cc)) , b , ff(a,b,c)) , b , ff(a,ff(a,b,c),c))', 3)
    assert stringIsValid('f(a, FF(a, b, fff(a, b, c, FfFf(a,b,c,d)), FfFf(a,b,c,d)), c, d)', 4)

    assert not stringIsValid('f()', 0)
    assert not stringIsValid('f()', 1)
    assert stringIsValid('f', 0)
    assert stringIsValid('f(x)', 1)

    assert stringIsValid('               a               ', 0)
    assert stringIsValid('     f        (      a        )', 1)

    assert stringIsValid('f(f(f(f(x))))', 1)

if __name__ == '__main__':
    print('Begin unit test on TokenChecker.py')
    TokenCheckerTest()
    stringIsValidTest()
    print('All tests passed!')
