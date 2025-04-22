import numpy as np
import sys

analyzed_system = sys.argv[1]
too_large_displacement = float(sys.argv[2])

data_filename = 'data/displacements_{}.dat'.format(analyzed_system)
filtered_data_filename = 'data/displacements_{}_{:.1f}.dat'.format(analyzed_system, too_large_displacement)

with open(data_filename, 'r') as input_file:
	with open(filtered_data_filename, 'w') as output_file:
		for line in input_file:
			if line[0] == '#':
				output_file.write(line)
			else:
				line_split = line.split(' ')
				lag = int( line_split[1] )
				dr = np.array( [float(line_split[2]), float(line_split[3]), float(line_split[4])] )
				dt = float(line_split[5])
				sd = np.sum(dr**2)
				sd_norm = sd/lag/dt
				if sd_norm < too_large_displacement:
					output_file.write(line)