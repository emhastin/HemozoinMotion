# this part of code is pretty technical: it is reading xml files
# and converting them to python data structures that I prepared
# you can see that it is based on some keywords from your xml files
# like particle, detection, etc.

from bs4 import BeautifulSoup
from particle import Particle

def xml_to_particles(datafilenames):

	number_of_particles = 0
	particles = []
	track_number = 1

	for datafile in datafilenames:

		with open(datafile, 'r') as f:
			data = f.read()

		traj_soup = BeautifulSoup(data, "xml")

		traj_info = traj_soup.Tracks.attrs
		# print('Number of particles: {}\nDistance measured in {}\nTimestep = {} {}'.format(traj_info["nTracks"], traj_info["spaceUnits"], traj_info["frameInterval"], traj_info["timeUnits"]))

		tracks = traj_soup.find_all('particle')

		for track in tracks:
			detections = track.find_all('detection')
			temp_coords = []
			temp_times = []
			temp_temp_indices = []
			for detection in detections:
				temporal_index =  int(detection.attrs["t"])
				dt = float(traj_info["frameInterval"])
				time = temporal_index * dt
				x = float(detection.attrs["x"])
				y = float(detection.attrs["y"])
				z = float(detection.attrs["z"])
				temp_coords.append([x, y, z])
				temp_times.append(time)
				temp_temp_indices.append(temporal_index)
			p = Particle(uid = track_number, coords = temp_coords, temporal_indices = temp_temp_indices, dt = dt, times = temp_times, label = "HEM")
			particles.append(p)

			track_number += 1

	return particles

def xyz_to_particles(datafilenames, freq):

	particles = []

	for datafile in datafilenames:

		with open(datafile) as f:

			for j, line in enumerate(f):

				if j==0:
					n_particles = int(line)
					particle_rs = [ [] for _ in range(n_particles) ]
					ts = []
					continue
				elif j % (n_particles+2) == 0:
					continue
				elif j % (n_particles+2) == 1:
					timeframe_number = j // (n_particles+2)
					if timeframe_number % freq != 0: continue
					ts.append( float(line.split()[3])/10**12 )
				else:
					track_number = (j % (n_particles+2)) - 2
					if timeframe_number % freq != 0: continue
					_, x, y, z = line.split()
					x = float(x)/10000
					y = float(y)/10000
					z = float(z)/10000
					particle_rs[track_number].append([x,y,z])

		for j in range(n_particles):
			p = Particle(uid = len(particles), coords = particle_rs[j], temporal_indices = range(len(ts)), dt = ts[1]-ts[0], times = ts, label = "HEM")
			particles.append( p )

	return particles	