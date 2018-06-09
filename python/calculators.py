def shim_thickness(start, stop, subtract):
    ''' sums from start to stop (inclusive) and subtracts subtract
    start, stop, subtract, and output given in thousandths of an inch (no fractions)
    '''
    out_value = 0
    for i in xrange(start, stop + 1):
        out_value += i
    out_value -= subtract
    return out_value
