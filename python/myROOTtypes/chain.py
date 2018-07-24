import sys
from ROOT import TChain
from fch import fch
from file import file


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
            if not isinstance(add_files_from, dict):
                raise TypeError('add_files_from must be a keyword dictionary')
            self.add_files_from(**add_files_from)

    def __getattr__(self, name):
        return getattr(self.chain, name)

    def add_tree(self, trname, recreate=False):
        raise Exception("chain.add_tree not yet implemented because it is not clear what it should do.")

    def add_file(self, floc, check_tree=False, insist_tree=False):
        'adds file. check_tree will check whether the specified tree exists before adding it (may slow performance) and raises an error if insist_tree.'
        if insist_tree and not check_tree:
            raise IOError('cannot use insist_tree without check_tree')
        addtree = True
        if check_tree:
            trname = self.chain.GetName()
            f = file(floc)  # myROOTtypes.file
            if not f.Get(trname):
                addtree = False
                if insist_tree:
                    raise IOError('{0} does not contain {1}'.format(floc, trname))
            f.Close()
            del f
        if addtree:
            self.chain.Add(floc)
            self.locations.append(floc)

    def add_files(self, lfiles, recreate=False, check_tree=False, insist_tree=False):
        if recreate:
            self.chain = TChain(self._thething.GetName(), "")
        for ifile in lfiles:
            self.add_file(ifile, check_tree=check_tree, insist_tree=insist_tree)

    def add_files_from(self, location, ignore_path='old', filemax=None, forcename=None, inclname=None, check_tree=False, insist_tree=False):
        '''walks down the specified directory, skipping all paths with the specified ignore_path string in them, and adds all files contained therein.
        If filemax is specified, only adds files until the number of added files reaches filemax.
        If forcename is specified, requires added files have the specified name.
        If inclname is specified, requires added files include the specified string in their name.
        '''
        import os
        from os.path import join as opj
        for dirpath, dirnames, filenames in os.walk(location):
            if ignore_path is not None and ignore_path in dirpath:
                continue
            for fl in filenames:
                if filemax is not None:
                    if len(self.locations) >= filemax:
                        return
                if forcename is not None:
                    if fl != forcename:
                        continue
                        # raise NameError("{} is not named {}".format(opj(dirpath, fl), forcename))
                if inclname is not None:
                    if inclname not in fl:
                        continue
                        # raise NameError("{} does not include {}".format(opj(dirpath, fl), forcename))
                self.add_file(opj(dirpath, fl), check_tree=check_tree, insist_tree=insist_tree)
