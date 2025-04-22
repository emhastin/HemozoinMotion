import numpy as np
import sys

# argument from terminal: what system will be analyzed
analyzed_system = sys.argv[1]

# this is the file in which displacements for this system are stored (these were computed earlier by compute_displacements.py)
data_filename = 'data/displacements_{}.dat'.format(analyzed_system)

# here I fo through displacements file, compute average timestep,
# max and min lag time
lag_min = np.inf
lag_max = 0
timestep = 0.0
count = 0
with open(data_filename, 'r') as input_file:
	for line in input_file:
		if line[0] == '#': continue
		line_split = line.split(' ')
		count += 1
		lag = int(line_split[1])
		timestep += float(line_split[-1])
		if lag < lag_min: lag_min = lag
		if lag > lag_max: lag_max = lag
timestep/=count
times = np.arange(lag_min, lag_max+1)*timestep

# here I go through the displacements file, read each line, and add the squared displacement
# to correct fields in arrays storing msd/tamsd. I also count how many values are
# added to the divide the values and have a mean, not a sum
# this ensures correct averaging, without overvaluing short tracks
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
		sd = np.sum(dr**2)
		tamsd[lag-lag_min] += sd
		sd_list[lag-lag_min].append(sd)
		counts_tamsd[lag-lag_min] += 1
		if start == 0:
			msd[lag-lag_min] += sd
			counts_msd[lag-lag_min] += 1
tamsd /= counts_tamsd
msd /= counts_msd

# here I store the data in separate files
# I always store separately, and the plot separately with other script
np.savetxt('data/tamsd_{}.dat'.format(analyzed_system), np.transpose([times, tamsd]), header='t TAMSD')
np.savetxt('data/msd_{}.dat'.format(analyzed_system), np.transpose([times, msd]), header = 't MSD')