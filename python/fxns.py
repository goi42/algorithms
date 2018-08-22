def invmass(*args):
    '''returns a string representing the invariant mass of an arbitrary number of strings in C++ by using '_PE', '_PX', '_PY', '_PZ' (or 'P_E' if 'TRUE' in the name)
    '''
    kvars = ('_PE', '_PX', '_PY', '_PZ')
    outstr = 'sqrt('
    for ikv, kv in enumerate(kvars):
        outstr += 'pow('
        for i, p in enumerate(args):
            if 'TRUE' in p:
                use_kv = kv.replace('_P', 'P_')
            else:
                use_kv = kv
            outstr += p + use_kv
            if not i == len(args) - 1:
                outstr += ' + '
        outstr += ', 2)'
        if not ikv == len(kvars) - 1:
            outstr += ' - '
    outstr += ')'
    return outstr


def declength(nm):
    '''returns a string representing the decay length of the given parameter name in C++ by finding the length of the vector between ORIGINVERTEX and ENDVERTEX. Be sure to include '_TRUE' in nm if using truth value.
    '''
    varname = nm if 'TRUE' in nm else nm + '_'
    return 'sqrt(pow({VARNAME}ENDVERTEX_X - {VARNAME}ORIGINVERTEX_X, 2) + pow({VARNAME}ENDVERTEX_Y - {VARNAME}ORIGINVERTEX_Y, 2) + pow({VARNAME}ENDVERTEX_Z - {VARNAME}ORIGINVERTEX_Z, 2))'.format(VARNAME=varname)


def replE(ps, ms, *args):
    '''replaces one mass hypothesis with another by recalculating the energy with the presumed mass
    returns an invariant mass string
    `ps` is a list of particles
    `ms` is a list of their desired mass hypotheses
    args are the names of other particles to include in the invariant mass
    '''
    assert type(ps) == list and type(ms) == list and len(ps) == len(ms)
    kvars = ('_PX', '_PY', '_PZ')
    parts = ps + list(args)
    outstr = 'sqrt(pow('
    for i, (p, m) in enumerate(zip(ps, ms)):
        outstr += 'sqrt({M} * {M} + {PART}_P * {PART}_P)'.format(M=m, PART=p)
        if not i == len(ps) - 1:
            outstr += ' + '
    for p in args:
        outstr += ' + {}_PE'.format(p)
    outstr += ', 2)'
    for ikv, kv in enumerate(kvars):
        outstr += ' - pow('
        for i, p in enumerate(parts):
            outstr += p + kv
            if not i == len(parts) - 1:
                outstr += ' + '
        outstr += ', 2)'
    outstr += ')'
    return outstr


def shim_thickness(start, stop, subtract):
    ''' sums from start to stop (inclusive) and subtracts subtract
    start, stop, subtract, and output given in thousandths of an inch (no fractions)
    '''
    assert stop > start
    out_value = 0
    for i in xrange(start, stop + 1):
        out_value += i
    out_value -= subtract
    return out_value
    

def print_thicknesses(*args):
    '''prints table of thicknesses (calculated using `shim_thickness`) ready for emailing.
    enter side A, then side C measurements for as many positions as you like, e.g.,
    `start1A, stop1A, subtract1A, start1C, stop1C, subtract1C, start2A, stop2A, subtract2A, start2C, stop2C, subtract2C`
    and so on.
    '''
    assert len(args) % 2 == 0 and len(args) % 3 == 0 and all(isinstance(x, int) for x in args)

    for irowt, ((Astart, Astop, Asubtract), (Cstart, Cstop, Csubtract)) in enumerate(zip(*[iter(zip(*[iter(args)] * 3))] * 2)):  # split and loop over undifferentiated argument list
        irow = irowt + 1
        print 'A{}:'.format(irow), shim_thickness(Astart, Astop, Asubtract), '\tC{}:'.format(irow), shim_thickness(Cstart, Cstop, Csubtract)


def randmoney(hival=10.00, loval=1.00):
    '''returns random monetary value (string)
    loval <= output < hival
    '''
    from random import randrange
    hi, lo = hival * 100, loval * 100
    v = randrange(lo, hi, 1)
    return '${}'.format(round(float(v) / 100, 2))  # float and round to make sure


def divsquare(num):
    '''returns rows, columns
    '''
    import math
    sqnc = math.sqrt(num)
    sqncu = int(math.ceil(sqnc))
    sqncd = int(math.floor(sqnc))
    while(sqncu * sqncd < num):
        sqncu += 1
    return sqncu, sqncd


def makedirsif(adir):
    '''makes directory tree if it doesn't already exist
    '''
    try:
        os.makedirs(adir)
    except OSError as e:
        if '[Errno 17]' in str(e):
            pass


def getRTDtemp(R, R0=100.0, T0=0.0, a=3.9083E-3, b=-5.7750E-7):
    ''' Return temperature in Celcius given an RTD's resistance in Ohms. Uses formula R = R0*(1+a*(T-T0)+b*(T-T0)**2). Only valid for T>=0.
    Originally based on email from Ivan:
    The RTD's in sub-basement lab are standard Pt100 ones. Their resistance depends on temperature as R = R0*(1+a*(T-T0)), where T0 = 0C, R0 = 100 Ohm, a = 0.00385 1/C.
    modified for greater precision according to the equation at https://techoverflow.net/2016/01/02/accurate-calculation-of-pt100pt1000-temperature-from-resistance/
    '''
    from math import sqrt
    T = T0 + (sqrt(a**2 + 4 * b * (R / R0 - 1)) - a) / (2 * b)
    if T < 0:
        raise ValueError('negative T calculated: T = {}. Formula not valid for T < 0.'.format(T))
    return T


def getRTDres(T, R0=100.0, T0=0.0, a=3.9083E-3, b=-5.7750E-7, c=None):
    ''' Return resistance in ohms an RTD should have for a given temperature in Celcius. Uses formula R = R0*(1+a*(T-T0)+b*(T-T0)**2+c*(T-T0-100)*(T-T0)**3).
    Careful assigning c. Calculated internally if not assigned. T-dependent in calculation (0 for T>=0).
    Originally based on email from Ivan:
    The RTD's in sub-basement lab are standard Pt100 ones. Their resistance depends on temperature as R = R0*(1+a*(T-T0)), where T0 = 0C, R0 = 100 Ohm, a = 0.00385 1/C.
    modified for greater precision according to the equation at https://techoverflow.net/2016/01/02/accurate-calculation-of-pt100pt1000-temperature-from-resistance/
    '''
    if c is None:
        c = 0 if T >= 0 else -4.1830E-12
    R = R0 * (1 + a * (T - T0) + b * (T - T0)**2 + c * (T - T0 - 100) * (T - T0)**3)
    return R
