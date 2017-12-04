# Converts binary single precision floats to human-readable ASCII
# 2017/11/17 @mknight
#

import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--ifile", help="Input file (binary single-precision floats)")
parser.add_argument('-o', '--ofile', help="Output file (ASCII-formatted floats)")

args = parser.parse_args()

if args.ifile is None or args.ofile is None:
    print "Usage: must specify input and output file paths"
    exit()

data = np.fromfile(args.ifile, dtype="float32")
np.savetxt(args.ofile, data, fmt="%f", delimiter=" ")

