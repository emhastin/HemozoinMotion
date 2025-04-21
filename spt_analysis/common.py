import numpy as np
from scipy.optimize import curve_fit

def autocorrelation(x):
	x = np.array(x)
	xn = x - np.mean(x)
	a = np.correlate(xn, xn, 'full')
	a = a[a.size//2:]
	a /= np.max(a)
	return a

def autocorrelation2d(steps):
	def _ac(k,j):
		# here I compute single dot product divided by vector lengths
		# so the cos of angle between them
		# but only if the displacement is not 0.0, 0.0, 0.0
		# because it means that there was jump in times in your xml
		# like 1,2,3,4, 6,7,...	
		# this is because dot product with (0,0,0) vector is problematic here
		if np.all(steps[k] == np.zeros(3)) or np.all(steps[k+j] == np.zeros(3)): return 0.0
		else: return np.dot(steps[k], steps[k+j])/np.sqrt(np.dot(steps[k], steps[k])*np.dot(steps[k+j], steps[k+j]))

	# we iterate over steps, compute this normed dot products and add them to
	# corresponding fields in the array, keeping track of how many we add to
	# compute the average based on that
	autocorrelation_alt = np.zeros(np.shape(steps)[0])
	count = np.zeros(len(autocorrelation_alt), dtype=int)
	for j in range(len(steps)):
		for k in range(len(steps)-j):
			ac_value = _ac(k,j)
			if ac_value == 0.0:
				continue
			else:
				count[j] += 1
				autocorrelation_alt[j] += ac_value

	# we divide sums by counts to have averages
	autocorrelation_alt/=count
	autocorrelation_alt[count==0.0]=0.0
	assert len(autocorrelation_alt)==len(steps)
	# notice that it returns the count as well, because we want
	# to correctly average it with what we get from the other particles
	# these counts will determine weights then
	return autocorrelation_alt, count

def autocorrelation2d_raw(steps,lag=1):
	def _ac(k,j):
		# here I compute single dot product divided by vector lengths
		# so the cos of angle between them
		# but only if the displacement is not 0.0, 0.0, 0.0
		# because it means that there was jump in times in your xml
		# like 1,2,3,4, 6,7,...	
		# this is because dot product with (0,0,0) vector is problematic here
		if np.all(steps[k] == np.zeros(3)) or np.all(steps[k+j] == np.zeros(3)): return 0.0
		else: return np.dot(steps[k], steps[k+j])/np.sqrt(np.dot(steps[k], steps[k])*np.dot(steps[k+j], steps[k+j]))

	# we iterate over steps, compute this normed dot products and add them to
	# corresponding lists in the array
	autocorrelation = [ [] for j in range(len(steps)) ]
	for j in range(len(steps)):
		for k in range(len(steps)-j):
			if not k%lag==0: continue
			ac_value = _ac(k,j)
			if ac_value == 0.0:
				continue
			else:
				autocorrelation[j].append(ac_value)
	return autocorrelation

def fit_curve_to_data(curve, x_data, y_data, fitting_range = [0, None], p0=None):
	return curve_fit(curve, x_data[fitting_range[0]:fitting_range[1]], y_data[fitting_range[0]:fitting_range[1]], p0=p0, maxfev=10000, full_output=True)

def weighted_fit_curve_to_data(curve, x_data, y_data, y_errors, fitting_range = [0, None], p0=None):
	return curve_fit(curve, x_data[fitting_range[0]:fitting_range[1]], y_data[fitting_range[0]:fitting_range[1]], p0=p0, sigma=y_errors[fitting_range[0]:fitting_range[1]], absolute_sigma=True, full_output=True, maxfev = 10000, bounds=(0,40))

def unweighted_fit_curve_to_data(curve, x_data, y_data, fitting_range = [0, None], p0=None):
	return curve_fit(curve, x_data[fitting_range[0]:fitting_range[1]], y_data[fitting_range[0]:fitting_range[1]], p0=p0, full_output=True, maxfev = 10000)

def sphere_to_disc_concentration(x, x0, R):
	return np.pi*(R**2 - (x-x0)**2) / (4/3*np.pi*R**3)

def sphere_to_disc_radial_concentration(r, R):
	return 4 * np.pi * r * np.sqrt(R**2 - r**2) / (4/3*np.pi*R**3)

def tolerant_mean(arrs):
    lens = [len(i) for i in arrs]
    arr = np.ma.empty((np.max(lens),len(arrs)))
    arr.mask = True
    for idx, l in enumerate(arrs):
        arr[:len(l),idx] = l
    return arr.mean(axis = -1)

def position_histogram(particles, number_of_bins, index_range = None):
	if index_range is None:
		xs = [ p.rs[i][0] for p in particles for i in range(len(p.rs)) ]
		ys = [ p.rs[i][1] for p in particles for i in range(len(p.rs)) ]		
	else:
		xs = [ p.rs[i][0] for p in particles for i in range(*index_range) ]
		ys = [ p.rs[i][1] for p in particles for i in range(*index_range) ]
	x_counts, x_bins = np.histogram(xs, number_of_bins, density = True)
	y_counts, y_bins = np.histogram(ys, number_of_bins, density = True)
	x_bin_centers = 0.5*(x_bins[1:] + x_bins[:-1])
	y_bin_centers = 0.5*(y_bins[1:] + y_bins[:-1])
	return x_bin_centers, x_counts, y_bin_centers, y_counts

def compute_msds(particles, time_average = True, index_range = [0, None]):
	drs = [ p.compute_displacements(index_range) for p in particles ]
	if not time_average: drs = [ [ [ drs[i][j][0] ] for j in range(len(drs[i])) ] for i in range(len(drs)) ]
	max_len = np.max([len(dr) for dr in drs])
	drs_total = [ [] for i in range(max_len) ]
	for i in range(max_len):
		for j, p in enumerate(particles):
			if (i < (p.length-1) ): drs_total[i] += drs[j][i]
	msds = [ np.mean( np.sum( np.array(dr_total)**2, axis = 1 ) ) for dr_total in drs_total ]
	dmsds = []
	for dr_total in drs_total:
		if len(dr_total) > 5:
			msdi = []
			for i in range(5):
				msdi.append( np.mean( np.sum( np.array(dr_total[i*len(dr_total)//5:(i+1)*len(dr_total)//5])**2, axis = 1 ) ) )
			dmsds.append(np.std(msdi)/5)
		else:
			dmsds.append(np.inf)
	# dmsds = [ np.std( np.sum( np.array(dr_total)**2, axis = 1 ) ) / len(dr_total) for dr_total in drs_total ]
	return msds, dmsds

def norm_diff(x, D):
        return 4*D*x
def norm_diff_stat_loc_err(x, D, s):
        return s+4*D*x
def anom_diff(x, D, a):
        return 4*D*x**a 
def anom_diff_stat_loc_err(x, D, a, s):
        return s+4*D*x**a 

def perform_weighted_fit(model, x, y, dy, start, end):
        # print(x[start:end])
        # print(y[start:end])
        # print(dy[start:end])
        opt = weighted_fit_curve_to_data(model, x, y, dy, fitting_range=[start,end])
        params = opt[0]
        dparams = np.sqrt(np.diag(opt[1]))
        print('Fitting data with model: {}, from {} to {}'.format(model.__name__, start, end))
        print('(range: from {} s to {} s)'.format(x[start], x[end]))
        print('{}+/-{}'.format(params,dparams))
        print()
        return params, dparams

def perform_unweighted_fit(model, x, y, start, end):
        opt = unweighted_fit_curve_to_data(model, x, y, fitting_range=[start,end])
        params = opt[0]
        dparams = np.sqrt(np.diag(opt[1]))
        print('Fitting data with model: {}, from {} to {}'.format(model.__name__, start, end))
        print('(range: from {} s to {} s)'.format(x[start], x[end]))
        print('{}+/-{}'.format(params,dparams))
        print()
        return params, dparams