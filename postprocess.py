#!/usr/bin/env python
# .- coding: utf-8 -.

import os
import sys
import datetime
import numpy as np
from glob import glob

#import scipy.stats

def reject_outliers(data, m = 2.):
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d/mdev if mdev else 0
    return data[s<m]

def oneline(data):
    print "mean: %7.3fμs (stdev %6.3fμs) median: %7.3fμs" % \
        (data.mean() * 1000.*1000,
        data.std() * 1000.*1000,
        np.median(data)*1000*1000)

def run_dataset(inputfile):
    data = np.loadtxt(dataset, delimiter='\n')
    data = reject_outliers(data)
    oneline(data)

    return data

    #_t, _p = scipy.stats.wilcoxon(data1, data2)
    #print "p-value: %f" % _p


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: %s <dataset> [datasetN]" % sys.argv[0]
        print "   Partial dataset names (tabcomplete) will be expanded."
        sys.exit(255)

    inputfile = sys.argv[1]
    if inputfile.endswith("."):
        inputfile = inputfile[:-1]

    ran_at = os.stat(glob(inputfile + "*")[0]).st_mtime
    ran_at = datetime.datetime.fromtimestamp(ran_at)

    runname = inputfile.split(".", 2)[1].split("__")
    print "%s:%s (%s on %s)" % (runname[0], runname[1], ran_at, os.uname()[1])
    print "-----"*10
    print

    for dataset in glob(inputfile + ".?"):
        run_dataset(inputfile)

    print

