#!/usr/bin/env python
# .- coding: utf-8 -.

import sys
import pandas as pd
import numpy as np

from glob import glob
#import scipy.stats

def reject_outliers(data, m = 2.):
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d/mdev if mdev else 0
    return data[s<m]

def oneline(data):
    print "mean: %.3fμs (stdev %.9f) median: %.3fμs" % \
        (data.mean() * 1000.*1000,
        data.std(),
        np.median(data)*1000*1000)

def run_dataset(input):
    for dataset in glob(input + ".?"):
        data = np.loadtxt(dataset, delimiter='\n')
        data = reject_outliers(data)
        oneline(data)

    #_t, _p = scipy.stats.wilcoxon(data1, data2)
    #print "p-value: %f" % _p


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "%s <dataset1> [datasetN]" % sys.argv[0]
        sys.exit(255)
    for inputfile in sys.argv[1:]:
        if inputfile.endswith("."):
            inputfile = inputfile[:-1]
        print inputfile
        print "==="*8
        run_dataset(inputfile)
        print


