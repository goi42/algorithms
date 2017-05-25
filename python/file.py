import sys
from ROOT import TTree,TFile
from fch import *

class file(fch):
    def __init__(self,location,name=None,tree=None,quality=None,):
        fch.__init__(self)
        self.file = TFile.Open(location)
        self.location = location
        if name: self.set_name(name)
        if tree: self.add_tree(tree)
        if quality: self.set_quality(quality)
    def add_tree(self,trname):
        temptree = TTree()
        self.file.GetObject(trname,temptree)
        self.t.append(temptree)
        self.tname.append(trname)
    def GetListOfBranches(self):
        if not self.check_tsize_1():
            print "file.GetListOfBranches() is only available for objects with only one tree."
            sys.exit()
        return self.t[0].GetListOfBranches()
    def GetNbranches(self):
        if not self.check_tsize_1():
            print "file.GetNbranches() is only available for objects with only one tree."
            sys.exit()
        return self.t[0].GetNbranches()
    def GetMaximum(self,bname):
        if not self.check_tsize_1():
            print "file.GetMaximum() is only available for objects with only one tree."
            sys.exit()
        return self.t[0].GetMaximum()
    def GetMinimum(self,bname):
        if not self.check_tsize_1():
            print "file.GetMinimum() is only available for objects with only one tree."
            sys.exit()
        return self.t[0].GetMinimum()
    def Draw(self,varexp,acut="",opt=""):
        if self.can_Draw():
            self.t[0].Draw(varexp,acut,opt)
