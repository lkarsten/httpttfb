#!/usr/bin/env python
# .- coding: utf-8 -.

import os
import sys
import datetime
import numpy as np
from glob import glob

from pprint import pprint

def reject_outliers(data, m = 2.):
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d/mdev if mdev else 0
    return data[s<m]

def print_report(data):
    print "mean: %7.3fμs (stdev %6.3fμs) median: %7.3fμs" % \
        (data.mean() * 1000.*1000,
        data.std() * 1000.*1000,
        np.median(data)*1000*1000)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print "Usage: %s < dataset" % sys.argv[0]
        sys.exit(255)

    # "USE_FASTOPEN=0 ./httpttfb localhost 6081 10" ran on immer at Tue Apr 29 13:26:09 2014
    header = sys.stdin.readline()

    _, cmd, remainder = header.split("\"", 2)

    cmd = cmd.split()
    remainder = remainder.split()

    ran_on = remainder[2]
    ran_at = datetime.datetime.strptime(" ".join(remainder[-5:]), "%a %b %d %H:%M:%S %Y")

    s = "%s:%s (%s on %s)" % (cmd[2], cmd[3], ran_at, ran_on)
    print s
    print "-"*len(s)

    data = np.loadtxt(sys.stdin, delimiter='\n')
    data = reject_outliers(data)

    print_report(data)
#    print

