def shouldRaise(f):
    '''
    test if f raises an error

    copied from my quiz 3 code

    Arguments:
    - f [() => any]

    Returns:
    - f raised any error [bool]
    '''
    try:
        f()
        return False
    except:
        return True
