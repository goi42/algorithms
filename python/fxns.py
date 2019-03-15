import os
import sys
from contextlib import contextmanager


def in_brackets(astring):
    if '[' not in astring:
        return None
    if ']' not in astring:
        raise ValueError('no closing ] in "{0}"'.format(astring))
    if len(astring.split('[')) != 2:
        raise ValueError('more than one [ in "{0}"'.format(astring))
    bef, aft_ = astring.split('[')
    brval, aft = aft_.split(']')
    return brval


def invmass(*args):
    """returns a string representing the invariant mass of an arbitrary number of strings (using pow and sqrt) by using '_PE', '_PX', '_PY', '_PZ' (or 'P_E' if 'TRUE' in the name)
    """
    kvars = ('_PE', '_PX', '_PY', '_PZ')
    outstr = 'sqrt('
    for ikv, kv in enumerate(kvars):
        outstr += 'pow('
        for i, p in enumerate(args):
            if 'TRUE' in p:
                use_kv = kv.replace('_P', 'P_')
            else:
                use_kv = kv
            brval = ''
            if '[' in p:
                if ']' not in p:
                    raise ValueError('no closing ] in "{0}"'.format(p))
                if len(p.split('[')) != 2:
                    raise ValueError('more than one [ in "{0}"'.format(p))
                bef, aft_ = p.split('[')
                brval, aft = aft_.split(']')
                if aft:
                    raise ValueError('more text after ] in "{0}"?'.format(p))
                p = bef + aft
            outstr += p + use_kv
            if brval:
                outstr += '[{0}]'.format(brval)
            if not i == len(args) - 1:
                outstr += ' + '
        outstr += ', 2)'
        if not ikv == len(kvars) - 1:
            outstr += ' - '
    outstr += ')'
    return outstr


def momentum(*args, **kwargs):
    """returns a string representing the magnitude of the momentum of an arbitrary number of strings (using pow and sqrt) by using '_PX', '_PY', '_PZ' (or 'P_X' if 'TRUE' in the name)
    use kwarg transverse=True for transverse momentum
    """
    kvars = ['_PX', '_PY']
    if 'transverse' not in kwargs.keys() or kwargs['transverse'] is not True:
        kvars.append('_PZ')
    outstr = 'sqrt('
    for ikv, kv in enumerate(kvars):
        outstr += 'pow('
        for i, p in enumerate(args):
            if 'TRUE' in p:
                use_kv = kv.replace('_P', 'P_')
            else:
                use_kv = kv
            outstr += p + use_kv
            if not i == len(args) - 1:
                outstr += ' + '
        outstr += ', 2)'
        if not ikv == len(kvars) - 1:
            outstr += ' + '
    outstr += ')'
    return outstr


def FD(mother, daughter):
    "returns a string representing the magnitude of the distance"
    " between endvertices of the mother and the daughter"
    
    kvars = ('_ENDVERTEX_X', '_ENDVERTEX_Y', '_ENDVERTEX_Z')
    outstr = 'sqrt('
    for ikv, kv in enumerate(kvars):
        outstr += 'pow('
        for i, p in enumerate((mother, daughter,)):
            if 'TRUE' in p:
                raise Exception
                use_kv = kv.replace('_P', 'P_')
            else:
                use_kv = kv
            outstr += p + use_kv
            if not i == len((mother, daughter,)) - 1:
                outstr += ' - '
        outstr += ', 2)'
        if not ikv == len(kvars) - 1:
            outstr += ' + '
    outstr += ')'
    return outstr


def rapidity(nm):
    "returns a string representing the rapidity y of nm (using atanh) by using '_PZ' and '_P' "
    "(or using 'P_Z' and calculating P with 'P_X', 'P_Y', 'P_Z' [using sqrt and pow] if 'TRUE' in nm): "
    "y = artanh(p_Z / abs(p)) ~= -ln(tan(theta / 2)) = eta = psuedorapidity"
    if 'TRUE' in nm:
        p = momentum(nm)
        pZ = '{NM}P_Z'.format(NM=nm)
    else:
        p = '{NM}_P'.format(NM=nm)
        pZ = '{NM}_PZ'.format(NM=nm)
    return 'atanh({PZ} / {P})'.format(PZ=pZ, P=p)


def truedeclength(nm):
    """returns a string representing the decay length of the given parameter name (using pow and sqrt) by finding the length of the vector between TRUEORIGINVERTEX and TRUEENDVERTEX.
    """
    return 'sqrt(pow({NM}_TRUEENDVERTEX_X - {NM}_TRUEORIGINVERTEX_X, 2) + pow({NM}_TRUEENDVERTEX_Y - {NM}_TRUEORIGINVERTEX_Y, 2) + pow({NM}_TRUEENDVERTEX_Z - {NM}_TRUEORIGINVERTEX_Z, 2))'.format(NM=nm)


def replE(ps, ms, *args):
    """replaces one mass hypothesis with another by recalculating the energy with the presumed mass
    returns an invariant mass string
    `ps` is a list of particles
    `ms` is a list of their desired mass hypotheses
    args are the names of other particles to include in the invariant mass
    """
    assert type(ps) == list and type(ms) == list and len(ps) == len(ms)
    kvars = ('_PX', '_PY', '_PZ')
    parts = ps + list(args)
    outstr = 'sqrt(pow('
    for i, (p, m) in enumerate(zip(ps, ms)):
        outstr += 'sqrt({M} * {M} + {PART}_P * {PART}_P)'.format(M=m, PART=p)
        if not i == len(ps) - 1:
            outstr += ' + '
    for p in args:
        outstr += ' + {}_PE'.format(p)
    outstr += ', 2)'
    for ikv, kv in enumerate(kvars):
        outstr += ' - pow('
        for i, p in enumerate(parts):
            outstr += p + kv
            if not i == len(parts) - 1:
                outstr += ' + '
        outstr += ', 2)'
    outstr += ')'
    return outstr


def shim_thickness(start, stop, subtract):
    """ sums from start to stop (inclusive) and subtracts subtract
    start, stop, subtract, and output given in thousandths of an inch (no fractions)
    """
    assert stop > start
    out_value = 0
    for i in xrange(start, stop + 1):
        out_value += i
    out_value -= subtract
    return out_value
    

def print_thicknesses(*args):
    """prints table of thicknesses (calculated using `shim_thickness`) ready for emailing.
    enter side A, then side C measurements for as many positions as you like, e.g.,
    `start1A, stop1A, subtract1A, start1C, stop1C, subtract1C, start2A, stop2A, subtract2A, start2C, stop2C, subtract2C`
    and so on.
    """
    assert len(args) % 2 == 0 and len(args) % 3 == 0 and all(isinstance(x, int) for x in args)

    for irowt, ((Astart, Astop, Asubtract), (Cstart, Cstop, Csubtract)) in enumerate(zip(*[iter(zip(*[iter(args)] * 3))] * 2)):  # split and loop over undifferentiated argument list
        irow = irowt + 1
        print 'A{}:'.format(irow), shim_thickness(Astart, Astop, Asubtract), '\tC{}:'.format(irow), shim_thickness(Cstart, Cstop, Csubtract)


def randmoney(hival=10.00, loval=1.00):
    """returns random monetary value (string)
    loval <= output < hival
    """
    from random import randrange
    hi, lo = hival * 100, loval * 100
    v = randrange(lo, hi, 1)
    return '${}'.format(round(float(v) / 100, 2))  # float and round to make sure


def divsquare(num):
    """returns rows, columns
    """
    import math
    sqnc = math.sqrt(num)
    sqncu = int(math.ceil(sqnc))
    sqncd = int(math.floor(sqnc))
    while(sqncu * sqncd < num):
        sqncu += 1
    return sqncu, sqncd


def makedirsif(adir):
    """makes directory tree if it doesn't already exist
    """
    try:
        os.makedirs(adir)
    except OSError as e:
        if '[Errno 17]' in str(e):
            pass


def getRTDtemp(R, R0=100.0, T0=0.0, a=3.9083E-3, b=-5.7750E-7):
    """ Return temperature in Celcius given an RTD's resistance in Ohms. Uses formula R = R0*(1+a*(T-T0)+b*(T-T0)**2). Only valid for T>=0.
    Originally based on email from Ivan:
    The RTD's in sub-basement lab are standard Pt100 ones. Their resistance depends on temperature as R = R0*(1+a*(T-T0)), where T0 = 0C, R0 = 100 Ohm, a = 0.00385 1/C.
    modified for greater precision according to the equation at https://techoverflow.net/2016/01/02/accurate-calculation-of-pt100pt1000-temperature-from-resistance/
    """
    from math import sqrt
    T = T0 + (sqrt(a**2 + 4 * b * (R / R0 - 1)) - a) / (2 * b)
    if T < 0:
        raise ValueError('negative T calculated: T = {}. Formula not valid for T < 0.'.format(T))
    return T


def getRTDres(T, R0=100.0, T0=0.0, a=3.9083E-3, b=-5.7750E-7, c=None):
    """ Return resistance in ohms an RTD should have for a given temperature in Celcius. Uses formula R = R0*(1+a*(T-T0)+b*(T-T0)**2+c*(T-T0-100)*(T-T0)**3).
    Careful assigning c. Calculated internally if not assigned. T-dependent in calculation (0 for T>=0).
    Originally based on email from Ivan:
    The RTD's in sub-basement lab are standard Pt100 ones. Their resistance depends on temperature as R = R0*(1+a*(T-T0)), where T0 = 0C, R0 = 100 Ohm, a = 0.00385 1/C.
    modified for greater precision according to the equation at https://techoverflow.net/2016/01/02/accurate-calculation-of-pt100pt1000-temperature-from-resistance/
    """
    if c is None:
        c = 0 if T >= 0 else -4.1830E-12
    R = R0 * (1 + a * (T - T0) + b * (T - T0)**2 + c * (T - T0 - 100) * (T - T0)**3)
    return R


class updateprogress(object):
    """docstring for updateprogress"""
    
    def __init__(self, maxval):
        super(updateprogress, self).__init__()
        self.maxval = maxval
        self.printevery = float(self.maxval) / 100
        import imp
        try:
            imp.find_module('progressbar')
            self.useprogressbar = True
        except ImportError:
            self.useprogressbar = False
    
    def _printupdate(self, addstring=''):
        def _makepercent(num, tot, exact=False):
            'returns an integer representing num/tot as a percentage'
            exactvalue = float(num) * 100 / float(tot)
            return exactvalue if exact else int(exactvalue)
        
        print 'on {0} out of {1} ({2}%){3}'.format(self.counter, self.maxval, _makepercent(self.counter, self.maxval), addstring)
    
    def start(self):
        self.counter = 0
        if self.useprogressbar:
            import progressbar
            self.progbar = progressbar.ProgressBar(maxval=self.maxval,
                                                   widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage() ]
                                                   )
            self.progbar.start()
        else:
            self._lastprintupdate = 0
            print 'tracking progress'
            self._printupdate()
    
    def update(self, i):
        self.counter = i
        if self.useprogressbar:
            self.progbar.update(i)
        else:
            if self.counter - self._lastprintupdate >= self.printevery or (self.counter < self._lastprintupdate):
                self._printupdate()
                self._lastprintupdate = self.counter
    
    def finish(self):
        if self.useprogressbar:
            self.progbar.finish()
        else:
            self._printupdate(' (finished)')


def progbar_makestart(maxval):
    thebar = updateprogress(maxval)
    thebar.start()
    return thebar


def save_plot_fit_4D(filetag, x, data, totalPdf, yields, outdir, binning=30, savevalues=False):
    def outtext(outputtext):
        print outputtext
        return outputtext + '\n'
    
    import ROOT

    textf = outtext('\n' + filetag + "_" + data.GetTitle() + "_" + x.GetName() + ":")
    valdict = {}

    # make frame
    print 'save_plot_fit_4D(): making ' + x.GetName() + ' frame'
    framex = x.frame()
    # plot data
    print 'save_plot_fit_4D(): plotting data'
    data.plotOn(framex, ROOT.RooFit.Name("Hist"), ROOT.RooFit.MarkerColor(ROOT.kBlack), ROOT.RooFit.LineColor(ROOT.kBlack), ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2), ROOT.RooFit.Binning(binning))
    # plot totalPdf
    print 'save_plot_fit_4D(): plotting the total PDF'
    totalPdf.plotOn(framex, ROOT.RooFit.Normalization(1.0, ROOT.RooAbsReal.RelativeExpected), ROOT.RooFit.LineColor(ROOT.kBlue), ROOT.RooFit.Name("curvetot"))
    # create legend
    print 'save_plot_fit_4D(): creating legend'
    # leg = ROOT.TLegend(0.2, 0.5, .4, .9)
    # leg = ROOT.TLegend(0.2, 0.02, .4, .42)
    # leg = ROOT.TLegend(0.75, 0.5, 1, .9)
    leg = ROOT.TLegend(0.6, 0.5, 0.85, .9)
    # leg = ROOT.TLegend(0.3, 0.6, 0.6, .9)
    leg.SetTextSize(0.06)
    leg.AddEntry(framex.findObject("curvetot"), "Total PDF", "l")
    # iterate over totalPdf components
    print 'save_plot_fit_4D(): plotting components'
    icol = 0  # color index
    itertPC = totalPdf.getComponents().createIterator()
    vartPC  = itertPC.Next()
    while vartPC:
        # check if this shape is based on ROOT.RooRealVar x
        isx = False
        it = vartPC.getVariables().createIterator()
        v = it.Next()
        while v:
            vname = v.GetName()
            xname = x.GetName()
            if(vname == xname):
                isx = True
            v = it.Next()
        if 'totalPdf' in vartPC.GetName() or 'Projection' in vartPC.GetName() or not isx or ":" in vartPC.GetTitle() or "@" in vartPC.GetTitle():
            # skip totalPdf itself, plotted above
            # only for non-sub-shapes
            vartPC = itertPC.Next()
            continue
        print 'save_plot_fit_4D(): getting parameters for ' + vartPC.GetTitle()
        itercompPars = vartPC.getParameters(data).createIterator()  # set of the parameters of the component the loop is on
        varcompPars = itercompPars.Next()
        while varcompPars:
            # write and print mean, sig, etc. of sub-shapes
            hi = varcompPars.getErrorHi()
            varerrorstring = "[exact]"
            if(hi != -1):
                lo = varcompPars.getErrorLo()
                varerror = ROOT.TMath.Max(ROOT.TMath.Abs(lo), hi)
                varerrorstring = repr(round(varerror, 3))

            outputtext = varcompPars.GetTitle() + " = " + repr(round(varcompPars.getVal(), 3)) + " +/- " + varerrorstring
            textf += outtext(outputtext)

            valdict[varcompPars.GetName()] = varcompPars.getVal()

            varcompPars = itercompPars.Next()
        # plot sub-shapes and add to legend
        while icol in [0, 10, 4, 1, 5] + range(10, 28):
            icol += 1  # avoid white and blue and black and yellow and horribleness
        print 'save_plot_fit_4D(): plotting ' + vartPC.GetTitle()
        totalPdf.plotOn(framex,
                        ROOT.RooFit.Normalization(1.0, ROOT.RooAbsReal.RelativeExpected),
                        ROOT.RooFit.Name(vartPC.GetName()),
                        ROOT.RooFit.LineStyle(ROOT.kDashed),
                        ROOT.RooFit.LineColor(icol),
                        ROOT.RooFit.Components(vartPC.GetName())
                        )
        leg.AddEntry(framex.findObject(vartPC.GetName()), vartPC.GetTitle(), "l")
        icol += 1
        vartPC = itertPC.Next()
        itercompPars.Reset()  # make sure it's ready for the next vartPC

    # Calculate chi2/ndf
    print 'save_plot_fit_4D(): calculating chi2'
    floatpar = totalPdf.getParameters(data)
    floatpars = (floatpar.selectByAttrib("Constant", ROOT.kFALSE)).getSize()
    chi2 = framex.chiSquare("curvetot", "Hist", floatpars)
    chi2string = repr(round(chi2, 3))
    outputtext = "#chi^{2}/N_{DoF} = " + chi2string
    textf += outtext(outputtext)

    # Print stuff
    print 'save_plot_fit_4D(): getting yields'
    Y = []
    E = []  # holds yields and associated errors
    YS = []
    ES = []  # holds strings of the corresponding yields
    j = 0  # count list position
    iteryields = yields.createIterator()
    varyields = iteryields.Next()
    while varyields:  # loop over yields
        varval = varyields.getVal()
        Y.append(varval)
        lo = varyields.getErrorLo()
        hi = varyields.getErrorHi()
        E.append(ROOT.TMath.Max(ROOT.TMath.Abs(lo), hi))
        YS.append(repr(round(Y[j], 3)))
        ES.append(repr(round(E[j], 3)))

        outputtext = varyields.GetTitle() + " = " + YS[j] + " +/- " + ES[j]
        textf += outtext(outputtext)

        j += 1
        varyields = iteryields.Next()

    # Create canvas and pads, set style
    print 'save_plot_fit_4D(): creating canvas'
    c1 = ROOT.TCanvas("c1", "data fits", 1200, 800)
    pad1 = ROOT.TPad("pad1", "pad1", 0.0, 0.3, 1.0, 1.0)
    pad2 = ROOT.TPad("pad2", "pad2", 0.0, 0.0, 1.0, 0.3)
    pad1.SetBottomMargin(0)
    pad2.SetTopMargin(0)
    pad2.SetBottomMargin(0.5)
    pad2.SetBorderMode(0)
    pad1.SetBorderMode(0)
    c1.SetBorderMode(0)
    pad2.Draw()
    pad1.Draw()
    pad1.cd()
    # framex.SetMinimum(1)
    # framex.SetMaximum(7500)

    framex.addObject(leg)  # add legend to frame

    ROOT.gPad.SetTopMargin(0.06)
    # pad1.SetLogy()
    # pad1.Range(4100,0,6100,0.0005)
    pad1.Update()
    print 'save_plot_fit_4D(): drawing'
    framex.Draw()

    # Pull distribution
    framex2 = x.frame()
    hpull = framex.pullHist("Hist", "curvetot")
    framex2.addPlotable(hpull, "P")
    hpull.SetLineColor(ROOT.kBlack)
    hpull.SetMarkerColor(ROOT.kBlack)
    framex2.SetTitle("")
    framex2.GetYaxis().SetTitle("Pull")
    framex2.GetYaxis().SetTitleSize(0.15)
    framex2.GetYaxis().SetLabelSize(0.15)
    framex2.GetXaxis().SetTitleSize(0.2)
    framex2.GetXaxis().SetLabelSize(0.15)
    framex2.GetYaxis().CenterTitle()
    framex2.GetYaxis().SetTitleOffset(0.45)
    framex2.GetXaxis().SetTitleOffset(1.1)
    framex2.GetYaxis().SetNdivisions(505)
    framex2.GetYaxis().SetRangeUser(-8.8, 8.8)
    pad2.cd()
    framex2.Draw()

    return c1, textf, valdict


def save_plot_fit_4D_main(filetag, variables, dtys, outdir, plot2D=False, savevalues=False, binning=34):
    """
    filetag is used for filenaming
    variables is a list of RooRealVars
    dtys is a list of tuples, e.g., [(dataRS,totalPdfRS,yieldsRS),(dataWS,totalPdfWS,yieldsWS)]
    """
    import os
    from os.path import join as opj
    if plot2D and not len(variables) == 2:
        raise ValueError('plot2D with ' + str(len(variables)) + '?')
    if not os.path.exists(opj(outdir, "cfiles")):
        os.makedirs(opj(outdir, "cfiles"))
    tstring = ""
    if savevalues:
        valfile = file(opj(outdir, 'fit' + filetag + '_dictionaries.py'), 'w')
    for data, totalPdf, yields in dtys:
        if savevalues:
            valfile.write(data.GetName() + "_" + totalPdf.GetName() + "_dict = {\n")

        for var in variables:
            print "save_plot_fit_4D(" + var.GetName() + "," + data.GetName() + ")..."

            c, t, v = save_plot_fit_4D(filetag, var, data, totalPdf, yields, outdir, binning=binning, savevalues=savevalues)

            tstring += t

            if var == variables[0] and (data, totalPdf, yields) == dtys[0] and not (len(variables) == 1 and len(dtys) == 1):
                endm = "("
            elif var == variables[-1] and (data, totalPdf, yields) == dtys[-1] and not (len(variables) == 1 and len(dtys) == 1):
                endm = ")"
            else:
                endm = ""
            c.Print(opj(outdir, "fit" + filetag + ".pdf" + endm))
            c.SaveAs(opj(outdir, "cfiles", "fit" + filetag + "_" + data.GetTitle() + "_" + var.GetName() + ".C"))

            if savevalues:
                for key, val in v.iteritems():
                    valfile.write("'" + key + "':" + repr(val) + ',\n')

            print "done"
        if savevalues:
            valfile.write('}\n')

    with open(opj(outdir, "fit" + filetag + ".txt"), 'w') as tfile:
        # tfile.write(tstring)
        tlines = tstring.split('\n')
        lines_seen = []
        for line in tlines:
            if line not in lines_seen:
                tfile.write(line + '\n')
                if line != '':
                    lines_seen.append(line)

    if(plot2D):
        import ROOT
        for data, totalPdf, yields in dtys:
            print "making 2D histogram..."
            x = variables[0]
            y = variables[1]
            h2D = totalPdf.createHistogram("h2D", x, ROOT.RooFit.YVar(y))
            h2Dd = data    .createHistogram(x, y, 48, 36)
            c = ROOT.TCanvas("c", "2D histogram", 1200, 800)
            c.Divide(2)
            c.cd(1)
            h2Dd.Draw("lego")
            c.cd(2)
            h2D .Draw("surf")
            usefiletag = filetag + "_" + data.GetTitle()
            c.SaveAs(opj(outdir, "fit" + usefiletag + "_2D.pdf"))
            c.SaveAs(opj(outdir, "cfiles", "fit" + usefiletag + "_2D.C"  ))
            print "done"


def makeRooList(itm):
    'calls itm.createIterator() and loops it into a list'
    retlist = []
    itritm = itm.createIterator()
    v = itritm.Next()
    while v:
        retlist.append(v)
        v = itritm.Next()
    return retlist


def fileno(file_or_fd):
    'see https://stackoverflow.com/a/22434728/4655426'
    fd = getattr(file_or_fd, 'fileno', lambda: file_or_fd)()
    if not isinstance(fd, int):
        raise ValueError("Expected a file (`.fileno()`) or a file descriptor")
    return fd


@contextmanager
def stdout_redirected(to=os.devnull, stdout=None):
    """redirects 'stdout' to 'to'
    see https://stackoverflow.com/a/22434728/4655426
    """
    if stdout is None:
        stdout = sys.stdout

    stdout_fd = fileno(stdout)
    # copy stdout_fd before it is overwritten
    # NOTE: `copied` is inheritable on Windows when duplicating a standard stream
    with os.fdopen(os.dup(stdout_fd), 'wb') as copied:
        stdout.flush()  # flush library buffers that dup2 knows nothing about
        try:
            os.dup2(fileno(to), stdout_fd)  # $ exec >&to
        except ValueError:  # filename
            with open(to, 'wb') as to_file:
                os.dup2(to_file.fileno(), stdout_fd)  # $ exec > to
        try:
            yield stdout  # allow code to be run with the redirected stdout
        finally:
            # restore stdout to its previous value
            # NOTE: dup2 makes stdout_fd inheritable unconditionally
            stdout.flush()
            os.dup2(copied.fileno(), stdout_fd)  # $ exec >&copied


def merged_stderr_stdout():  # $ exec 2>&1
    """Useage:
    with stdout_redirected(to="file.log"), merged_stderr_stdout():
        <do something>
    see https://stackoverflow.com/a/22434728/4655426
    """
    return stdout_redirected(to=sys.stdout, stdout=sys.stderr)


class addsyspath:
    """Useage:
    with addsyspath(path):
        from x import y
    
    adds path to sys.path, enabling module imports
    based on https://stackoverflow.com/a/47518468/4655426
    """
    import sys
    
    def __init__(self, path):
        self.path = path
        self.index = None
    
    def __enter__(self):
        sys.path.append(self.path)
        self.index = len(sys.path) - 1
    
    def __exit__(self, *args):
        sys.path.pop(self.index)


def printcans(outfilename, clist):
    'creates a multi-page PDF of the canvases in clist'
    for c in clist:
        if len(clist) == 1:
            app = ''
        elif c is clist[0]:
            app = '('
        elif c is clist[-1]:
            app = ')'
        else:
            app = ''
        c.Print(outfilename + app)


def logical_combine(one, sym, two):
    'combines `one` and `two` using parentheses to enable logically consistent combination chains'
    return '({one}) {sym} ({two})'.format(one=one, sym=sym, two=two)


def stdpull(fr):
    'make standard pull plot adjustments for RooFit frame'
    fr.SetTitle('')
    fr.GetYaxis().SetTitle('Pull')
    fr.GetYaxis().CenterTitle()
    fr.GetYaxis().SetTitleSize(0.1)
    fr.GetYaxis().SetTitleOffset(0.3)
    fr.GetYaxis().SetLabelSize(0.10)
    fr.GetYaxis().SetNdivisions(505)
    fr.GetXaxis().SetLabelSize(0.10)
    fr.GetXaxis().SetTitle()
