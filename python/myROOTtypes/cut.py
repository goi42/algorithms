from ROOT import TCut
from cbfch import cbfch


class cut(cbfch):
    def __init__(self, cut, name=None, linecolor=None, fillcolor=None, fillstyle=None, hname=None):
        cbfch.__init__(self, linecolor=linecolor, fillcolor=fillcolor, fillstyle=fillstyle, hname=hname)
        self.cut = TCut(cut)
        self.name = str(name) if name is not None else str(cut)
    
    def _arithmetic(self, sym, another, altsym='_'):
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
            raise TypeError('cannot perform arithmetic on object of class "' + another.__class__.__name__ + '" with object of class "cut"')
        
        newcut = '(' + self.cut.GetTitle() + ')' + sym + '(' + ancut + ')'
        newname = '(' + self.name + ') ' + sym + ' (' + anname + ')'
        newhname = self.hname + altsym + another.hname if self.hname is not None and another.hname is not None else None
        
        return newcut, newname, ancut, anname, newhname
    
    def __add__(self, another):
        newcut, newname, ancut, anname, newhname = self._arithmetic('&&', another, '_and_')
        if not self.cut.GetTitle().strip():
            newcut = ancut
            if not self.name.strip():
                newname = anname
        return cut(newcut, newname, hname=newhname)
    
    def __sub__(self, another):
        newcut, newname, ancut, anname, newhname = self._arithmetic('&& !', another, '_and_not_')
        if not self.cut.GetTitle().strip():
            newcut = '!(' + ancut + ')'
            if not self.name.strip():
                newname = '!(' + anname + ')'
        return cut(newcut, newname, hname=newhname)
    
    def __mul__(self, another):
        '''useful for combining weights
        '''
        newcut, newname, ancut, anname, newhname = self._arithmetic('*', another, '_times_')
        if not self.cut.GetTitle().strip():
            newcut = ancut
            if not self.name.strip():
                newname = anname
        return cut(newcut, newname, hname=newhname)
    
    def __div__(self, another):
        '''not actual division--a wonky way to do OR
        '''
        newcut, newname, ancut, anname, newhname = self._arithmetic('||', another, '_or_')
        if not self.cut.GetTitle().strip():
            newcut = ancut
            if not self.name.strip():
                newname = anname
        return cut(newcut, newname, hname=newhname)
    
    def __iadd__(self, another):
        return self + another
    
    def __isub__(self, another):
        return self - another
    
    def __imul__(self, another):
        return self * another
    
    def __idiv__(self, another):
        return self / another
    
    def __str__(self):
        return self.cut.GetTitle()
    
    def __getattr__(self, name):
        return getattr(self.cut, name)
