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
#import
import sys,os,math,subprocess
import ROOT
from ROOT import TLegend, TTree, TROOT, TRint, TFile, THStack, TH1, TH1F, TH2, TStyle, TCanvas, TVector3, TPaveStats, TString, TCut
#import local
from makeplots_parser import *
from branch import *
from cut import *
from file import *
from chain import *
from layer import *

ROOT.gROOT.SetBatch(True)

sys.path.insert(0,pathtolayerfile)
from makeplots_layer import L

print '---------------------------makeplots_main.py---------------------------'
print 'using layer input from '+pathtolayerfile
print 'will save plots using option "'+drawopt+'" to '+outputlocation+filename
if histograms: print 'will create histogram file '+outputlocation+hfilename
if verbose and not debug: print 'verbose mode set'
if debug: print 'debug mode set'
print ''

#-------assign layers, etc.---------#
if(verbose): print "assigning layers... ",

nLayers = len(L)
nhpc=int(1)#actual value assigned below
nCanvases=int(1)#actual value assigned below
fL=bL=cL=int(0)#actual value assigned below
for iLayer in L:
    #assign layers this is not an algorithm 
    if(iLayer.name=="file" or iLayer.name=="chain"):
        fL=L.index(iLayer)
    elif(iLayer.name=="branch"):
        bL=L.index(iLayer)
    elif(iLayer.name=="cut"):
        cL=L.index(iLayer)

    #calculate nhpc and nCanvases
    if(iLayer.compared): nhpc *= iLayer.nL
    else: nCanvases *= iLayer.nL
if(verbose): print "done"
print "nFiles = "+repr(len(L[fL].element))+", nBranches = "+repr(len(L[bL].element))+", nCuts = "+repr(len(L[cL].element))
print "nLayers = "+repr(nLayers)+", nCanvases = "+repr(nCanvases)+", nhpc = "+repr(nhpc)
#------------done-----------#

#------------------------------------canvas loop-----------------------------#
hfile = TFile() #declared here
if(histograms):
    if(verbose): print "creating histogram file"+hfilename+"...",
    placeholder=outputlocation+hfilename
    hfile = TFile(hfilename,"recreate")#assigned here
    if(verbose): print "done"
#create necessary counters, canvases, legends, etc.
if(verbose): print "\ncreating canvasy things... ",
#c = [TCanvas() for _ in range(nCanvases)] #each canvas holds one stack of histograms
cf = TCanvas("cf","combined") #canvas to hold everything
sqnc = math.sqrt(nCanvases)
sqncu = int(math.ceil(sqnc))
sqncd = int(math.floor(sqnc))
while(sqncu*sqncd<nCanvases): sqncu += 1
cf.Divide(sqncu,sqncd)#canvas divided to be able to hold all other canvases
#calculate plL (product of lower layers) (helps iterate L[i].Li)
#this name made more sense when the order layers were specified mattered
#now, compared layers must iterate most frequently and non-compared less frequently
#the if statements mean the user can specify what layers to use in any order
#        instead of just iterating the last most frequently
#plLx (product of lower layers exclusive) helps determine which file we're using
for i in xrange(0,nLayers): #the following is very C++, but I haven't rethought the logic yet
    for j in xrange(nLayers-1,i,-1):
        if(not L[i].compared): #non-compared need product of all lower levels
            L[i].plL*=L[j].nL
            if(not (L[j].name=="cut" or L[j].name=="branch")): L[i].plLx*=L[j].nL
        elif(L[j].compared): #compared need product of all lower compared levels
            L[i].plL*=L[j].nL
            if(not(L[j].name=="cut" or L[j].name=="branch")): L[i].plLx*=L[j].nL
    if(not L[i].compared): #non-compared need product of all higher compared levels
        for k in xrange(0,i):
            if(L[k].compared):
                L[i].plL*=L[k].nL
                if(not (L[k].name=="cut" or L[k].name=="branch")): L[i].plLx*=L[k].nL
pli=int(0) #this counts the number of plots generated helps iterate L[i].Li
if(verbose): print "done"
print "\nstarting canvas loop..."
#actual start of the loop
for ci_i in range(0,nCanvases): #ci in c:
    cistring = repr(ci_i) #repr(c.index(ci))
    print "On canvas "+repr(int(cistring)+1)+" out of "+repr(nCanvases)
    #create necessary canvasy things
    placeholder = "c"+cistring
    ci = TCanvas(placeholder,placeholder,1200,800) #create the canvases
    ci.cd()
    ROOT.gStyle.SetOptStat("")
    leg = TLegend(legpars[0],legpars[1],legpars[2],legpars[3])
    placeholder = "hs"+cistring
    hs = THStack(placeholder,placeholder) #create the stack to hold the histograms

    stacktitle=""
    #histogram loop
    for hi in xrange(0,nhpc):
        #decide which file to use
        file_num=0
        for Li in L:
            if(not (Li.name=="cut" or Li.name=="branch")):#cuts and branches do not get their own files
                file_num += Li.Li*Li.plLx
        if(debug): print "creating strings and pointers for histogram loop "+repr(hi+1)+"/"+repr(nhpc)+"... ",
        #create convenient strings
        histring = repr(hi)
        hname = "h"+cistring+histring
        #create convenient pointers
        thisfile = L[fL].element[file_num]
        thisbranch = thisfile.b[L[bL].Li]
        thiscut = thisbranch.c[L[cL].Li]
        if(debug): print "done"
        #create histogram
        if(verbose): print "creating histogram "+repr(hi+1)+"... ",
        binning_set = any([thisbranch.nBins,thisbranch.loBin,thisbranch.hiBin]) #was the binning specified above?
        if(not binning_set): #currently only considers whether all or no binning was specified could theoretically handle some
            thisbranch.nBins = 100
        h = TH1F(hname,thisbranch.name,thisbranch.nBins,thisbranch.loBin,thisbranch.hiBin)
        if(not binning_set or thisbranch.can_extend): h.SetCanExtend(TH1.kAllAxes)
        if(verbose): print "done"
        #draw histograms
        if(verbose): print "drawing histogram "+repr(hi+1)+"... ",
        h.SetLineColor(hi+1)
        if((hi+1==5) or (hi+1==10)): h.SetLineColor(hi+21)
        if(thisbranch.set_log_Y): #if any branches have this option set, draw them that way.
            ci.SetLogy()
        placeholder = thisbranch.branch+">>"+hname
        try:
            thisfile.Draw(placeholder,thiscut.cut,drawopt)#one tree per file
        except:
            print "Draw() failed for branch: "+thisbranch.name
            print "in file: "+thisfile.name
            print "with cut: "+thiscut.name
            print "Attempting to draw again..."
            h.SetCanExtend(TH1.kAllAxes)
            thisfile.Draw(placeholder,thiscut.cut,drawopt)#one tree per file	
        if(verbose): print "done"
        pli+=1 #iterate the number of plots that have been drawn

        if(histograms):
            if(verbose): print "saving histogram"+repr(hi+1)+"...",
            hfile.cd()
            h.Write()
            if(verbose): print "done"
            ci.cd()
        if(verbose): print "stacking histogram "+repr(hi+1)+"... ",
        hs.Add(h)#stack histograms
        if(verbose): print "done"

        #loop over layers
        if(verbose): print "creating legend "+repr(hi+1)+"... ",
        leglabel=""
        for Li in L:
            #determine the name of the stack title
            if(Li.compared):#compared layers in the legend entry
                if(leglabel!=""): leglabel+=", "
                leglabel+= Li.element[Li.Li].name
            elif(hi==0): #since stacktitle reflects non-compared layers, it only needs to change per canvas
                if(stacktitle!=""): stacktitle+=": "
                stacktitle+= Li.element[Li.Li].name #non-compared goes in title

            #iterate layer counters
            if(Li.plL==1): Li.Li+=1 #if it's at the lowest hierarchy, iterate
            elif((pli%Li.plL==0) and (pli!=0)): Li.Li+=1 #if all variations of plots lower than it have been plotted, iterate
            if(Li.Li==Li.nL): Li.Li=0 #reset the iteration if it's reached the end
        #end layer loop
        #fill legends
        leg.AddEntry(h,leglabel,"l")
        if(verbose): print "done"
    #end histogram loop
    #draw stacked histograms
    if(verbose): print "drawing stack "+repr(int(cistring)+1)+": "+stacktitle+"... ",
    hs.SetTitle(stacktitle)
    placeholder = "nostack"
    if drawopt: placeholder+=" "+drawopt #turns out "nostack " is different than "nostack"...
    hs.Draw(placeholder)
    if(leg.GetNRows()>0): leg.Draw() #you don't need a legend if nothing's compared
    cf.cd(int(cistring)+1)
    ci.DrawClonePad()
    if(verbose): print "done"
    #save stuff:
    if(verbose): print "saving files... ",
    placeholder = outputlocation+filename+"("#the closing page is added after the loop
    ci.Print(placeholder)
    if(saveC):
        placeholder = outputlocation+"c"+cistring+"_"+stacktitle+".C"
        ci.SaveAs(placeholder)
    if(verbose): print "done\n"
#end canvas loop
if(histograms):
    if(verbose): print "closing histogram file "+hfilename+"...",
    hfile.Close()
    if(verbose): print "done"
cf.cd()
placeholder = outputlocation+filename+")"
cf.Print(placeholder)
ROOT.gROOT.SetBatch(False)
print "---------------------------done---------------------------"
