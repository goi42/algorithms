'''
Command-line argument parser for makeplots_main.py. Handled here for elegance.
makeplots_layer.py might also import arguments from here for convenience.
'''
import importlib
import argparse
import os
# parse arguments
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--verbose', action='store_true',
                    help='prints extra information while running')
parser.add_argument('--debug', action='store_true',
                    help='prints all information while running')
parser.add_argument('--pathtolayerfile', default='./',
                    help='directory where makeplots_layer.py is located')
parser.add_argument('--outputlocation', default='./',
                    help='where the output files will be stored')
parser.add_argument('--filename', default='plots_main.pdf',
                    help='plots file to be created; ".pdf" added if no extension specified')
parser.add_argument('--drawopt', default='',  # 'NORM HIST',
                    help='the option passed to Draw')
parser.add_argument('--C', action='store_true',
                    help='saves .C files')
parser.add_argument('--hist', action='store_true',
                    help='creates a file containing the generated histograms')
parser.add_argument('--hfilename', default=None,
                    help='file to store histograms if --hist option specified; uses filename with ".root" extension by default')
parser.add_argument('--can', action='store_true',
                    help='saves canvases in hfilename')
parser.add_argument('--legend', type=float, nargs=4,
                    metavar=('xlo', 'ylo', 'xhi', 'yhi'),
                    default=[0.6, 0.6, 0.9, 0.9],
                    help='list of parameters for legend placement')
parser.add_argument('--legendkey', default=None, choices=['topcenter', 'topleft'],
                    help='shortcuts to certain legend configurations')
# leg =  TLegend(0.3, 0.7, 0.6, 0.9)#create legend
# leg =  TLegend(0.75, 0.6, 1, 0.9)#create legend
# leg = TLegend(0.41, 0.7, 0.85, 0.9)#create legend
# leg = TLegend(0.65, 0.7, 1, 0.9)#create legend
parser.add_argument('--norm', action='store_true',
                    help='normalize histograms')
parser.add_argument('--fixbinning', action='store_true',
                    help='after the first histogram is drawn, all subsequent histograms on the same canvas will be drawn with the same number of bins and same hi and lo bins.')
parser.add_argument('--doDraw', action='store_true',
                    help='use Draw instead of looping over events')
parser.add_argument('--labelaxes', action='store_true',
                    help='turn on x- and y- axis labels (done automatically for 2D plots)')
parser.add_argument('--notitle', action='store_true',
                    help='turn off plot titles')
parser.add_argument('--nolegend', action='store_true',
                    help='turn off the legend')
parser.add_argument('--filllinecolors', action='store_true',
                    help='use linecolor as fillcolor')
parser.add_argument('--markerlinecolors', action='store_true',
                    help='use linecolor as markercolor')
parser.add_argument('--yesstack', action='store_true',
                    help='stack histograms')
parser.add_argument('--setoptstat', default='',
                    help='string to pass to gStyle.SetOptStat')
parser.add_argument('--nosumw2', action='store_true',
                    help='do not call Sumw2 on histograms')
parser.add_argument('--nomultithreading', action='store_true',
                    help='do not do ROOT.EnableImplicitMT()')
parser.add_argument('--lhcbStyle', action='store_true',
                    help='use lhcbStyle.C formatting')
parser.add_argument('--buildlegend', action='store_true',
                    help='use BuildLegend instead of the default creation (overrides all other settings)')

# class modimport(argparse.Action):
#     def __init__(self,option_strings,dest,nargs=None,**kwargs):
#         # if nargs is not None:
#         #     raise ValueError("nargs not allowed")
#         super(modimport,self).__init__(option_strings,dest,**kwargs)
#     def __call__(self,parser,namespace,values,option_string=None):
#         L = importlib.import_module(values,package='L')
#     L=None
# parser.add_argument('layer',nargs='1',action=modimport,
#                     help='executes "from fr import im"')


args = parser.parse_args()
verbose = args.verbose
debug = args.debug
if(debug):
    verbose = True
pathtolayerfile = args.pathtolayerfile
outputlocation = args.outputlocation
filename = args.filename
if '.' not in filename:
    filename += '.pdf'
drawopt = args.drawopt
saveC = args.C
histograms = args.hist
hfilename = os.path.splitext(args.filename)[0] + '.root' if args.hfilename is None else args.hfilename
if '.root' not in hfilename:
    hfilename += '.root'
savecan = args.can
legpars = args.legend
if args.legendkey == 'topcenter':
    legpars = [0.3, 0.7, 0.6, 0.9]
elif args.legendkey == 'topleft':
    legpars = [0.1, 0.7, 0.3, 0.9]
norm = args.norm
fixbinning = args.fixbinning
doDraw = args.doDraw
if fixbinning and not doDraw:
    raise parser.error('fixbinning does nothing without doDraw')
labelaxes = args.labelaxes
notitle = args.notitle
nolegend = args.nolegend
filllinecolors = args.filllinecolors
markerlinecolors = args.markerlinecolors
yesstack = args.yesstack
setoptstat = args.setoptstat
nosumw2 = args.nosumw2
nomultithreading = args.nomultithreading
lhcbStyle = args.lhcbStyle
buildlegend = args.buildlegend
