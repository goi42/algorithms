import sys
from ROOT import TTree,TFile
from myfch import *

class myfile(myfch):
    def __init__(self,location,name=None,tree=None,quality=None,opencondition='READ'):
        myfch.__init__(self)
        self.file = TFile.Open(location,opencondition)
        self.location = location
        if name: self.set_name(name)
        if tree: self.add_tree(tree)
        if quality: self.set_quality(quality)
    def __getattr__(self,name):
        return getattr(self.file,name)
    def add_tree(self,trname):
        temptree = TTree()
        self.file.GetObject(trname,temptree)
        self.t.append(temptree)
        self.tname.append(trname)
        if(self.check_tsize_1()):
            self._thething = self.t[0]
    def GetTree(self,trname=''):
        if trname == '':
            self.file_1tree_check('GetTree')
            return self._thething
        else:
            for tr in self.t:
                if trname == tr.GetName():
                    return tr
    
