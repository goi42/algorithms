from ROOT import TCut
class cut:
    def __init__(self,cut,name=None):
        self.cut = TCut(cut)
        self.name = str(cut)
        if name: self.name = str(name)
        self.csig="" #the cut in addition to self that produces nsig
        self.cbkg="" #the cut in addition to self that produces nbkg
        self.nsig=0
        self.nbkg=0
        self.nL=0
        self.nS=0
        self.nb=0