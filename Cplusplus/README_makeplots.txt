makeplots.C is a flexible program for making sets of plots from nTuples.
Suppose you want to compare nTracks to nLongTracks across several years, decays, filetypes, and cuts. It will collect the nTuples corresponding to each year, decay, and filetype, allow you to vary the names of the branches by tuple, allow you to vary the names of the cuts by branch and tuple, and allow you to pick what values should be compared in the same plot (i.e., different cuts and years on top of each other). It will then print a .pdf file with each plot, with a summary page at the end containing all the plots.

It must be in a directory with a copy of storeAll.C (original in ~/algorithms/).

I recommend compiling it with '.L makeplots.C++'. It can then be run with 'makeplots("<runmode>","<drawopt>")'.

There are 2 options:
The 1st: "o" to specify the output (./plots.pdf by default), "b" to specify the branches, "f" to specify the files, "c" to specify the cuts, "C" to save canvas.C files; these may be used in combination. Blank or "d" uses default parameters (see code).
The 2nd: "norm" is the default option and plots normalized histograms. It's just the draw option for MyTree->Draw(branch,cuts,option).

The counters that get printed out correspond to looped variables, meaning if there are 8 canvases, the canvas number will go from 0 to 7.

KNOWN ISSUES:
Custom parameter entry hasn't been tested. (Though it has been for plotbranches.C, from which this is derived.)
It will break if you don't provide the right kind of input (int, string, etc.).
If the names of the cuts or branches vary by tuple and cuts or branches are compared in a single canvas, the legend at the end will not reflect this (it only shows the legend for the upper left canvas, which is usually fine).
There is no fast way to enter cuts or branches if they vary by, say, decay and not every single tuple, like there is in plotbranches.C for variation by decay. Since makeplots.C allows for any number of layers with a user specified name, this is harder to implement, and I haven't wanted to take the time to work out the logic of this. For now, it seems the best bet is to work this into the default options if you don't want to type them in for every tuple.
In principle, I could accomodate variations in drawopt the same way I have branches and cuts, but I haven't wanted to take the time. Shouldn't be too difficult as the logic has already been worked out, although I'd probably want to make it a 4D vector, able to vary by file, branch, and cut.
