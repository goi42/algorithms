import sys
from cut import cut

class branch:
    def __init__(self,branch,name=None,nBins=None,loBin=None,hiBin=None,xlabel=None,ylabel=None):
        binlist = (nBins,loBin,hiBin)
        self.branch = branch
        self.name = branch #nickname--usually what you want to appear on a plot
        if name: self.name = name
        self.nBins = self.loBin = self.hiBin = 0
        if all(binlist):
            self.nBins = nb
            self.loBin = lb
            self.hiBin = hb
        elif any(binlist) and not all(binlist):
            print repr(self.name)+" not instantiated properly!"
            print "must specify none or all of nBins, loBin, and hiBin when instantiating branch object!"
            sys.exit()
        self.xlabel = self.ylabel = ""
        if xlabel: self.xlabel = xlabel
        if ylabel: self.ylabel = ylabel
        self.can_extend = False #do you want Draw to change the bin range?
        self.set_log_Y = False #do you want a log scale?
        self.c=[]#cuts to be applied to the branch
        # self.legxi = 0.3
        # self.legxf = 0.6
        # self.legyi = 0.7
        # self.legyf = 0.9
        # self.legend = TLegend(self.legxi,self.legyi,self.legxf,self.legyf)
    def binning(self,nBins,loBin,hiBin,can_extend=None):
        if nBins<0 or loBin>hiBin:
            if nBins<0:
                print "branch "+repr(self.name)+" cannot be assigned nBins = "+repr(nBins)+". nBins must be >=0!"
            if loBin>hiBin:
                print "branch "+repr(self.name)+" cannot be assigned loBin = "+repr(loBin)+" and hiBin = "+repr(hiBin)+" loBin must be <= hiBin!"
            sys.exit()
        self.nBins=nBins
        self.loBin=loBin
        self.hiBin=hiBin
        if can_extend:
            self.can_extend = can_extend
    def add_cut(self,Cut,name=None):
        self.c.append(cut(Cut,name))
  
