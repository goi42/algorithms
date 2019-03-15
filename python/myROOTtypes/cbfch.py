class cbfch:  # abstract base class for cut, branch, and fch classes
    nh = 0  # number of created histograms to avoid duplicate names and memory leaks
    
    def __init__(self, linecolor=None, fillcolor=None, fillstyle=None, hname=None, neededbranchnames=None):
        self.linecolor = linecolor
        self.fillcolor = fillcolor
        self.fillstyle = fillstyle
        self.hname = hname
        self.h = None
        self.neededbranchnames = neededbranchnames  # only really useful for cut and branch
