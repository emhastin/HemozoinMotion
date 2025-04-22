# here is the part of code that I prepared to store the particles/tracks
# and do fundamental math on them

import numpy as np

from common import autocorrelation2d, autocorrelation2d_raw

#-------------------------------------------------------------------------------

class Particle():

	# constructor function, so a way to create a particle object
	# by providing series of coordinates, times, etc.
	# temporal indices means times in a form of integers
	# so times/dt
	def __init__(self, uid, coords, temporal_indices, dt, times, label = "XXX"):

		self.id = uid

		self.dt = dt

		self.rs = np.array(coords)
		self.ts = np.array(times)
		self.temporal_indices = np.array(temporal_indices, dtype = int)

		self.r_start = self.rs[0]
		self.r_end = self.rs[-1]

		self.t_start = self.ts[0]
		self.t_end = self.ts[-1]

		self.length = len(self.ts)

		self.label = label

	#-------------------------------------------------------------------------------

	# here displacements for single partice/track are computed
	# it is a double loop through the series of positions
	# I always store the displacement start temporal index
	# the temporal index difference (lag),
	# dx, dy, dz (three components of dr)
	# and as an extra info, the dt in this particle/track
	def compute_displacements(self):

		self.drs = []

		for j in range(len(self.rs)-1):
			for k in range(1, len(self.rs)-j):
				dr = self.rs[j+k]-self.rs[j]
				data = (self.temporal_indices[j], self.temporal_indices[j+k]-self.temporal_indices[j], *dr, self.dt)
				self.drs.append( data )

	#-------------------------------------------------------------------------------

	# here autocorrelation for single particle/track is computed
	def compute_autocorrelation(self,n=1):

		# self.dr1 = np.zeros((self.temporal_indices[-1]-self.temporal_indices[0], 3))
		self.drn = np.zeros((self.temporal_indices[-1]-n+1-self.temporal_indices[0], 3))

		# here I create a list of all displacements with lag
		# (difference in temporal indices) of n
		for dr in self.drs:
			start = dr[0]-self.temporal_indices[0]
			lag = dr[1]
			displacement = dr[2:5]
			# if lag == 1:
			if lag == n:
				# self.dr1[start] = np.array(displacement)
				self.drn[start] = np.array(displacement)

		# self.t_ac = np.arange(self.temporal_indices[-1]-self.temporal_indices[0])
		self.t_ac = np.arange(self.temporal_indices[-n]-self.temporal_indices[0])
		# here I compute autocorrelation
		# the function to compute it is defined in common.py
		# self.ac = autocorrelation2d(self.dr1)
		self.ac = autocorrelation2d(self.drn)
		# remember that self.ac is both autocorrelation and counts! (see the common.py)

	# here autocorrelation for single particle/track is computed
	def compute_autocorrelation_raw(self,n=1):

		# self.dr1 = np.zeros((self.temporal_indices[-1]-self.temporal_indices[0], 3))
		self.drn = np.zeros((self.temporal_indices[-1]-n+1-self.temporal_indices[0], 3))

		# here I create a list of all displacements with lag
		# (difference in temporal indices) of n
		for dr in self.drs:
			start = dr[0]-self.temporal_indices[0]
			lag = dr[1]
			displacement = dr[2:5]
			# if lag == 1:
			if lag == n:
				# self.dr1[start] = np.array(displacement)
				self.drn[start] = np.array(displacement)

		# self.t_ac = np.arange(self.temporal_indices[-1]-self.temporal_indices[0])
		self.t_ac = np.arange(self.temporal_indices[-n]-self.temporal_indices[0])
		# here I compute autocorrelation
		# the function to compute it is defined in common.py
		# self.ac = autocorrelation2d(self.dr1)
		self.ac_raw = autocorrelation2d_raw(self.drn,n)
		# remember that self.ac is both autocorrelation and counts! (see the common.py)

	#-------------------------------------------------------------------------------

	def __str__(self):

		return "{}#{}: {}".format(self.label, self.id, self.rs)

	#-------------------------------------------------------------------------------

	def __repr__(self):

		return self.__str__()

	#-------------------------------------------------------------------------------

	def __eq__(self, p):

		if isinstance( p, Particle ):
			return ( np.all( self.rs == p.rs ) ) and ( self.id == p.id ) and ( self.label == p.label )
		return False

#-------------------------------------------------------------------------------

def pointer(particle1, particle2, index):

	return particle2.rs[index] - particle1.rs[index]

#-------------------------------------------------------------------------------

def pointer_pbc(particle1, particle2, box_size):

	r = pointer(particle1, particle2)

	for i in range(3):
		while r[i] >= box_size/2:
			r[i] -= box_size
		while r[i] <= -box_size/2:
			r[i] += box_size

	return r

#-------------------------------------------------------------------------------

def distance(particle1, particle2, index):

	r = pointer(particle1, particle2, index)

	return np.sqrt( r[0]*r[0] + r[1]*r[1] + r[2]*r[2] )

#-------------------------------------------------------------------------------

def distance_pbc(particle1, particle2, box_size):

	r = pointer_pbc(particle1, particle2, box_size)

	return math.sqrt( r[0]*r[0] + r[1]*r[1] + r[2]*r[2] )

#-------------------------------------------------------------------------------

def get_particle_with_id(particles, particle_id):

	for i in range(len(particles)):

		if particles[i].id == particle_id: return particles[i]

	return None

#-------------------------------------------------------------------------------