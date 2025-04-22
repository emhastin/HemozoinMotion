import os
import sys

import numpy as np

from xml_to_xyz import xml_to_particles, xyz_to_particles

# arguments from terminal: what system (directory with xmls)
analyzed_system = sys.argv[1]
n_bins = int(sys.argv[2])

# here I iterate over all xml files, compute displacements and
# store them in displacements file
analyzed_dir = 'raw_data/' + analyzed_system
analyzed_xml_filenames = [ '{}/{}'.format(analyzed_dir, filename) for filename in os.listdir(analyzed_dir) ]
if analyzed_xml_filenames[0][-3:] == 'xml':
	mode = 'xml'
elif analyzed_xml_filenames[0][-3:] == 'xyz':
	mode = 'xyz'
else:
	1/0
output_filename = 'data/track_lengths_{}.dat'.format(analyzed_system)
track_lengths = []
dts = []
with open(output_filename, "w") as output_file:
	for i in range(len(analyzed_xml_filenames)):
		print(analyzed_xml_filenames[i])
		# here the tracks from xml file are transformed into 'particle' objects
		if mode == 'xml': particles = xml_to_particles([analyzed_xml_filenames[i]])
		elif mode == 'xyz': particles = xyz_to_particles([analyzed_xml_filenames[i]], freq)
		else: 1/0
		for j, p in enumerate(particles):
			track_length = p.length
			dts.append(p.dt)
			track_lengths.append(track_length)
		print('Number of tracks: {}'.format(j+1))



track_length_counts, track_length_bins = np.histogram(track_lengths, n_bins, density = False)
track_length_bin_centers = 0.5 * (track_length_bins[1:] + track_length_bins[:-1])

np.savetxt('data/track_lengths_{}.dat'.format(analyzed_system), np.transpose([track_length_bin_centers, np.mean(dts)*track_length_bin_centers, track_length_counts]), header = 'track_length track_duration/s N(track_length)')
