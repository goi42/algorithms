from ROOT import TCut
from cbfch import cbfch


class cut(cbfch):
    def __init__(self, cut, name=None, weight=None, linecolor=None, fillcolor=None, fillstyle=None, hname=None, neededbranchnames=None, evaltemp=None, needednames=None):
        cbfch.__init__(self, linecolor=linecolor, fillcolor=fillcolor, fillstyle=fillstyle, hname=hname, neededbranchnames=neededbranchnames, evaltemp=evaltemp, needednames=needednames)
        self.cut = TCut(cut)
        self.name = str(name) if name is not None else str(cut)
        self.weight = weight if weight is not None else None  # should be cut, string, or TCut -- another way to apply weights when drawing
    
    def _arithmetic(self, sym, another, altsym='_'):
        from fxns import logical_combine
        if another.__class__.__name__ == self.__class__.__name__:
            ancut = another.cut.GetTitle()
            anname = another.name
            anweight = another.weight
            anlinecolor = another.linecolor
            anfillcolor = another.fillcolor
            anfillstyle = another.fillstyle
            anhname = another.hname
            anneededbranchnames = another.neededbranchnames
            anevaltemp = another.evaltemp
            anneedednames = another.needednames
        elif another.__class__.__name__ == 'str':
            ancut = another
            anname = another
            anweight = anlinecolor = anfillcolor = anfillstyle = anhname = anneededbranchnames = anevaltemp = anneedednames = None
        elif another.__class__.__name__ == 'TCut':
            ancut = another.GetTitle()
            anname = another.GetName()
            anweight = anlinecolor = anfillcolor = anfillstyle = anhname = anneededbranchnames = anevaltemp = anneedednames = None
        else:
            raise TypeError('cannot perform arithmetic on object of class "' + another.__class__.__name__ + '" with object of class "cut"')
        
        newcut = logical_combine(self.cut.GetTitle(), sym, ancut)
        newname = logical_combine(self.name, sym, anname)
        if self.weight == anweight:
            newweight = self.weight
        else:
            raise Exception('cannot combine two cuts with different weights!')
        newlinecolor = self.linecolor if self.linecolor == anlinecolor else None
        newfillcolor = self.fillcolor if self.fillcolor == anfillcolor else None
        newfillstyle = self.fillstyle if self.fillstyle == anfillstyle else None
        newhname = self.hname + altsym + anhname if (self.hname is not None and anhname is not None) else None
        newneededbranchnames = (
            list(set(self.neededbranchnames + anneededbranchnames))
        ) if (
            self.neededbranchnames is not None and anneededbranchnames is not None
        ) else self.neededbranchnames if self.neededbranchnames is not None else anneededbranchnames
        newevaltemp = logical_combine(
            self.evaltemp, sym, anevaltemp
        ) if (
            self.evaltemp is not None and anevaltemp is not None
        ) else None
        newneedednames = (
            list(set(self.needednames + anneedednames))
        ) if (
            self.needednames is not None and anneedednames is not None
        ) else self.needednames if self.needednames is not None else anneedednames
        
        return (
            newcut, newname,
            ancut, anname,
            newweight,
            newlinecolor, newfillcolor, newfillstyle,
            newhname,
            newneededbranchnames,
            newevaltemp,
            newneedednames,
        )
    
    def __add__(self, another):
        (
            newcut, newname,
            ancut, anname,
            newweight,
            newlinecolor, newfillcolor, newfillstyle,
            newhname,
            newneededbranchnames,
            newevaltemp,
            newneedednames,
        ) = self._arithmetic('&&', another, '_and_')
        if not self.cut.GetTitle().strip():
            newcut = ancut
            if not self.name.strip():
                newname = anname
        return cut(
            newcut, newname,
            weight=newweight, hname=newhname, evaltemp=newevaltemp,
            linecolor=newlinecolor, fillcolor=newfillcolor, fillstyle=newfillstyle,
            neededbranchnames=newneededbranchnames, needednames=newneedednames,
        )
    
    def __sub__(self, another):
        'not actual subtraction--actually AND NOT'
        (
            newcut, newname,
            ancut, anname,
            newweight,
            newlinecolor, newfillcolor, newfillstyle,
            newhname,
            newneededbranchnames,
            newevaltemp,
            newneedednames,
        ) = self._arithmetic('&& !', another, '_and_not_')
        if not self.cut.GetTitle().strip():
            newcut = '!(' + ancut + ')'
            if not self.name.strip():
                newname = '!(' + anname + ')'
        return cut(
            newcut, newname,
            weight=newweight, hname=newhname, evaltemp=newevaltemp,
            linecolor=newlinecolor, fillcolor=newfillcolor, fillstyle=newfillstyle,
            neededbranchnames=newneededbranchnames, needednames=newneedednames,
        )
    
    def __neg__(self):
        return cut('') - self
    
    def __mul__(self, another):
        'useful for combining weights'
        (
            newcut, newname,
            ancut, anname,
            newweight,
            newlinecolor, newfillcolor, newfillstyle,
            newhname,
            newneededbranchnames,
            newevaltemp,
            newneedednames,
        ) = self._arithmetic('*', another, '_times_')
        if not self.cut.GetTitle().strip():
            newcut = ancut
            if not self.name.strip():
                newname = anname
        return cut(
            newcut, newname,
            weight=newweight, hname=newhname, evaltemp=newevaltemp,
            linecolor=newlinecolor, fillcolor=newfillcolor, fillstyle=newfillstyle,
            neededbranchnames=newneededbranchnames, needednames=newneedednames,
        )
    
    def __div__(self, another):
        'not actual division--actually OR'
        (
            newcut, newname,
            ancut, anname,
            newweight,
            newlinecolor, newfillcolor, newfillstyle,
            newhname,
            newneededbranchnames,
            newevaltemp,
            newneedednames,
        ) = self._arithmetic('||', another, '_or_')
        if not self.cut.GetTitle().strip():
            newcut = ancut
            if not self.name.strip():
                newname = anname
        return cut(
            newcut, newname,
            weight=newweight, hname=newhname, evaltemp=newevaltemp,
            linecolor=newlinecolor, fillcolor=newfillcolor, fillstyle=newfillstyle,
            neededbranchnames=newneededbranchnames, needednames=newneedednames,
        )
    
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
