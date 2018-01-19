from cut import *
from ROOT import TCut


class bfch:  # abstract base class for branch and fch classes
    def __init__(self, c=None):
        self.c = []  # cuts to be applied
        if c:
            if isinstance(c, list) and all(isinstance(x, cut) for x in c):
                self.c = c
            else:
                raise TypeError('passed a ' + c.__class__.__name__ + ' as "c" instead of a list.')

    def add_cut(self, *args, **kwargs):
        if isinstance(args[0], cut):
            if len(args) == 1 and len(kwargs) == 0:  # if it's just one cut
                self.c.append(*args)  # just add it
            elif len(args) == 2 and isinstance(args[1], str):  # if it's a cut and a string
                self.add_cut(args[0].cut, args[1])  # add the cut and rename it
            elif all(isinstance(x, cut) for x in args):  # if it's a bunch of cuts
                self.c.extend(args)  # just add them
            else:
                raise TypeError
        elif all(isinstance(x, list) for x in args):  # if it's a list (or lists)
            for ar in args:
                if all(isinstance(x, cut) for x in ar):  # of cuts, add them
                    self.c.extend(ar)
                elif all(isinstance(x, (str, TCut)) for x in ar):  # of strings or TCuts
                    for ct in ar:
                        self.add_cut(ct)  # add_cut each of them
                else:
                    raise TypeError
        else:
            self.c.append(cut(*args, **kwargs))  # create new cut, append it
