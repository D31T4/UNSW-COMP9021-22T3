def exceptionRaised(f):
    '''
    Arguments:
    - f: function to be tested

    Returns:
    `True` if an exception is raised; `False` otherwise
    '''
    try:
        f()
        return False
    except:
        return True
