import numpy as np
import os
import sys
import glob

analyzed_system = sys.argv[1]
bin_min = float(sys.argv[2])
bin_max = float(sys.argv[3])
bin_num = int(sys.argv[4])
radius = float(sys.argv[5])
reference_draws = int(sys.argv[6])

data_filenames = glob.glob('data/positions_{}_*'.format(analyzed_system))

distances = []

for i, data_filename in enumerate(data_filenames):

	positions = [ [] for j in range(1000000) ]

	with open(data_filename, 'r') as input_file:
		for line in input_file:
			if line[0] == '#': continue
			line_split = line.split(' ')
			time = int( line_split[0] )
			r = np.array( [float(line_split[1]), float(line_split[2]), float(line_split[3])] )
			positions[time].append(r)

	print(data_filename)
	print( 'first frame: {} particles; max: {} particles'.format(len(positions[0]), np.max([ len(positions[j]) for j in range(1000000) if len(positions[j]) > 0 ])) )

	for p in positions:
		if len(p) < 2: continue
		for j in range(len(p)-1):
			for k in range(j):
				distances.append( np.sqrt(np.sum((p[j]-p[k])**2)) )

# 1/0

h, b = np.histogram(distances, bins = np.linspace(bin_min, bin_max, bin_num), density = True)
bc = 0.5*(b[1:]+b[:-1])

# reference system
ref_pos_3d = []
for j in range(reference_draws):
	while True:
		x = radius*(2*np.random.rand()-1)
		y = radius*(2*np.random.rand()-1)
		z = radius*(2*np.random.rand()-1)
		if x**2+y**2+z**2<radius**2:
			ref_pos_3d.append(np.array([x,y]))
			break
		else:
			continue

ref_distances_3d = []
for j in range(len(ref_pos_3d)-1):
	for k in range(j):
		ref_distances_3d.append( np.sqrt(np.sum((ref_pos_3d[j]-ref_pos_3d[k])**2)) )

rh3d, _ = np.histogram(ref_distances_3d, bins = np.linspace(bin_min, bin_max, bin_num), density = True)

np.savetxt('data/rdf_{}.dat'.format(analyzed_system), np.transpose([bc, h, rh3d]), header='r hist hist_ref')

	# N = 1000
	# R = 3.0

	# ref_pos = []
	# for j in range(N):
	# 	while True:
	# 		x = R*(2*np.random.rand()-1)
	# 		y = R*(2*np.random.rand()-1)
	# 		if x**2+y**2<R**2:
	# 			ref_pos.append(np.array([x,y]))
	# 			break
	# 		else:
	# 			continue

	# ref_distances = []
	# for j in range(len(ref_pos)-1):
	# 	for k in range(j):
	# 		ref_distances.append( np.sqrt(np.sum((ref_pos[j]-ref_pos[k])**2)) )

	# rh, _ = np.histogram(ref_distances, bins = np.linspace(0.0, 6.0, 51), density = True)

	# ref_pos_3d = []
	# for j in range(N):
	# 	while True:
	# 		x = R*(2*np.random.rand()-1)
	# 		y = R*(2*np.random.rand()-1)
	# 		z = R*(2*np.random.rand()-1)
	# 		if x**2+y**2+z**2<R**2:
	# 			ref_pos_3d.append(np.array([x,y]))
	# 			break
	# 		else:
	# 			continue

	# ref_distances_3d = []
	# for j in range(len(ref_pos_3d)-1):
	# 	for k in range(j):
	# 		ref_distances_3d.append( np.sqrt(np.sum((ref_pos_3d[j]-ref_pos_3d[k])**2)) )

	# rh3d, _ = np.histogram(ref_distances_3d, bins = np.linspace(0.0, 6.0, 51), density = True)

	# np.savetxt('data/data_rdf_{}.dat'.format(i+1), np.transpose([bc, h, h/rh, h/rh3d]))