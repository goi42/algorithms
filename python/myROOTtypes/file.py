import sys
from ROOT import TTree, TFile
from fch import fch


class file(fch):
    def __init__(self, location, name=None, tree=None, quality=None, opencondition='READ', linecolor=None, fillcolor=None, fillstyle=None, hname=None):
        fch.__init__(self, linecolor=linecolor, fillcolor=fillcolor, fillstyle=fillstyle, hname=hname)
        self.file = TFile.Open(location, opencondition)
        self._theotherthing = self.file
        self.location = location
        self.t = []
        if name:
            self.set_name(name)
        if tree:
            self.add_tree(tree)
        if quality:
            self.set_quality(quality)

    def add_tree(self, trname):
        temptree = TTree()
        self.file.GetObject(trname, temptree)
        self.t.append(temptree)
        if(len(self.t) == 1):
            self._thething = self.t[0]

    def GetNtrees(self):
        return len(self.t)
    
    def add_all_trees(self):
        for ikey in self.GetListOfKeys():
            if isinstance(ikey.ReadObj(), TTree):
                self.add_tree(ikey.GetName())
