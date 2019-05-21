#!/usr/bin/python
'''
example usage:
    (in directory containing makeplots_layer.py:)
    python ~/algorithms/python/makeplots_main.py --verbose

This compares any number of layers on any number of plots. It needs to be passed a list of layers, which it imports from a file called makeplots_layer.py. Such a file need only declare (and fill) a list of layers called L. This script handles all the sorting logic and plot making. It takes arguments as described in makeplots_parser.py, one of which specifies the directory containing makeplots_layer.py. Overall, this architecture should make things much cleaner as this script should be able to reside undisturbed in this directory while users (*ahem* just me *ahem*) will only have to modify/create project-specific makeplots_layer.py scripts.

I say it can compare any number of layers. It should be able to--the C++ code it was adapted from could. But I've made some small changes to the layer class (specifically, the element list no longer just holds names but an actual list of items--this change allows this script simply to import the layer list L without having to worry about anything else), and while I know it still compares files, branches, and cuts just fine, I haven't tried it out with anything more complicated. (Things like having multiple files from various years and comparing years, for instance.)

It suffers from a need for all files to have the same number of branches and all branches to have the same number of cuts.

Elements of its logic are very C++-like, an artifact from its original design. I haven't wanted to rethink the logic yet, nor have I needed to.
'''
# import
from makeplots_parser import *  # up here to make sure --help works

import sys
import os
import math
import subprocess
import progressbar
import time
import threading

import ROOT
from ROOT import TLegend, TFile, THStack, TCanvas
from myROOTtypes.branch import branch
from myROOTtypes.cut import cut
from myROOTtypes.file import file
from myROOTtypes.chain import chain
from myROOTtypes.layer import layer
from fxns import addsyspath, progbar_makestart, do_ROOT_multithreading

with addsyspath(pathtolayerfile):
    from makeplots_layer import L

ROOT.gROOT.SetBatch(True)
if(not debug):
    ROOT.gErrorIgnoreLevel = ROOT.kWarning
if not nomultithreading:
    do_ROOT_multithreading()
if lhcbStyle:
    ROOT.gROOT.ProcessLine('.x lhcbStyle.C')

print '---------------------------makeplots_main.py---------------------------'
print 'starting at', time.asctime(time.localtime(time.time()))
print 'using layer input from ' + pathtolayerfile
print 'will save plots using option "' + drawopt + '" to', os.path.join(outputlocation, filename)
if(histograms):
    print 'will create histogram file', os.path.join(outputlocation, hfilename)
if(verbose and not debug):
    print 'verbose mode set'
if(debug):
    print 'debug mode set'
print ''

# -------assign layers, etc.---------#
if(verbose):
    print "assigning layers...",

CutLayerExists = False
while not CutLayerExists:
    nhpc = nCanvases = int(1)  # actual values assigned below
    fL = bL = cL = int(0)  # actual values assigned below
    for iLayer in L:
        # assign layers this is not an algorithm
        if(iLayer.name == "file" or iLayer.name == "chain"):
            fL = L.index(iLayer)
        elif(iLayer.name == "branch"):
            bL = L.index(iLayer)
        elif(iLayer.name == "cut"):
            CutLayerExists = True
            cL = L.index(iLayer)
        # calculate nhpc and nCanvases
        if(iLayer.compared):
            nhpc *= iLayer.nL
        else:
            nCanvases *= iLayer.nL
    if(not CutLayerExists):
        print 'No cut layer given. Generating...',
        for ifile in L[fL].element:
            for ibranch in ifile.b:
                ibranch.c = [cut("", "no additional cuts")]
        L.append(layer(L[fL].element[0].b[0].c))
        print 'done.'
if(verbose):
    print "done"
nLayers = len(L)
nFiles, nBranches, nCuts = len(L[fL].element), len(L[bL].element), len(L[cL].element)
print "nFiles = {nFiles}, nBranches = {nBranches}, nCuts = {nCuts}".format(nFiles=nFiles, nBranches=nBranches, nCuts=nCuts)
print "nLayers = {nLayers}, nCanvases = {nCanvases}, nhpc = {nhpc}".format(nLayers=nLayers, nCanvases=nCanvases, nhpc=nhpc)

if(histograms or savecan):
    if(verbose):
        print "creating histogram/canvas file {0}...".format(hfilename),
    hfile = TFile(os.path.join(outputlocation, hfilename), "recreate")  # assigned here
    if(verbose):
        print "done"
# create necessary counters, canvases, legends, etc.
if(verbose):
    print "\ncreating canvasy things...",
cf = TCanvas("cf", "combined")  # canvas to hold everything
cf.DivideSquare(nCanvases)  # canvas divided to be able to hold all other canvases
# calculate plL (product of lower layers) (helps iterate L[i].Li)
# this name made more sense when the order layers were specified mattered
# now, compared layers must iterate most frequently and non-compared less frequently
# (the if statements mean the user can specify what layers to use in any order
#        instead of just iterating the last most frequently)
# plLx (product of lower layers exclusive) helps determine which file we're using
for i in xrange(0, nLayers):  # the following is very C++, but I haven't rethought the logic yet
    for j in xrange(nLayers - 1, i, -1):
        if(not L[i].compared):  # non-compared need product of all lower levels
            L[i].plL *= L[j].nL
            if(not (L[j].name == "cut" or L[j].name == "branch")):
                L[i].plLx *= L[j].nL
        elif(L[j].compared):  # compared need product of all lower compared levels
            L[i].plL *= L[j].nL
            if(not(L[j].name == "cut" or L[j].name == "branch")):
                L[i].plLx *= L[j].nL
    if(not L[i].compared):  # non-compared need product of all higher compared levels
        for k in xrange(0, i):
            if(L[k].compared):
                L[i].plL *= L[k].nL
                if(not (L[k].name == "cut" or L[k].name == "branch")):
                    L[i].plLx *= L[k].nL
pli = int(0)  # this counts the number of plots generated helps iterate L[i].Li
if(verbose):
    print "done"
# ------------done-----------#

# ---------------declare and fill histograms (maybe)---------------#
if not doDraw:
    print '\nstarting histogram declaration loop...'
    hbar = progbar_makestart(nFiles * nBranches * nCuts)
    i = 0
    for ifile in L[fL].element:
        for ibranch in ifile.b:
            for icut in ibranch.c:
                icut.make_histogram(ifile, ibranch, return_histogram=False)
                icut.format_histogram(b=ibranch, sumw2=not nosumw2)  # preliminary stuff here, more below
                i += 1
                hbar.update(i)
    hbar.finish()
    
    class myThread(threading.Thread):
        def __init__(self, f):
            threading.Thread.__init__(self)
            self.f = f
            self.Nents = f.GetEntries()
            self.prog = 0
        
        def run(self):
            for ievt, evt in enumerate(self.f.GetTree()):
                for ibranch in self.f.b:
                    for icut in ibranch.c:
                        icut.fill_histogram(evt, ibranch)
                self.prog = ievt + 1
    
    print '\ngetting entries...'
    threads = []
    for ifile in L[fL].element:
        threads.append(myThread(ifile))
    nEntries = sum(x.Nents for x in threads)
    print 'starting histogram fill loops over {} entries...'.format(nEntries)
    fillbar = progbar_makestart(nEntries)
    Nth_at_once = len(threads) if len(threads) < 5 else 5
    startedthreads = []
    while len(startedthreads) < len(threads) or any(  # start all threads
        [th.isAlive() for th in threads]  # wait for them to finish
    ):
        for th in [x for x in threads if x not in startedthreads]:
            runningthreads = [x for x in threads if x.isAlive()]
            if len(runningthreads) < Nth_at_once:
                th.start()
                startedthreads.append(th)
            else:
                break
        fillbar.update(sum(x.prog for x in threads))
        time.sleep(0.001)
    fillbar.finish()
# ---------------done----------------------------------------------#

# ------------------------------------canvas loop-----------------------------#
print "\nstarting canvas loop..."
# actual start of the loop
canbar = histbar = None  # choose which/whether to use
if(not debug):
    if(nhpc > nCanvases):
        histbar = True
    else:
        canbar = progbar_makestart(nCanvases)
hs = []
for ci_i in range(0, nCanvases):  # ci in c:
    if(debug):
        print "On canvas {i} out of {n}".format(i=ci_i + 1, n=nCanvases)
    # create necessary canvasy things
    ci = TCanvas("c" + str(ci_i), "c" + str(ci_i), 1200, 800)  # create the canvases
    ci.cd()
    ROOT.gStyle.SetOptStat(setoptstat)
    if not buildlegend:
        leg = TLegend(legpars[0], legpars[1], legpars[2], legpars[3])
        leg.SetFillStyle(0)  # transparent legend
    
    hs.append(THStack("hs" + str(ci_i), "hs" + str(ci_i)))  # create the stack to hold the histograms
    
    stacktitle = ""
    # histogram loop
    if(histbar is not None):
        print 'starting histogram loop for canvas {0} out of {1}...'.format(ci_i + 1, nCanvases)
        histbar = progbar_makestart(nhpc)
    for hi in xrange(0, nhpc):
        # decide which file to use
        file_num = 0
        for Li in L:
            if(not (Li.name == "cut" or Li.name == "branch")):  # cuts and branches do not get their own files
                file_num += Li.Li * Li.plLx
        if(debug):
            print "creating strings and pointers for histogram loop {i}/{n}...".format(i=hi + 1, n=nhpc),
        # create convenient pointers
        thisfile = L[fL].element[file_num]
        thisbranch = thisfile.b[L[bL].Li]
        assocbranch = thisbranch.associated_branch
        if(assocbranch and debug):
            print thisbranch.name, 'has associated branch', assocbranch.name
        thiscut = thisbranch.c[L[cL].Li]
        if(debug):
            print "done"
        # create histogram
        if(debug):
            print "creating histogram {0}...".format(hi + 1),
        listofthings = (thiscut, thisbranch, thisfile)
        if(any(x.linecolor is not None for x in listofthings)):
            foundlc = False
            for th in listofthings:
                if(th.linecolor and not foundlc):
                    linecolor = th.linecolor
                    foundlc = True
                elif(th.linecolor and not foundlc):
                    raise ValueError('cannot assign a linecolor for multiple types of things!')
        else:
            linecolor = hi + 1
            if((hi + 1 == 5) or (hi + 1 == 10)):
                linecolor = hi + 21
        markercolor = None
        if(markerlinecolors):
            markercolor = linecolor
        elif(any(x.markercolor is not None for x in listofthings)):
            foundfc = False
            for th in listofthings:
                if(th.markercolor and not foundfc):
                    markercolor = th.markercolor
                    foundfc = True
                elif(th.markercolor and not foundfc):
                    raise ValueError('cannot assign a markercolor for multiple types of things!')
        fillcolor = None
        if(filllinecolors):
            fillcolor = linecolor
        elif(any(x.fillcolor is not None for x in listofthings)):
            foundfc = False
            for th in listofthings:
                if(th.fillcolor and not foundfc):
                    fillcolor = th.fillcolor
                    foundfc = True
                elif(th.fillcolor and not foundfc):
                    raise ValueError('cannot assign a fillcolor for multiple types of things!')
        fillstyle = None
        if(any(x.fillstyle is not None for x in listofthings)):
            foundfs = False
            for th in listofthings:
                if(th.fillstyle and not foundfs):
                    fillstyle = th.fillstyle
                    foundfs = True
                elif(th.fillstyle and not foundfs):
                    raise ValueError('cannot assign a fillstyle for multiple types of things!')
        
        if(hs[ci_i].GetHists() and fixbinning):
            if(debug):
                print 'forcing branch to match previous one...',
            lasthistaxis = hs[ci_i].GetHists()[-1].GetXaxis()
            thisbranch.nBins = lasthistaxis.GetNbins()
            thisbranch.loBin = lasthistaxis.GetXmin()
            thisbranch.hiBin = lasthistaxis.GetXmax()
            if(debug):
                print 'done'
        if doDraw:
            thish = thisbranch.make_histogram(hname="h" + str(ci_i) + str(hi), linecolor=linecolor, markercolor=markercolor, fillcolor=fillcolor, fillstyle=fillstyle, overwrite=True, return_histogram=True, sumw2=not nosumw2)  # linecolor is ignored for 2D histograms by make_histogram
            # draw histograms
            if(verbose):
                print "drawing histogram {i}...".format(i=hi + 1),
            thisfile.Draw(thisbranch, thiscut, drawopt, canvas=ci)
            if(verbose):
                print "done"
        else:
            thiscut.format_histogram(linecolor=linecolor, fillcolor=fillcolor, fillstyle=fillstyle, b=thisbranch, sumw2=False, set_can_extend=False)  # linecolor is ignored for 2D histograms by format_histogram
            thish = thiscut.h
            if(thiscut.hdims == 1):
                if(thisbranch.set_log_X):
                    ci.SetLogx()
                if(thisbranch.set_log_Y):
                    ci.SetLogy()
            elif(thiscut.hdims == 2):
                if(thisbranch.set_log_X):
                    ci.SetLogx()
                if(assocbranch.set_log_X):
                    ci.SetLogy()
                if(thisbranch.set_log_Y or assocbranch.set_log_Y):
                    ci.SetLogz()
            else:
                raise Exception('{0} has neither 1 nor 2 hdims?'.format(thiscut.name))
        
        # clone histograms
        if(verbose):
            print "cloning histogram {i}...".format(i=hi + 1),
        h = thish.Clone()
        if(verbose):
            print "done"
        pli += 1  # iterate the number of plots that have been drawn
        
        if(histograms):
            if(verbose):
                print "saving histogram {i}...".format(i=hi + 1),
            hfile.cd()
            thish.Write()
            if(verbose):
                print "done"
            ci.cd()
        if(norm):
            if(verbose):
                print "normalizing histogram {i}...".format(i=hi + 1),
            h.Scale(1 / h.Integral())
            if(verbose):
                print "done"
        if(verbose):
            print "stacking histogram {i}...".format(i=hi + 1),
        hs[ci_i].Add(h)  # stack histograms
        if(verbose):
            print "done"

        # loop over layers
        if(verbose):
            print "creating legend {i}...".format(i=hi + 1),
        leglabel = ""
        for Li in L:
            # determine the name of the stack title
            Ltitle = Li.element[Li.Li].name
            if(Li.name == 'branch' and Li.element[Li.Li].associated_branch):
                Ltitle = Li.element[Li.Li].associated_branch.name + ' vs. ' + Ltitle
            if(Li.compared):  # compared layers in the legend entry
                if(leglabel != ""):
                    leglabel += ", "
                leglabel += Ltitle
            elif(hi == 0):  # since stacktitle reflects non-compared layers, it only needs to change per canvas
                if(stacktitle != ""):
                    stacktitle += ": "
                stacktitle += Ltitle  # non-compared goes in title

            # iterate layer counters
            if(Li.plL == 1):
                Li.Li += 1  # if it's at the lowest hierarchy, iterate
            elif((pli % Li.plL == 0) and (pli != 0)):
                Li.Li += 1  # if all variations of plots lower than it have been plotted, iterate
            if(Li.Li == Li.nL):
                Li.Li = 0  # reset the iteration if it's reached the end
        # end layer loop
        # fill legends
        if(leglabel != "" and not buildlegend):
            leg.AddEntry(h, leglabel)  # no need for a legend if nothing is compared
        if(verbose):
            print "done"
        if(histbar is not None):
            histbar.update(hi + 1)
    # end histogram loop
    if(histbar is not None):
        histbar.finish()
    # draw stacked histograms
    if(verbose):
        print "drawing stack {i}: {st}...".format(i=ci_i + 1, st=stacktitle),
    hs[ci_i].SetTitle(stacktitle)
    if(notitle):
        hs[ci_i].SetTitle('')
    placeholder = '' if yesstack else 'nostack'
    if(drawopt):
        placeholder += " " + drawopt  # turns out "nostack " is different than "nostack"...
    ci.cd()
    hs[ci_i].Draw(placeholder)
    if(assocbranch or labelaxes):
        placeholder = thisbranch.axname if thisbranch.axname else thisbranch.name
        if(thisbranch.units):
            placeholder += ' [{}]'.format(thisbranch.units)
        hs[ci_i].GetXaxis().SetTitle(placeholder)
        if(assocbranch):
            placeholder = assocbranch.axname if assocbranch.axname else assocbranch.name
            if(assocbranch.units):
                placeholder += ' [{}]'.format(assocbranch.units)
            hs[ci_i].GetYaxis().SetTitle(placeholder)
        else:
            placeholder = 'Entries / ({}{})'.format(
                thisbranch.get_bin_width(),
                (' ' + thisbranch.units) if thisbranch.units else '')
            hs[ci_i].GetYaxis().SetTitle(placeholder)
        ci.Update()
    if(not nolegend and not buildlegend and leg.GetNRows() > 0):  # you don't need a legend if nothing's compared
        leg.Draw()
    if(buildlegend):
        ci.BuildLegend()
    cf.cd(ci_i + 1)
    ci.DrawClonePad()
    if(verbose):
        print "done"
    # save stuff:
    if(verbose):
        print "saving files...",
    placeholder = os.path.join(outputlocation, filename)
    if(nCanvases > 1):
        placeholder += "("  # the closing page is added after the loop
    ci.Print(placeholder)
    if(saveC):
        ci.SaveAs(os.path.join(outputlocation, "c{i}_{st}.C".format(i=ci_i, st=stacktitle)))
    if(savecan):
        ci.Write()
    if(verbose):
        print "done\n"
    if(canbar is not None):
        canbar.update(ci_i)
# end canvas loop
if(canbar is not None):
    canbar.finish()
if(histograms or savecan):
    if(verbose):
        print "closing histogram/canvas file {hnm}...".format(hnm=hfilename),
    hfile.Close()
    if(verbose):
        print "done"
cf.cd()
if(nCanvases > 1):
    cf.Print(os.path.join(outputlocation, filename + ")"))
ROOT.gROOT.SetBatch(False)
print 'finished at', time.asctime(time.localtime(time.time()))
print "---------------------------done----------------------------------------"
