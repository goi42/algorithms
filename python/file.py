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
        if(self.check_tsize_1()):
            self.thething = self.t[0]
