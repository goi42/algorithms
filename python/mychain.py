import sys
from ROOT import TChain
from myfch import *

class mychain(myfch):
    def __init__(self,trname,name=None,quality=None,lfiles=None):
        myfch.__init__(self)
        self.tname.append(trname)
        self.chain = TChain(trname,"")
        self.t.append(self.chain.GetTree())
        if name: self.set_name(name)
        if quality: self.set_quality(quality)
        if lfiles: self.add_files(lfiles)
        self.locations = [] #list of locations of added files
        self._thething = self.chain
    def __getattr__(self,name):
        return getattr(self.chain,name)
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
                raise ValueError("chain.add_files(...,recreate=True) requires 1 tree to avoid ambiguity.")
            self.chain = TChain(tname[0],"")
        for ifile in lfiles:
            self.add_file(ifile)
    def add_files_from(self,location,ignore_path='old',filemax=None,forcename=None):
        '''walks down the specified directory, skipping all paths with the specified ignore_path string in them, and adds all files contained therein. If filemax is specified, only adds files until the number of added files reaches filemax. If forcename is specified, requires added files have the specified name.
        '''
        import os
        for dirpath,dirnames,filenames in os.walk(location):
            if 'old' in dirpath:
                continue
            for fl in filenames:
                if filemax:
                    if len(self.locations) >= filemax:
                        return
                if forcename:
                    if fl != forcename:
                        raise NameError(os.path.join(dirpath,fl)+" is not named "+forcename)
                self.add_file(os.path.join(dirpath,fl))
