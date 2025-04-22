import numpy as np
import os
import sys

from common import autocorrelation2d
from xml_to_xyz import xml_to_particles, xyz_to_particles

analyzed_system = sys.argv[1]
min_len = int(sys.argv[2])
max_len = int(sys.argv[3])
lag = int(sys.argv[4])
freq = int(sys.argv[5])

analyzed_dir = 'raw_data/' + analyzed_system

analyzed_xml_filenames = [ '{}/{}'.format(analyzed_dir, filename) for filename in os.listdir(analyzed_dir) ]
if analyzed_xml_filenames[0][-3:] == 'xml':
	mode = 'xml'
elif analyzed_xml_filenames[0][-3:] == 'xyz':
	mode = 'xyz'
else:
	1/0

output_filename = 'data/autocorrelation_{}_{}_{}_lag_{}.dat'.format(analyzed_system, min_len, max_len, lag)

ts = np.array([])
acs = []
for i in range(len(analyzed_xml_filenames)):
	print(analyzed_xml_filenames[i])
	if mode == 'xml': particles = xml_to_particles([analyzed_xml_filenames[i]])
	elif mode == 'xyz': particles = xyz_to_particles([analyzed_xml_filenames[i]], freq)
	else: 1/0
	for p in particles:
		if p.length < min_len or p.length > max_len: continue
		# I should make the displacements read from the file
		# not compute them once mroe
		# but I was in a hurry ;)
		p.compute_displacements()
		p.compute_autocorrelation(n=lag)
		acs.append(p.ac)
		if len(p.t_ac)>len(ts): ts = p.t_ac

ac = np.zeros(len(ts))
print(ts)
1/0

weights_sum = np.zeros(len(ac),dtype=int)
weights = []

for a in acs:
	weights_a = a[1]
	weights.append(weights_a)
	print(len(weights_a))
	print(len(a[0]))
	print(len(weights_sum))
	print(len(weights_sum[:len(a[0])]))
	print()
	weights_sum[:len(a[0])] += weights_a

for j in range(len(acs)):
	ac[:len(weights[j])] = ac[:len(weights[j])] + acs[j][0]*weights[j]/weights_sum[:len(weights[j])]

np.savetxt(output_filename, np.transpose([ts,ac]), header='lag ac')