import sys

inp = sys.argv[1]
out = sys.argv[2]
dt = float(sys.argv[3])

with open(inp, 'r') as input_file:
	with open(out, 'w') as output_file:
		for line in input_file:
			if len(line.split()) == 1:
				output_file.write('{}'.format(line))
			elif "Timestep:" in line.split():
				time = float(line.split()[-1])
				output_file.write('{} time [ps] {}\n'.format(out, time*dt))
			elif len(line.split()) == 4:
				label, x, y, z = line.split()
				output_file.write('{} {} {} 0.0\n'.format(label, x, y))
			else:
				1/0
