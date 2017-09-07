import sys
from cut import cut

class branch:
    def __init__(self,branch,name=None,nBins=0,loBin=0,hiBin=0,xlabel="",ylabel="",set_log_X=False,set_log_Y=False,can_extend=False,c=None,associated_branch=None):
        self.branch = branch #name of branch as it appears in the tree
        self.name = branch #nickname--usually what you want to appear on a plot
        if name: self.name = name
        self.nBins = nBins
        self.loBin = loBin
        self.hiBin = hiBin
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.set_log_X = set_log_X #do you want a log scale?
        self.set_log_Y = set_log_Y #do you want a log scale?
        self.can_extend = can_extend #do you want Draw to change the bin range?
        self.c = []
        if c: self.c=c #cuts to be applied to the branch
        self.associated_branch = None
        if associated_branch: self.associated_branch = associated_branch #branch() object that this will be plotted against, as <thisbranch>:<associated branch>
        # self.legxi = 0.3
        # self.legxf = 0.6
        # self.legyi = 0.7
        # self.legyf = 0.9
        # self.legend = TLegend(self.legxi,self.legyi,self.legxf,self.legyf)
    def set_binning(self,nBins,loBin,hiBin,can_extend=False):
        if nBins<0 or loBin>hiBin:
            if nBins<0:
                print "branch "+repr(self.name)+" cannot be assigned nBins = "+repr(nBins)+". nBins must be >=0!"
            if loBin>hiBin:
                print "branch "+repr(self.name)+" cannot be assigned loBin = "+repr(loBin)+" and hiBin = "+repr(hiBin)+" loBin must be <= hiBin!"
            sys.exit()
        self.nBins=nBins
        self.loBin=loBin
        self.hiBin=hiBin
        self.can_extend = can_extend
    def add_cut(self,*args,**kwargs):
        if len(args)==1 and len(kwargs)==0 and args[0].__class__.__name__=='cut':
            self.c.append(*args)
        else:
            self.c.append(cut(*args,**kwargs))
