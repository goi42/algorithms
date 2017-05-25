'''
Command-line argument parser for makeplots_main.py. Handled here for elegance.
'''
import argparse,importlib
#parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--hist',action='store_true',
                    help='creates a file containing the generated histograms')
parser.add_argument('--verbose',action='store_true',
                    help='prints extra information while running')
parser.add_argument('--debug',action='store_true',
                    help='prints all information while running')
parser.add_argument('--C',action='store_true',
                    help='saves .C files')
parser.add_argument('--drawopt',default='NORM HIST',
                    help='the option passed to Draw')
parser.add_argument('--outputlocation',default='./',
                    help='where the output files will be stored')
parser.add_argument('--filename',default='plots_main.pdf',
                    help='plots file to be created')
parser.add_argument('--hfilename',default='histograms.root',
                    help='file to store histograms if --hist option specified')
parser.add_argument('--pathtolayerfile',default='./',
                    help='directory where makeplots_layer.py is located')

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
histograms = args.hist
verbose = args.verbose
debug = args.debug
saveC = args.C
drawopt = args.drawopt
outputlocation = args.outputlocation
filename = args.filename
pathtolayerfile = args.pathtolayerfile