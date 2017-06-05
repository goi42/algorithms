import sys
from branch import *
from cut import *

class fch: #abstract base class for file and chain classes
    def __init__(self):
        self.name="" #nickname for the file or chain
        self.quality = {} #handy for comparing files, e.g., quality["year"]="2015"
        self.t=[]
        self.tname=[]
        self.b=[]
        self.c=[]#cuts to be applied to the file
        self.thething = None #should be set to a tree for file and the chain for chain

    def set_name(self,name):
        self.name = name
    def set_quality(self,quality):
        self.quality = quality
    def add_branch(self,Branch,Name=None,nBins=None,loBin=None,hiBin=None):
        self.b.append(branch(Branch,Name,nBins,loBin,hiBin))
    def add_cut(self,Cut,Name=None):
        self.c.append(cut(Cut,Name))
    def GetNtrees(self):
        if len(self.t) != len(self.tname):
            print repr(self.name)+" has "+len(t)+" trees but "+len(tname)+" tree names. How did this happen?"
            sys.exit()
        return len(self.t)
    def check_tsize_1(self):
        if self.GetNtrees()==1:
            return True
        else:
            print repr(self.name)+" has a tree list with "+repr(self.GetNtrees())+" trees."
            return False
    def file_1tree_check(self,fname):
        if self.thething.__class__.__name__=='file':
            if not self.check_tsize_1():
                print "file."+fname+" is only available for objects with only one tree."
                sys.exit()
    def can_Draw(self):
        if self.check_tsize_1():
            return True
        else:
            print "fch::Draw is only available for objects with just one associated tree."
    def GetListOfBranches(self):
        self.file_1tree_check("GetListOfBranches")
        temp = []
        for nm in self.thething.GetListOfBranches():
            temp.append(nm.GetName())
        return temp
    def GetNbranches(self):
        self.file_1tree_check("GetNbranches")
        return self.thething.GetNbranches()
    def GetMaximum(self,brname):
        self.file_1tree_check("GetMaximum")
        return self.thething.GetMaximum(brname)
    def GetMinimum(self,brname):
        self.file_1tree_check("GetMinimum")
        return self.thething.GetMinimum(brname)
    def Draw(self,varexp,acut="",opt=""):
        if self.can_Draw():
            self.thething.Draw(varexp,acut,opt)

