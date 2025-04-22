import os
import sys

from xml_to_xyz import xml_to_particles, xyz_to_particles

# arguments from terminal: what system (directory with xmls),
# what minimum track length,
# what maximum track length
analyzed_system = sys.argv[1]
min_len = int(sys.argv[2])
max_len = int(sys.argv[3])
freq = int(sys.argv[4])

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
output_filename = 'data/displacements_{}_{}_{}.dat'.format(analyzed_system, min_len, max_len)
with open(output_filename, "w") as output_file:
	output_file.write('# start lag dx dy dz time_res\n') # header explaining the columns in file
	for i in range(len(analyzed_xml_filenames)):
		print(analyzed_xml_filenames[i])
		# here the tracks from xml file are transformed into 'particle' objects
		if mode == 'xml': particles = xml_to_particles([analyzed_xml_filenames[i]])
		elif mode == 'xyz': particles = xyz_to_particles([analyzed_xml_filenames[i]], freq)
		else: 1/0
		for p in particles:
			if p.length < min_len or p.length > max_len: continue
			# i compute and store displacements only if the track/particle
			# length is between min_len and max_len
			p.compute_displacements()
			for dr in p.drs:
				output_file.write('{} {} {} {} {} {}\n'.format(*dr))
