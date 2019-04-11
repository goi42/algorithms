import sys
import copy
from cut import cut
from cbfch import cbfch
from bfch import bfch
from ROOT import TH1F, TH1, TH2F, TCut


class branch(bfch):
    def __init__(self, branch, name=None, nBins=0, loBin=0, hiBin=0, units=None, xlabel="", ylabel="",
                 set_log_X=False, set_log_Y=False, can_extend=False, c=None, axname=None,
                 associated_branch=None, uniquenm=None, linecolor=None, fillcolor=None, fillstyle=None,
                 hname=None, neededbranchnames=None, datatype=None, evaltemp=None, needednames=None,
                 nBins_pretty=None, subranges=None,
                 ):
        # evaluate some default values
        if name is None:
            name = branch
        if uniquenm is None:
            uniquenm = (branch.split(':=')[0].strip()) if ':=' in branch else branch
        if hname is None:
            hname = uniquenm
        if neededbranchnames is None:
            neededbranchnames = ([branch]) if ':=' not in branch else ([])
        if evaltemp is None and ':=' not in branch:
            evaltemp = '{0}.' + branch
        if datatype is None:
            datatype = 'F'
        if needednames is None:
            needednames = []
        
        # initialize members
        bfch.__init__(
            self, c=c, linecolor=linecolor, fillcolor=fillcolor, fillstyle=fillstyle, hname=hname,
            neededbranchnames=neededbranchnames, evaltemp=evaltemp, needednames=needednames)
        self.branch = branch  # name of branch as it appears in the tree
        self.name = name  # nickname--usually what you want to appear on a plot
        self.nBins = nBins
        self.loBin = loBin
        self.hiBin = hiBin
        self.units = units
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.set_log_X = set_log_X  # do you want a log scale?
        self.set_log_Y = set_log_Y  # do you want a log scale?
        self.can_extend = can_extend  # do you want Draw to change the bin range?
        self.associated_branch = associated_branch  # branch() object that this will be plotted against, as <thisbranch>:<associated branch>
        self.uniquenm = uniquenm
        self.axname = axname
        self.datatype = datatype  # 'F' for float, etc.
        self.nBins_pretty = nBins_pretty
        self.subranges = {}
        if subranges is not None:
            self.set_subranges(subranges)
        # self.legxi = 0.3
        # self.legxf = 0.6
        # self.legyi = 0.7
        # self.legyf = 0.9
        # self.legend = TLegend(self.legxi,self.legyi,self.legxf,self.legyf)
    
    def set_binning(self, nBins, loBin, hiBin, can_extend=False):
        if nBins < 0:
            raise ValueError("branch {} cannot be assigned nBins = {}. nBins must be >=0!".format(repr(self.name), repr(nBins)))
        if loBin > hiBin:
            raise ValueError("branch {} cannot be assigned loBin = {} and hiBin = {} loBin must be <= hiBin!".format(repr(self.name), repr(loBin), repr(hiBin)))
        self.nBins = nBins
        self.loBin = loBin
        self.hiBin = hiBin
        self.can_extend = can_extend
    
    def calc_nBins(self, binsize):
        nBins = float(self.hiBin - self.loBin) / float(binsize)
        if nBins != int(nBins):
            raise ValueError('binsize incompatible with range')
        self.nBins = int(nBins)
    
    def get_bin_width(self):
        return (float(self.hiBin) - float(self.loBin)) / float(self.nBins)
    
    def prep_for_histogram(self):
        'make sure properties are set properly for histogram creation'
        
        if self.nBins is None:
            self.nBins = 100  # set default binning if not specified
        hilospec = False  # is either loBin or hiBin non-0?
        if self.loBin or self.hiBin:
            hilospec = True
        binning_set = all([self.nBins, hilospec])  # is the binning completely specified now?
        if not binning_set:
            self.can_extend = True
        if self.associated_branch:
            self.associated_branch.prep_for_histogram()
    
    def make_histogram(self, hname=None, linecolor=None, fillcolor=None, fillstyle=None, sumw2=True, overwrite=False, return_histogram=True):  # create an empty histogram
        if linecolor is None and self.linecolor is None:
            linecolor = 1
        elif linecolor is None:
            linecolor = self.linecolor
        if fillcolor is None:
            fillcolor = self.fillcolor
        if fillstyle is None:
            fillstyle = self.fillstyle
            
        if not hname:
            hname = 'h' + repr(cbfch.nh)
            cbfch.nh += 1
        if self.h and not overwrite:
            raise Exception('{} has h already'.format(self.name))
        elif overwrite:
            self.h = None
        assocbranch = self.associated_branch
        self.prep_for_histogram()
        if not assocbranch:
            h = TH1F(hname, self.name, self.nBins, self.loBin, self.hiBin)
            if(self.can_extend):
                h.SetCanExtend(TH1.kAllAxes)
            h.SetLineColor(linecolor)
            if fillcolor is not None:
                h.SetFillColor(fillcolor)
            if fillstyle is not None:
                h.SetFillStyle(fillstyle)
        else:
            h = TH2F(hname, self.name + ' vs. ' + assocbranch.name, self.nBins, self.loBin, self.hiBin, assocbranch.nBins, assocbranch.loBin, assocbranch.hiBin)
            if(self.can_extend):
                h.SetCanExtend(TH1.kXaxis)
            if(assocbranch.can_extend):
                h.SetCanExtend(TH1.kYaxis)
            h.GetXaxis().SetTitle(self.branch)
            h.GetYaxis().SetTitle(assocbranch.branch)
        if sumw2:
            h.Sumw2()
        self.h = h
        if return_histogram:
            return h
    
    def set_subranges(self, subranges):
        'subranges is a dictionary specifying other binning ranges '
        'of the form {"name": (nBins, loBin, hiBin),} '
        'must be an even subset of the primary range '
        if not isinstance(subranges, dict):
            raise TypeError('expected a dictionary!')
        if not all(len(x) == 3 for x in subranges.values()):
            raise ValueError('subranges should specify nBins, loBin, hiBin')
        
        for snm, (nBins, loBin, hiBin) in subranges.iteritems():
            if snm in self.subranges:
                raise ValueError('subrange {0} is already specified'.format(snm))
            if loBin < self.loBin:
                raise ValueError('subrange {0} has loBin {1} which is lower than the primary loBin {2}'.format(snm, loBin, self.loBin))
            if hiBin > self.hiBin:
                raise ValueError('subrange {0} has hiBin {1} which is higher than the primary hiBin {2}'.format(snm, hiBin, self.hiBin))
            
            if nBins != 0 and self.nBins != 0:
                perbin = float(hiBin - loBin) / nBins
                selfperbin = float(self.hiBin - self.loBin) / self.nBins
                
                if perbin < selfperbin:
                    raise ValueError('{0} has {1} per bin, but this is less than {2}, the one of the overall range'.format(snm, perbin, selfperbin))
                if perbin % selfperbin > 0.001:  # rounding errors
                    raise ValueError('{0} has {1} per bin, but this is not an even multiple of {2}, the one of the overall range'.format(snm, perbin, selfperbin))
            
            self.subranges[snm] = (nBins, loBin, hiBin)
    
    def _arithmetic(self, sym, another, altsym='_'):
        from fxns import logical_combine
        newbranch = logical_combine(self.branch, sym, another.branch)
        newname = logical_combine(self.name, sym, another.name)
        if not(self.hiBin - self.loBin == 0 or another.hiBin - another.loBin == 0):
            binning_rate = max(float(self.nBins) / (self.hiBin - self.loBin), float(another.nBins) / (another.hiBin - another.loBin))
        else:
            binning_rate = 0
        if all([self.xlabel, self.ylabel, another.xlabel, another.ylabel]):
            xlabel = logical_combine(self.xlabel, sym, another.xlabel)
            ylabel = logical_combine(self.ylabel, sym, another.ylabel)
        else:
            xlabel = None
            ylabel = None
        if self.set_log_X or another.set_log_X:
            set_log_X = True
        else:
            set_log_X = False
        if self.set_log_Y or another.set_log_Y:
            set_log_Y = True
        else:
            set_log_Y = False
        if self.can_extend or another.can_extend:
            can_extend = True
        else:
            can_extend = False
        c = list(set(self.c + another.c))
        if not (self.associated_branch and another.associated_branch):
            if self.associated_branch:
                associated_branch = self.associated_branch
            elif another.associated_branch:
                associated_branch = another.associated_branch
            else:
                associated_branch = None
        else:
            associated_branch = None
        newhname = self.hname + altsym + another.hname if self.hname is not None and another.hname is not None else None
        newuniquenm = self.uniquenm + altsym + another.uniquenm if self.uniquenm and another.uniquenm else None
        newunits = None if any(x is None for x in (self.units, another.units)) else logical_combine(self.units, sym, another.units)
        return newbranch, newname, binning_rate, xlabel, ylabel, set_log_X, set_log_Y, can_extend, c, associated_branch, newhname, newuniquenm, newunits
    
    def __add__(self, another):
        newbranch, newname, binning_rate, xlabel, ylabel, set_log_X, set_log_Y, can_extend, c, associated_branch, newhname, newuniquenm, newunits = self._arithmetic('+', another, '_plus_')
        hiBin = self.hiBin + another.hiBin
        loBin = self.loBin + another.loBin
        nBins = int(round(binning_rate * (hiBin - loBin)))
        if nBins == 0:
            nBins = 100
        if all(x is not None for x in (self.units, another.units)) and self.units == another.units:
            newunits = self.units
        if self.associated_branch and another.associated_branch:
            associated_branch = self.associated_branch + another.associated_branch
        return branch(newbranch, newname, nBins, loBin, hiBin, newunits, xlabel, ylabel, set_log_X, set_log_Y, can_extend, c, associated_branch, hname=newhname, uniquenm=newuniquenm)
    
    def __sub__(self, another):
        newbranch, newname, binning_rate, xlabel, ylabel, set_log_X, set_log_Y, can_extend, c, associated_branch, newhname, newuniquenm, newunits = self._arithmetic('-', another, '_minus_')
        hiBin = self.hiBin - another.loBin
        loBin = self.loBin - another.hiBin
        nBins = int(round(binning_rate * (hiBin - loBin)))
        if nBins == 0:
            nBins = 100
        # hiBin = loBin = 0
        # nBins = 100
        if all(x is not None for x in (self.units, another.units)) and self.units == another.units:
            newunits = self.units
        if self.associated_branch and another.associated_branch:
            associated_branch = self.associated_branch - another.associated_branch
        return branch(newbranch, newname, nBins, loBin, hiBin, newunits, xlabel, ylabel, set_log_X, set_log_Y, can_extend, c, associated_branch, hname=newhname, uniquenm=newuniquenm)
    
    def __mul__(self, another):
        newbranch, newname, binning_rate, xlabel, ylabel, set_log_X, set_log_Y, can_extend, c, associated_branch, newhname, newuniquenm, newunits = self._arithmetic('*', another, '_times_')
        if self.hiBin >= 0 and another.hiBin >= 0 and self.loBin >= 0 and another.loBin >= 0:
            hiBin = self.hiBin * another.hiBin
            loBin = self.loBin * another.loBin
            nBins = int(round(binning_rate * (hiBin - loBin)))
            if nBins == 0:
                nBins = 100
        else:
            hiBin = 0
            loBin = 0
            nBins = 100
        if self.associated_branch and another.associated_branch:
            associated_branch = self.associated_branch * another.associated_branch
        if all(x is not None for x in (self.units, another.units)) and self.units == another.units:
            newunits = '({0})^{{2}}'.format(self.units)
        return branch(newbranch, newname, nBins, loBin, hiBin, newunits, xlabel, ylabel, set_log_X, set_log_Y, can_extend, c, associated_branch, hname=newhname, uniquenm=newuniquenm)
    
    def __pow__(self, power):  # special case; does not call _arithmetic
        outbranch = copy.deepcopy(self)
        if power == 0.5:
            outbranch.branch = 'sqrt(' + self.branch + ')'
            outbranch.name = '#sqrt{' + self.name + '}'
            if self.xlabel:
                outbranch.xlabel = '#sqrt{' + self.xlabel + '}'
            if self.ylabel:
                outbranch.ylabel = '#sqrt{' + self.ylabel + '}'
        else:
            outbranch.branch = 'pow(' + self.branch + ',' + repr(power) + ')'
            outbranch.name = '(' + self.name + ')^{' + repr(power) + '}'
            if self.xlabel:
                outbranch.xlabel = '(' + self.xlabel + ')^{' + repr(power) + '}'
            if self.ylabel:
                outbranch.ylabel = '(' + self.ylabel + ')^{' + repr(power) + '}'
        if not(self.hiBin - self.loBin == 0):
            binning_rate = float(self.nBins) / (self.hiBin - self.loBin)
        else:
            binning_rate = 0
        outbranch.hiBin = self.hiBin ** power
        outbranch.loBin = self.loBin ** power
        outbranch.nBins = int(round(binning_rate * (outbranch.hiBin - outbranch.loBin)))
        if self.units is not None:
            outbranch.units = '({0})^{{{1}}}'.format(self.units, power)
        if outbranch.nBins == 0:
            outbranch.nBins = 100
        if self.hname is not None:
            outbranch.hname = self.hname + '_to_power_{}_'.format(power)
        if self.uniquenm is not None:
            outbranch.uniquenm = self.uniquenm + '_to_power_{}_'.format(power)
        return outbranch
    
    def __div__(self, another):
        newbranch, newname, binning_rate, xlabel, ylabel, set_log_X, set_log_Y, can_extend, c, associated_branch, newhname, newuniquenm, newunits = self._arithmetic('/', another, '_divided_by_')
        if self.hiBin >= 0 and another.hiBin > 0 and self.loBin >= 0 and another.loBin > 0:
            hiBin = self.hiBin / another.loBin
            loBin = self.loBin / another.hiBin
            nBins = int(round(binning_rate * (hiBin - loBin)))
            if nBins == 0:
                nBins = 100
        else:
            hiBin = 0
            loBin = 0
            nBins = 100
        if all(x is not None for x in (self.units, another.units)) and self.units == another.units:
            newunits = ''
        if self.associated_branch and another.associated_branch:
            associated_branch = self.associated_branch * another.associated_branch
        return branch(newbranch, newname, nBins, loBin, hiBin, newunits, xlabel, ylabel, set_log_X, set_log_Y, can_extend, c, associated_branch, hname=newhname, uniquenm=newuniquenm)
    
    def __iadd__(self, another):
        return self + another
    
    def __isub__(self, another):
        return self - another
    
    def __imul__(self, another):
        return self * another
    
    def __ipow__(self, power):
        return self ** power
    
    def __idiv__(self, another):
        return self / another
    
    def __str__(self):
        return self.branch
