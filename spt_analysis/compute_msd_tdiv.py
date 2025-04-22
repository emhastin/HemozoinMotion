# analogous to compute_msd.py but sds are divided by dt
# for normal diffusion it is the best way to account for different dt
# for anomalous diffusion it is not so rigorous

import numpy as np
import sys

analyzed_system = sys.argv[1]

data_filename = 'data/displacements_{}.dat'.format(analyzed_system)

lag_min = np.inf
lag_max = 0
timestep = 0.0
count = 0

with open(data_filename, 'r') as input_file:
	for line in input_file:
		if line[0] == '#': continue
		line_split = line.split(' ')
		lag = int(line_split[1])
		if lag < lag_min: lag_min = lag
		if lag > lag_max: lag_max = lag

times = np.arange(lag_min, lag_max+1)

sd_list = [[] for i in range(len(times))]
tamsd = np.zeros(len(times))
dtamsd = np.zeros(len(times))
counts_tamsd = np.zeros(len(times), dtype=int)
msd = np.zeros(len(times))
counts_msd = np.zeros(len(times), dtype=int)

with open(data_filename, 'r') as input_file:
	for line in input_file:
		if line[0] == '#': continue
		line_split = line.split(' ')
		start = int( line_split[0] )
		lag = int( line_split[1] )
		dr = np.array( [float(line_split[2]), float(line_split[3]), float(line_split[4])] )
		dt = float( line_split[5] )
		sd = np.sum(dr**2)/dt
		tamsd[lag-lag_min] += sd
		sd_list[lag-lag_min].append(sd)
		counts_tamsd[lag-lag_min] += 1
		if start == 0:
			msd[lag-lag_min] += sd
			counts_msd[lag-lag_min] += 1

tamsd /= counts_tamsd
msd /= counts_msd

np.savetxt('data/tamsd_tdiv_{}.dat'.format(analyzed_system), np.transpose([times, tamsd]), header='t TAMSD')
np.savetxt('data/msd_tdiv_{}.dat'.format(analyzed_system), np.transpose([times, msd]), header = 't MSD')