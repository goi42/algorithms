def invmass(*args):
    '''returns the invariant mass of an arbitrary number of strings by using '_PE', '_PX', '_PY', '_PZ' (or 'P_E' if 'TRUE in the name')
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


def replE(ps, ms, *args):
    '''replaces one mass hypothesis with another by recalculating the energy with the presumed mass
    `ps` is a list of particles
    `ms` is a list their desired mass hypotheses
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
