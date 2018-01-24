from ROOT import TCut


class cut:
    def __init__(self, cut, name=None):
        self.cut = TCut(cut)
        self.name = str(cut)
        if name:
            self.name = str(name)
        # deprecated:
        self.csig = ""  # the cut in addition to self that produces nsig
        self.cbkg = ""  # the cut in addition to self that produces nbkg
        self.nsig = 0
        self.nbkg = 0
        self.nL = 0
        self.nS = 0
        self.nb = 0

    def __getattr__(self, name):
        return getattr(self.cut, name)

    def _arithmetic(self, sym, another):
        if another.__class__.__name__ == self.__class__.__name__:
            ancut = another.cut.GetTitle()
            anname = another.name
        elif another.__class__.__name__ == 'str':
            ancut = another
            anname = another
        elif another.__class__.__name__ == 'TCut':
            ancut = another.GetTitle()
            anname = another.GetName()
        else:
            raise TypeError('cannot add object of class "' + another.__class__.__name__ + '" to object of class "cut"')

        newcut = '(' + self.cut.GetTitle() + ')' + sym + '(' + ancut + ')'
        newname = '(' + self.name + ') ' + sym + ' (' + anname + ')'

        return newcut, newname, ancut, anname

    def __add__(self, another):
        newcut, newname, ancut, anname = self._arithmetic('&&', another)
        if not self.cut.GetTitle().strip():
            newcut = ancut
            if not self.name.strip():
                newname = anname
        return cut(newcut, newname)

    def __sub__(self, another):
        newcut, newname, ancut, anname = self._arithmetic('&& !', another)
        if not self.cut.GetTitle().strip():
            newcut = '!(' + ancut + ')'
            if not self.name.strip():
                newname = '!(' + anname + ')'
        return cut(newcut, newname)

    def __iadd__(self, another):
        return self + another
        
    def __isub__(self, another):
        return self - another

    def __str__(self):
        return self.cut.GetTitle()
