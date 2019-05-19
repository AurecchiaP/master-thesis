#!/usr/bin/env python3
import os
import sys
import glob
import pandas as pd
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt

if len(sys.argv) < 4:
    print ("Usage:", sys.argv[0], "<data dir> <pattern> <lat|tp>")
    sys.exit(1)

srcdir = str(sys.argv[1])
pattern = str(sys.argv[2])
op = str(sys.argv[3])

if op != "lat" and op != "tp" and op != "skew":
    print ("Invalid request:", op)
    sys.exit(1)
if op == "lat" or op == "tp":
    allfiles = glob.glob(os.path.join(srcdir, pattern))
    df_list = {}
    for file in allfiles:
        #print "Processing ", file
        # tmp = pd.read_table(file, engine='python', header='infer', skipfooter=10)
        tmp = pd.read_csv(file, sep='\t', engine='python', header='infer', skipfooter=10)
        tmp['sec'] = tmp['ABS'] // 1000000
        if op == "tp":
            df_list[file] = tmp.groupby('sec').count()
        elif op == "lat":
            df_list[file] = tmp['LATENCY']

if op == "tp":
    panel = pd.Panel(df_list)
    grouped = panel.sum(axis=0)
    if len(sys.argv) > 4:
        print(grouped['#ORDER'])
        plt.plot(grouped)
        plt.legend()
        plt.tight_layout()
        plt.show()

    discarded = grouped[5:len(grouped) - 5]  # sub the first and last 15 seconds
    a = discarded['#ORDER']
    (min, max) = st.t.interval(0.95, len(a) - 1, loc=np.mean(a), scale=st.sem(a))
    print ('#', srcdir, np.mean(a), min, max)

elif op == "skew":
    # lines = [int(line.rstrip('\n')) for line in open(srcdir)]
    lines1 = [int(line.rstrip('\n')) for line in open("skew/skew-alpha0.txt")]
    # for i in range():
    #     lines1.insert(0, lines1.pop(-1))
    # lines2 = [int(line.rstrip('\n')) for line in open("skew/skew-alpha1smooth.txt")]
    # for i in range(25):
    #     lines2.insert(0, lines2.pop(-1))
    # lines3 = [int(line.rstrip('\n')) for line in open
    #     ("skew/skew-alpha1smooth.txt")]
    # for i in range(75):
    #     lines3.insert(0, lines3.pop(-1))
    plt.xlabel('Key')
    plt.ylabel('Frequency')
    plt.plot(lines1)
    # plt.plot(lines2, label='Group 2')
    # plt.plot(lines3, label='Group 3')
    # plt.plot(lines)
    axes = plt.gca()
    # axes.set_xlim([xmin,xmax])
    axes.set_ylim([0,10000])
    plt.legend()
    plt.tight_layout()
    plt.show()
elif op == "lat":
    df = pd.concat(df_list)
    #df = df[df.VALUES != 0]  # remove lines with no latencies
    lat = df[int(len(df)*0.3):int(len(df)*0.9)]

    # Choose how many bins you want here
    data_set = sorted(set(lat))
    num_bins = np.append(data_set, data_set[-1] + 1)

    # Use the histogram function to bin the data
    counts, bin_edges = np.histogram(lat, bins=num_bins)  # , normed=True)
    counts = counts.astype(float) / len(lat)
    # Now find the cdf
    cdf = np.cumsum(counts)
    cdf_plot = {'value': bin_edges[0:-1], 'percentage': cdf}
    df = pd.DataFrame(cdf_plot)
    pd.set_option('display.max_rows', len(df))
    print ('#', df)
    pd.reset_option('display.max_rows')
    print ('#')
    print ('#')
    print ('#')
    print ('#')
    print ('#srcdir, mean, 5p, 25p, 50p, 75p, 95p, 99p')
    print ('#',  srcdir, lat.mean(), np.percentile(lat, 5), np.percentile(lat, 25), np.percentile(lat, 50), np.percentile(lat, 75), np.percentile(lat, 95), np.percentile(lat, 99))

    # And finally plot the cdf
    if len(sys.argv) > 4:
        plt.plot(bin_edges[0:-1], cdf)
        plt.ylim((0, 1))
        plt.legend()
        plt.tight_layout()
        plt.show()
