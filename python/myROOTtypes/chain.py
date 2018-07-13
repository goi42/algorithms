import sys
from ROOT import TChain
from fch import fch


class chain(fch):
    def __init__(self, trname, name=None, quality=None, lfiles=None, add_files_from=None):
        fch.__init__(self)
        self.chain = TChain(trname, "")
        self._thething = self.chain
        self.locations = []  # list of locations of added files
        if name is not None:
            self.set_name(name)
        if quality is not None:
            self.set_quality(quality)
        if lfiles is not None:
            self.add_files(lfiles)
        if add_files_from is not None:
            self.add_files_from(*add_files_from)

    def __getattr__(self, name):
        return getattr(self.chain, name)

    def add_tree(self, trname, recreate=False):
        raise Exception("chain.add_tree not yet implemented because it is not clear what it should do.")

    def add_file(self, floc):
        self.chain.Add(floc)
        self.locations.append(floc)

    def add_files(self, lfiles, recreate=False):
        if recreate:
            self.chain = TChain(self._thething.GetName(), "")
        for ifile in lfiles:
            self.add_file(ifile)

    def add_files_from(self, location, ignore_path='old', filemax=None, forcename=None):
        '''walks down the specified directory, skipping all paths with the specified ignore_path string in them, and adds all files contained therein. If filemax is specified, only adds files until the number of added files reaches filemax. If forcename is specified, requires added files have the specified name.
        '''
        import os
        for dirpath, dirnames, filenames in os.walk(location):
            if ignore_path in dirpath:
                continue
            for fl in filenames:
                if filemax is not None:
                    if len(self.locations) >= filemax:
                        return
                if forcename is not None:
                    if fl != forcename:
                        raise NameError(os.path.join(dirpath, fl) + " is not named " + forcename)
                self.add_file(os.path.join(dirpath, fl))
