def catch(f):
    try:
        f()
        return None
    except Exception as e:
        return e

def flatmap(seq):
    for arr in seq:
        for el in arr:
            yield el
