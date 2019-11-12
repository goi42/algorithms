import ROOT
from cbfch import cbfch


class cut(cbfch):
    def __init__(self, cut=None, name=None, weight=None, linecolor=None, markercolor=None, fillcolor=None, fillstyle=None, hname=None, neededbranchnames=None, evaltemp=None, needednames=None, uniquenm=None, stackcut=None):
        if cut is None and evaltemp is not None:
            cut = evaltemp.replace('{0}.', '')
        if hname is None:
            hname = uniquenm
        cbfch.__init__(self, linecolor=linecolor, markercolor=markercolor, fillcolor=fillcolor, fillstyle=fillstyle, hname=hname, neededbranchnames=neededbranchnames, evaltemp=evaltemp, needednames=needednames)
        self.cut = ROOT.TCut(cut)
        self.name = str(name) if name is not None else str(cut)
        self.weight = weight if weight is not None else None  # should be cut, string, or TCut -- another way to apply weights when drawing
        if uniquenm is None:
            uniquenm = self.cut.GetTitle()
        self.uniquenm = uniquenm
        self.stackcut = stackcut  # this cut should be interpreted as a filter of another cut (the stackcut)
        # WARNING: make sure that cuts with this stackcut are assigned a unique uniquenm! Otherwise they could get overridden by cuts without.
    
    def check_dummy(self):
        return not any([  # decide whether this is a dummy cut
            bool(self.cut.GetTitle()),
            bool(self.name),
            bool(self.weight),
            bool(self.linecolor),
            bool(self.markercolor),
            bool(self.fillcolor),
            bool(self.fillstyle),
            bool(self.hname),
            bool(self.neededbranchnames),
            bool(self.evaltemp),
            bool(self.needednames),
            bool(self.uniquenm),
            bool(self.stackcut),
        ])
    
    def make_histogram(self, f, b, hname=None, htit=None, overwrite=False, return_histogram=True, use_subranges=False):
        'declare a histogram (set to self.h) from the given file `f` and branch `b`'
        
        if overwrite:
            self.h = None
        elif self.h is not None:
            raise Exception('h already exists!')
        
        if use_subranges:
            def getarray(_b):
                from array import array
                
                # ensure subranges exists
                if not _b.subranges:
                    raise Exception('branch {0} has no subranges'.format(_b.name))
                
                # get list of bin edges
                bins = []
                for key, (nbins, lo, hi) in _b.subranges.iteritems():
                    step = float(hi - lo) / nbins
                    val = lo
                    while val <= hi:
                        if val not in bins:
                            bins.append(val)
                        val += step
                
                return array('d', sorted(bins))
            
            bbins = getarray(b)
            abbins = getarray(b.associated_branch)
        
        # add potentially missing items
        b.add_column(f)
        b.prep_for_histogram()
        filterdframe = f.add_filtered_dframe(self)
        
        # declare title and name
        if hname is None:
            hname = 'h_{0}_{1}{2}_{3}'.format(
                cbfch.nh if f.hname is None else f.hname,
                '' if b.associated_branch is None else b.associated_branch.hname + '_',
                cbfch.nh if b.hname is None else b.hname,
                cbfch.nh if self.hname is None else self.hname,
            )
        if htit is None:
            if b.associated_branch:
                bname = '{0} vs. {1}'.format(b.associated_branch.name, b.name)
            else:
                bname = b.name
            htit = '{0}: {1}: {2}'.format(f.name, bname, self.name)
        
        # declare parameters for histogram creation
        hargs = [hname, htit]
        hargs += [len(bbins) - 1, bbins] if use_subranges else [b.nBins, b.loBin, b.hiBin]
        if b.associated_branch is None:
            passlist = [tuple(hargs), b.uniquenm]
            thehcomm = filterdframe.Histo1D
            self.hdims = 1
        else:
            ab = b.associated_branch
            toadd = [len(abbins) - 1, abbins] if use_subranges else [ab.nBins, ab.loBin, ab.hiBin]
            passlist = [tuple(hargs + toadd), b.uniquenm, ab.uniquenm]
            thehcomm = filterdframe.Histo2D
            self.hdims = 2
        if self.weight is not None:
            passlist += [self.weight if isinstance(self.weight, str) else self.weight.GetTitle()]
        
        # create histogram
        theh = thehcomm(*passlist)
        
        cbfch.nh += 1
        
        self.h = theh
        if return_histogram:
            return theh
    
    def format_histogram(self, hname=None, htit=None, linecolor=None, markercolor=None, fillcolor=None, fillstyle=None, sumw2=True, set_can_extend=True, set_axis_titles=True, b=None):
        if set_can_extend and b is None:
            raise TypeError('`set_can_extend` requires `b`')
        if set_axis_titles and b is None:
            raise TypeError('`set_axis_titles` requires `b`')
        
        if linecolor is None and self.linecolor is None:
            linecolor = 1
        elif linecolor is None:
            linecolor = self.linecolor
        if markercolor is None:
            markercolor = self.markercolor
        if fillcolor is None:
            fillcolor = self.fillcolor
        if fillstyle is None:
            fillstyle = self.fillstyle
            
        if hname is not None:
            self.h.SetName(hname)
        if htit is not None:
            self.h.SetTitle(htit)
        if sumw2:
            self.h.Sumw2()
        if self.hdims == 1:
            if set_can_extend:
                if b.can_extend is True:
                    self.h.SetCanExtend(ROOT.TH1.kAllAxes)
            self.h.SetLineColor(linecolor)
            if markercolor is not None:
                self.h.SetMarkerColor(markercolor)
            if fillcolor is not None:
                self.h.SetFillColor(fillcolor)
            if fillstyle is not None:
                self.h.SetFillStyle(fillstyle)
            if set_axis_titles:
                xaxtit = b.name
                if b.units:
                    xaxtit += ' [{}]'.format(b.units)
                yaxtit = 'Entries / ({}{})'.format(
                    b.get_bin_width(),
                    (' ' + b.units) if b.units else '')
                self.h.GetXaxis().SetTitle(xaxtit)
                self.h.GetYaxis().SetTitle(yaxtit)
        elif self.hdims == 2:
            if set_can_extend:
                if b.can_extend is True:
                    self.h.SetCanExtend(ROOT.TH1.kXaxis)
                if b.associated_branch.can_extend is True:
                    self.h.SetCanExtend(ROOT.TH1.kYaxis)
            if set_axis_titles:
                xaxtit = b.name
                if b.units:
                    xaxtit += ' [{}]'.format(b.units)
                yaxtit = b.associated_branch.name
                if b.associated_branch.units:
                    yaxtit += ' [{}]'.format(b.associated_branch.units)
                self.h.GetXaxis().SetTitle(xaxtit)
                self.h.GetYaxis().SetTitle(yaxtit)
    
    def fill_histogram(self, evt, b):
        if eval(self.evaltemp.format('evt')):
            if self.hdims == 1:
                filllist = [eval(b.evaltemp.format('evt'))]
            elif self.hdims == 2:
                filllist = [eval(b.evaltemp.format('evt')), eval(b.associated_branch.evaltemp.format('evt'))]
            if self.weight is not None:
                filllist.append(self.weight)
            
            self.h.Fill(*filllist)
    
    def _arithmetic(self, sym, another, altsym='_', pysym=None):
        from fxns import logical_combine
        
        if another.__class__.__name__ == self.__class__.__name__:
            ancut = another.cut.GetTitle()
            anname = another.name
            anweight = another.weight
            anlinecolor = another.linecolor
            anmarkercolor = another.markercolor
            anfillcolor = another.fillcolor
            anfillstyle = another.fillstyle
            anhname = another.hname
            anneededbranchnames = another.neededbranchnames
            anevaltemp = another.evaltemp
            anneedednames = another.needednames
        elif another.__class__.__name__ == 'str':
            ancut = another
            anname = another
            anweight = anlinecolor = anmarkercolor = anfillcolor = anfillstyle = anhname = anneededbranchnames = anevaltemp = anneedednames = None
        elif another.__class__.__name__ == 'TCut':
            ancut = another.GetTitle()
            anname = another.GetName()
            anweight = anlinecolor = anmarkercolor = anfillcolor = anfillstyle = anhname = anneededbranchnames = anevaltemp = anneedednames = None
        else:
            raise TypeError('cannot perform arithmetic on object of class "' + another.__class__.__name__ + '" with object of class "cut"')
        
        if self.check_dummy():  # self is a dummy, blank-slate cut; just use another
            return (
                ancut, anname,
                ancut, anname,
                anweight,
                anlinecolor, anmarkercolor, anfillcolor, anfillstyle,
                anhname,
                anneededbranchnames,
                anevaltemp,
                anneedednames,
            )
        
        newcut = logical_combine(self.cut.GetTitle(), sym, ancut)
        newname = logical_combine(self.name, sym, anname)
        if self.weight == anweight:
            newweight = self.weight
        else:
            raise Exception('cannot combine two cuts with different weights!')
        newlinecolor = self.linecolor if self.linecolor == anlinecolor else None
        newmarkercolor = self.markercolor if self.markercolor == anmarkercolor else None
        newfillcolor = self.fillcolor if self.fillcolor == anfillcolor else None
        newfillstyle = self.fillstyle if self.fillstyle == anfillstyle else None
        newhname = self.hname + altsym + anhname if (self.hname is not None and anhname is not None) else None
        newneededbranchnames = (
            list(set(self.neededbranchnames + anneededbranchnames))
        ) if (
            self.neededbranchnames is not None and anneededbranchnames is not None
        ) else self.neededbranchnames if self.neededbranchnames is not None else anneededbranchnames
        newevaltemp = logical_combine(
            self.evaltemp, sym if pysym is None else pysym, anevaltemp
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
            newlinecolor, newmarkercolor, newfillcolor, newfillstyle,
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
            newlinecolor, newmarkercolor, newfillcolor, newfillstyle,
            newhname,
            newneededbranchnames,
            newevaltemp,
            newneedednames,
        ) = self._arithmetic('&&', another, '_and_', 'and')
        return cut(
            newcut, newname,
            weight=newweight, hname=newhname, evaltemp=newevaltemp,
            linecolor=newlinecolor, markercolor=newmarkercolor, fillcolor=newfillcolor, fillstyle=newfillstyle,
            neededbranchnames=newneededbranchnames, needednames=newneedednames,
        )
    
    def __sub__(self, another):
        'not actual subtraction--actually AND NOT'
        (
            newcut, newname,
            ancut, anname,
            newweight,
            newlinecolor, newmarkercolor, newfillcolor, newfillstyle,
            newhname,
            newneededbranchnames,
            newevaltemp,
            newneedednames,
        ) = self._arithmetic('&& !', another, '_and_not_', 'and not')
        if self.check_dummy():
            newcut = '!(' + ancut + ')'
            if not self.name.strip():
                newname = '!(' + anname + ')'
            newevaltemp = 'not (' + newevaltemp + ')'
            newhname = 'not_' + newhname
        return cut(
            newcut, newname,
            weight=newweight, hname=newhname, evaltemp=newevaltemp,
            linecolor=newlinecolor, markercolor=newmarkercolor, fillcolor=newfillcolor, fillstyle=newfillstyle,
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
            newlinecolor, newmarkercolor, newfillcolor, newfillstyle,
            newhname,
            newneededbranchnames,
            newevaltemp,
            newneedednames,
        ) = self._arithmetic('*', another, '_times_')
        return cut(
            newcut, newname,
            weight=newweight, hname=newhname, evaltemp=newevaltemp,
            linecolor=newlinecolor, markercolor=newmarkercolor, fillcolor=newfillcolor, fillstyle=newfillstyle,
            neededbranchnames=newneededbranchnames, needednames=newneedednames,
        )
    
    def __div__(self, another):
        'not actual division--actually OR'
        (
            newcut, newname,
            ancut, anname,
            newweight,
            newlinecolor, newmarkercolor, newfillcolor, newfillstyle,
            newhname,
            newneededbranchnames,
            newevaltemp,
            newneedednames,
        ) = self._arithmetic('||', another, '_or_', 'or')
        return cut(
            newcut, newname,
            weight=newweight, hname=newhname, evaltemp=newevaltemp,
            linecolor=newlinecolor, markercolor=newmarkercolor, fillcolor=newfillcolor, fillstyle=newfillstyle,
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
