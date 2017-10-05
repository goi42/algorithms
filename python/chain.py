import sys
from ROOT import TChain
from fch import *

class chain(fch):
    def __init__(self,trname,name=None,quality=None,lfiles=None):
        fch.__init__(self)
        self.tname.append(trname)
        self.chain = TChain(trname,"")
        self.t.append(self.chain.GetTree())
        if name: self.set_name(name)
        if quality: self.set_quality(quality)
        if lfiles: self.add_files(lfiles)
        self.locations = [] #list of locations of added files
        self._thething = self.chain
    def add_tree(self,trname,recreate=False):
        print "chain.add_tree not yet implemented because it is not clear what it should do."
        sys.exit()
    def add_file(self,floc):
        self.chain.Add(floc)
        self.locations.append(floc)
        if not self.check_tsize_1():
            raise ValueError("chain::add_file only works if there is only 1 associated tree.")
        self.t[0] = self.chain.GetTree()
    def add_files(self,lfiles,recreate=False):
        if recreate:
            if not self.check_tsize_1():
                print "chain.add_files(...,recreate=True) requires 1 tree to avoid ambiguity."
                sys.exit()
            self.chain = TChain(tname[0],"")
        for ifile in lfiles:
            self.add_file(ifile)


