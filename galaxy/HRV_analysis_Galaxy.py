from DataSeries import DataSeries
from Indexes import *
from Files import *
import optparse

## TODO: load a .RR file (as functions do in Files)
## TODO: add windowing
## TODO: if inputfile is a .tar.gz: untar and load more files



usage = "Usage: load RR file"
parser = optparse.OptionParser(usage=usage)

parser.add_option("-i", "--inputfile",
                  action="store", type="string",
                  dest="input_file", help="Input File")

parser.add_option("-o", "--outputdir",
                  action="store", type="string",
                  dest="output_dir", help="Output Dir")

# parser.add_option("-l", "--list",
#                   action="store", type="string", default='',
#                   dest="hrvlist", help="List of HRV indexes to be computed")

parser.add_option("-w", "--windowfile",
                  action="store", type="string", default='',
                  dest="window_file", help="Window File")
# parser.add_option("-n", "--name",
#                   action="store", type="string", default='RR',
#                   dest="colname", help="Name of RR column")

(options, args) = parser.parse_args()
INPUTFILE = options.input_file
OUTDIR = options.output_dir
WINFILE = options.window_file


HRVlist = [True,True,True,True]
# inputfile is a csv, but it will be a .RR file, created with RRData.save(...)
RRdata = load_rr_data_series(INPUTFILE)

INDEXES = list()
if HRVlist[0]:
    INDEXES.append(RRMean(RRdata).value)
if HRVlist[1]:
    INDEXES.append(RRSTD(RRdata).value)
if HRVlist[2]:
    INDEXES.append(pNNx(50, RRdata).value)
if HRVlist[3]:
    INDEXES.append(pNNx(25, RRdata).value)

print(INDEXES)

# TODO: if I understood a class with execute;

# TODO: I think it is better to inheritate from a common class with e.g. a def execute(**pars) ovverridable


class GalaxyHRVAnalysis(object):
    def execute(self, **kwargs):
        INPUTFILE = kwargs['input']
        OUTDIR = kwargs['output']

        indexes = [True, True, True, True]
        RRdata = load_rr_data_series(INPUTFILE)

        results = list()
        if indexes[0]:
            results.append(("RRMean", RRMean(RRdata).value))
        if indexes[1]:
            results.append(("RRSTD", RRSTD(RRdata).value))
        if indexes[2]:
            results.append(("pNN50", pNNx(50, RRdata).value))
        if indexes[3]:
            results.append(("pNN25", pNNx(25, RRdata).value))

        pd.DataFrame(results).to_csv(OUTDIR, header=True)