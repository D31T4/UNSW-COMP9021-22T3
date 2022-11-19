def shouldRaise(f):
    '''
    test if f raises an error

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
