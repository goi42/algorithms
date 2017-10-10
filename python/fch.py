import sys
from branch import *
from cut import *
from ROOT import TCanvas

class fch(bfch): #abstract base class for file and chain classes
    def __init__(self):
        self.name="" #nickname for the file or chain
        self.quality = {} #handy for comparing files, e.g., quality["year"]="2015"
        self.t=[]
        self.tname=[]
        self.b=[]
        self._thething = None #should be set to a tree for file and the chain for chain
        self.bMaxes = {}
        self.bMins  = {}
    # def __enter__(self):
    #     return self
    # def __exit__(self, exc_type, exc_value, traceback):
    #     self._thething.Delete()

    def set_name(self,name):
        self.name = name
    def set_quality(self,quality):
        self.quality = quality
    def add_branch(self,*args,**kwargs):
        if args[0].__class__.__name__=='branch':
                self.b += args
        else:
            self.b.append(branch(*args,**kwargs))
    def GetNtrees(self):
        if len(self.t) != len(self.tname):
            raise ValueError(repr(self.name)+" has "+repr(len(t))+" trees but "+repr(len(tname))+" tree names. How did this happen?")
        return len(self.t)
    def check_tsize_1(self):
        if self.GetNtrees()==1:
            return True
        else:
            print repr(self.name)+" has a tree list with "+repr(self.GetNtrees())+" trees."
            return False
    def file_1tree_check(self,fname):
        if self._thething.__class__.__name__=='file':
            if not self.check_tsize_1():
                raise NotImplementedError("file."+fname+" is only available for objects with only one tree.")
    def can_Draw(self):
        if self.check_tsize_1():
            return True
        else:
            raise NotImplementedError("fch::Draw is only available for objects with just one associated tree.")
    def GetListOfBranches(self):
        self.file_1tree_check("GetListOfBranches")
        temp = []
        for nm in self._thething.GetListOfBranches():
            temp.append(nm.GetName())
        return temp
    def GetNbranches(self):
        self.file_1tree_check("GetNbranches")
        return self._thething.GetNbranches()
    def GetMaximum(self,brname):
        self.file_1tree_check("GetMaximum")
        return self._thething.GetMaximum(brname)
    def GetMinimum(self,brname):
        self.file_1tree_check("GetMinimum")
        return self._thething.GetMinimum(brname)
    def GetbMaxMin(self,brlist=[]):
        self.file_1tree_check("GetMaxMin")
        bloop = []
        if not isinstance(brlist,list):
            raise TypeError("GetbMaxMin takes a _list_, not a "+brlist.__class__.__name__)
        if brlist:
            bloop = brlist
        elif self.b:
            for ib in self.b:
                bloop.append(ib.branch)
        else:
            bloop = self.GetListOfBranches()
        for bname in bloop:
            self.bMaxes[bname] = self.GetMaximum(bname)
            self.bMins [bname] = self.GetMinimum(bname)
    def GetEntries(self,selection):
        if isinstance(selection,str):
            p = selection
        elif isinstance(selection,cut):
            p = selection.cut.GetTitle()
        elif isinstance(selection,TCut):
            p = selection.GetTitle()
        else:
            raise TypeError('GetEntries requires a str, cut, or TCut, not a '+selection.__class__.__name__)
        return self._thething.GetEntries(p)
    def Draw(self,thisbranch,thiscut="",opt="",canvas=None):
        if self.can_Draw():
            btypepassed = thisbranch.__class__.__name__
            ctypepassed = thiscut.__class__.__name__
            if ctypepassed == 'cut': acut = thiscut.cut
            else: acut = thiscut

            if btypepassed == 'str' or btypepassed == 'TString': #if a string is passed
                self._thething.Draw(thisbranch,acut,opt)

            elif btypepassed == 'branch': #if a branch object is passed
                if not canvas: #make canvas
                    canvas = TCanvas(self.name,self.name,1200,800)
                    canvas.cd()
                if not thisbranch.h: thisbranch.make_histogram()
                thisbranch.h.Reset()
                h = thisbranch.h
                hname = h.GetName()
                assocbranch = thisbranch.associated_branch
                #draw histograms
                if not assocbranch:
                    #if any branches have these options set, draw them that way:
                    if(thisbranch.set_log_X): canvas.SetLogx()
                    if(thisbranch.set_log_Y): canvas.SetLogy()
                    placeholder = thisbranch.branch+">>"+hname
                else:
                    placeholder = assocbranch.branch+":"+thisbranch.branch+">>"+hname
                    if(thisbranch.set_log_X):  canvas.SetLogx()
                    if(assocbranch.set_log_X): canvas.SetLogy()
                    if(thisbranch.set_log_Y or assocbranch.set_log_Y): canvas.SetLogz()
                # try:
                self.Draw(placeholder,acut,opt)#one tree per file
                # except:
                #     print "Draw() failed for "+placeholder
                #     print "in file: "+self.name
                #     if ctypepassed == 'cut': placeholder2 = thiscut.name
                #     else: placeholder2 = thiscut
                #     print "with cut: "+placeholder2
                #     print "Attempting to draw again with extendable axes..."
                #     h.SetCanExtend(TH1.kAllAxes)
                #     thisfile.Draw(placeholder,acut,drawopt)#one tree per file
            else:
                raise TypeError
