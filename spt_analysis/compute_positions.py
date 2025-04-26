import os
import sys

from xml_to_xyz import xml_to_particles

analyzed_system = sys.argv[1]

analyzed_dir = 'raw_data/' + analyzed_system
analyzed_xml_filenames = [ '{}/{}'.format(analyzed_dir, filename) for filename in os.listdir(analyzed_dir) ]

for i in range(len(analyzed_xml_filenames)):
	particles = xml_to_particles([analyzed_xml_filenames[i]])
	output_filename = 'data/positions_{}_{}.dat'.format(analyzed_system, i+1)
	with open(output_filename, "w") as output_file:
		output_file.write('# t x y z\n') # header explaining the columns in file
		for p in particles:
			for j in range(len(p.rs)):
				output_file.write('{} {} {} {}\n'.format(p.temporal_indices[j], *p.rs[j]))