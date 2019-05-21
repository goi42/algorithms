import sys
from ROOT import TChain
from fch import fch
from file import file


class chain(fch):
    def __init__(self, trname, name=None, quality=None, lfiles=None, add_files_from=None, nentries=False, fracentries=False, linecolor=None, markercolor=None, fillcolor=None, fillstyle=None, hname=None):
        fch.__init__(self, linecolor=linecolor, markercolor=markercolor, fillcolor=fillcolor, fillstyle=fillstyle, hname=hname)
        self.chain = TChain(trname, "")
        self._thething = self.chain
        self._theotherthing = self.chain
        self.locations = []  # list of locations of added files
        if name is not None:
            self.set_name(name)
        if quality is not None:
            self.set_quality(quality)
        if lfiles is not None:
            self.add_files(lfiles, nentries=nentries, fracentries=fracentries)
        if add_files_from is not None:
            if not isinstance(add_files_from, dict):
                raise TypeError('add_files_from must be a keyword dictionary')
            self.add_files_from(**add_files_from)

    def add_tree(self, trname, recreate=False):
        raise Exception("chain.add_tree not yet implemented because it is not clear what it should do.")

    def add_file(self, floc, nentries=False, fracentries=False, check_tree=False, insist_tree=False, quiet=True):
        'adds file. check_tree will check whether the specified tree exists before adding it (may slow performance) and raises an error if insist_tree.'
        ' nentries will limit the number of entries added; fracentries will enable nentries and check_tree and take only the specified fraction (minimum 1).'
        if insist_tree and not check_tree:
            raise IOError('cannot use insist_tree without check_tree')
        if fracentries:
            if not 0 < fracentries < 1:
                raise ValueError('fracentries must be between 0 and 1!')
            check_tree = nentries = True
        addtree = True
        if check_tree:
            trname = self.chain.GetName()
            f = file(floc)  # myROOTtypes.file
            if not f.Get(trname):
                addtree = False
                if insist_tree:
                    raise IOError('{0} does not contain {1}'.format(floc, trname))
                if not quiet:
                    print floc, 'does not contain', trname
            if fracentries and addtree:
                nEntries = int(f.Get(trname).GetEntries() * fracentries)
                if nEntries == 0:
                    nEntries = 1
            f.Close()
            del f
        if nentries and not fracentries:
            nEntries = nentries
        if addtree:
            if nentries:
                self.chain.Add(floc, nEntries)
            else:
                self.chain.Add(floc)
            self.locations.append(floc)

    def add_files(self, lfiles, recreate=False, nentries=False, fracentries=False, check_tree=False, insist_tree=False, quiet=True):
        if recreate:
            self.chain = TChain(self._thething.GetName(), "")
        for ifile in lfiles:
            self.add_file(ifile, nentries=nentries, fracentries=fracentries, check_tree=check_tree, insist_tree=insist_tree, quiet=quiet)

    def add_files_from(self, location, ignore_path='old', filemax=None, forcename=None, inclname=None, nentries=False, fracentries=False, check_tree=False, insist_tree=False):
        '''walks down the specified directory, skipping all paths with the specified ignore_path string in them, and adds all files contained therein.
        If filemax is specified, only adds files until the number of added files reaches filemax.
        If forcename is specified, requires added files have the specified name.
        If inclname is specified, requires added files include the specified string in their name.
        '''
        import os
        from os.path import join as opj
        if not os.path.isdir(location):
            raise IOError('{0} is not a directory!'.format(location))
        for dirpath, dirnames, filenames in os.walk(location):
            if ignore_path is not None and ignore_path in dirpath:
                continue
            for fl in filenames:
                if filemax is not None and len(self.locations) >= filemax:
                    return
                if forcename is not None and fl != forcename:
                    continue
                    # raise NameError("{} is not named {}".format(opj(dirpath, fl), forcename))
                if inclname is not None and inclname not in fl:
                    continue
                    # raise NameError("{} does not include {}".format(opj(dirpath, fl), forcename))
                self.add_file(opj(dirpath, fl), nentries=nentries, fracentries=fracentries, check_tree=check_tree, insist_tree=insist_tree)
