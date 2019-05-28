#!/usr/bin/env python3
import os
import sys
import glob
import pandas as pd
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 12})


plt.style.use('bmh')

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
    allfiles2 = glob.glob(os.path.join(srcdir, pattern))
    df_list = {}
    for file in allfiles:
        #print "Processing ", file
        # tmp = pd.read_table(file, engine='python', header='infer', skipfooter=10)
        tmp = pd.read_csv(file, sep='\t', engine='python', header='infer', skipfooter=10)
        tmp['sec'] = tmp['ABS'] // 1000000
        tmp['LATENCY'] = tmp['LATENCY'] / 1000
        if op == "tp":
            df_list[file] = tmp.groupby('sec').count()
        elif op == "lat":
            df_list[file] = tmp['LATENCY']

if op == "tp":
    # allfiles = glob.glob(os.path.join("variable_50/bin/old_stats", pattern))
    # df_list2 = {}
    # for file in allfiles:
    #     tmp = pd.read_csv(file, sep='\t', engine='python', header='infer', skipfooter=10)
    #     tmp['sec'] = (tmp['ABS'] // 1000000) + 215
    #     df_list2[file] = tmp.groupby('sec').count()
    panel = pd.Panel(df_list)
    # panel2 = pd.Panel(df_list2)
    grouped = panel.sum(axis=0)
    # grouped2 = panel2.sum(axis=0)
    # grouped = grouped[5:len(grouped)]
    # grouped2 = grouped2[:len(grouped2)-5]
    if len(sys.argv) > 4:
        print(grouped['#ORDER'])
        plt.xlabel('Time(s)')
        plt.ylabel('Throughput(msgs/s)')
        plt.plot(grouped)
        # plt.plot(grouped2)
        # plt.legend()
        plt.tight_layout()
        plt.show()

    discarded = grouped[5:len(grouped)-5]  # sub the first and last 15 seconds
    a = discarded['#ORDER']
    (min, max) = st.t.interval(0.95, len(a) - 1, loc=np.mean(a), scale=st.sem(a))
    print ('#', srcdir, np.mean(a), min, max)

elif op == "skew":
    # lines1 = [int(line.rstrip('\n'))/1000 for line in open("./local_50")]
    # lines2 = [int(line.rstrip('\n'))/1000 for line in open("skew/LRU_8_500000.txt")]
    # lines3 = [int(line.rstrip('\n'))/1000 for line in open("skew/LRU_8_1000000.txt")]
    # lines1 = [int(line.rstrip('\n')) for line in open("skew/skew-alpha0.txt")]
    # lines2 = [int(line.rstrip('\n')) for line in open("skew/skew-alpha05.txt")]
    # lines3 = [int(line.rstrip('\n')) for line in open("skew/skew-alpha0.txt")]
    # lines4 = [int(line.rstrip('\n')) for line in open("skew/skew-alpha1smooth.txt")]
    # lines1 = [int(line.rstrip('\n')) for line in open
    #     ("skew/skew-alpha0.txt")]
    # for i in range(0):
    #     lines1.insert(0, lines1.pop(-1))
    # lines2 = [int(line.rstrip('\n')) for line in open
    #     ("skew/skew-alpha0.txt")]
    # for i in range(1):
    #     lines2.insert(0, lines2.pop(-1))
    # lines3 = [int(line.rstrip('\n')) for line in open
    #     ("skew/skew-alpha0.txt")]
    # for i in range(98):
    #     lines3.insert(0, lines3.pop(-1))
    plt.xlabel('Key')
    plt.ylabel('Frequency')
    plt.plot(lines1, label='Group 1')
    plt.plot(lines2, label='Group 2')
    plt.plot(lines3, label='Group 3')
    # plt.plot(lines4)
    # plt.plot(lines)
    axes = plt.gca()
    # axes.set_xlim([xmin,xmax])
    axes.set_ylim([0,5000])
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
        # plt.legend()
        plt.xlabel('Latency(ms)')
        plt.ylabel('Percentage')
        plt.tight_layout()
        plt.show()
