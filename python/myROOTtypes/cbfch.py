class cbfch:  # abstract base class for cut, branch, and fch classes
    nh = 0  # number of created histograms to avoid duplicate names and memory leaks
    
    def __init__(self, linecolor=None, markercolor=None, fillcolor=None, fillstyle=None, hname=None, neededbranchnames=None, evaltemp=None, needednames=None):
        self.linecolor = linecolor
        self.markercolor = markercolor
        self.fillcolor = fillcolor
        self.fillstyle = fillstyle
        self.hname = hname
        self.h = None
        self.neededbranchnames = neededbranchnames  # what branch names is this composed of? only really useful for cut and branch
        self.evaltemp = evaltemp  # to be called like `eval(evaltemp.format(tree))`
        self.needednames = needednames  # things that must be defined in the environment for evaltemp to evaluate
    
    def __repr__(self):
        return '<myROOTtypes.{0} object ("{0}") at {1}>'.format(self.__class__.__name__, hex(id(self)))
