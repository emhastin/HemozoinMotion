import numpy as np
import os
import sys

import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator, FuncFormatter)

from common import perform_unweighted_fit, anom_diff_stat_loc_err, anom_diff, norm_diff

zoom_range = int(sys.argv[1])
tamsd_systems = sys.argv[2:]

# Import config (FIXME: change the path accordingly)
configfile = 'Config.pyc'
sys.path.append(os.path.dirname(os.path.expanduser(configfile)))
from Config import (plot_config,my_formatter)
# Set the config
plot_config()

fig, ax = plt.subplots()
DefaultSize = fig.get_size_inches()
fig.set_size_inches( (DefaultSize[0], DefaultSize[1]/2) )

# label formatter (in Config.py)
formatter = FuncFormatter(my_formatter)

# create grid
nx=2
ny=1
grid = plt.GridSpec(nrows=ny, ncols=nx, wspace=0.2, hspace=0.8)

################
# Subplot a
################
axa = plt.subplot(grid[0, 0])
# axa.axis('off')
axa.text(-0.15, 1.1, r'\bf{a}', {'color': 'black', 'fontsize': 14}, horizontalalignment='left', 
        verticalalignment='center', rotation=0, clip_on=False, transform=axa.transAxes)

axa.set_xlabel(r'Lag')
axa.set_ylabel(r'TAM(SD$/\Delta t)$ ($\si{\micro\meter\squared\per\second}$)')

# axa.set_xlim(0, 0.04)
# axa.set_ylim(0, 0.2)

# # Ticks
# axa.xaxis.set_major_locator(MultipleLocator(0.01))
# axa.xaxis.set_major_formatter(formatter)
# axa.xaxis.set_minor_locator(MultipleLocator(0.002))
# axa.yaxis.set_major_locator(MultipleLocator(0.05))
# axa.yaxis.set_major_formatter(formatter)
# axa.yaxis.set_minor_locator(MultipleLocator(0.01))

################
# Subplot b
################
axb = plt.subplot(grid[0, 1])
# axb.axis('off')
axb.text(-0.15, 1.1, r'\bf{b}', {'color': 'black', 'fontsize': 14}, horizontalalignment='left', 
        verticalalignment='center', rotation=0, clip_on=False, transform=axb.transAxes)

axb.set_xlabel(r'Lag')

# axb.set_xlim(0, 150)
# axb.set_ylim(0, 1000)

# # Ticks
# axb.xaxis.set_major_locator(MultipleLocator(0.01))
# axb.xaxis.set_major_formatter(formatter)
# axb.xaxis.set_minor_locator(MultipleLocator(0.002))
# axb.yaxis.set_major_locator(MultipleLocator(0.05))
# axb.yaxis.set_major_formatter(formatter)
# axb.yaxis.set_minor_locator(MultipleLocator(0.01))

colors = ['black', 'red', 'blue', 'green', 'orange']

for j, tamsd_system in enumerate(tamsd_systems):

	print(tamsd_system)

	tamsd_filename = 'data/tamsd_tdiv_{}.dat'.format(tamsd_system)
	tamsd_nondiv_filename = 'data/tamsd_{}.dat'.format(tamsd_system)

	times, tamsd = np.transpose( np.genfromtxt(tamsd_filename, skip_header=1) )
	times_nondiv, tamsd_nondiv = np.transpose( np.genfromtxt(tamsd_nondiv_filename, skip_header=1) )

	axa.plot(times, tamsd, '-', color = colors[j], label = '{}'.format(tamsd_system))
	axb.plot(times[:zoom_range], tamsd[:zoom_range], '-', color = colors[j], label = '{}'.format(tamsd_filename))

	dt = times_nondiv[1]-times_nondiv[0]
	axa.plot(times_nondiv/dt, tamsd_nondiv/dt, ':', color = colors[j], label = '{}'.format(tamsd_system))
	axb.plot(times_nondiv[:zoom_range]/dt, tamsd_nondiv[:zoom_range]/dt, ':', color = colors[j], label = '{}'.format(tamsd_filename))

	# perform_unweighted_fit(norm_diff, times, tamsd, 0, 200)
	# perform_unweighted_fit(norm_diff, times, tamsd, 20, 200)

	# fit = np.polyfit(times[1:zoom_range], tamsd[1:zoom_range], deg=1)
	# print(fit)
	# norm_fit = lambda t,D,b: 4*D*t+b
	# coeff, _ = fit_curve_to_data(norm_fit, times[1:zoom_range], tamsd[1:zoom_range], p0=[0.35,0.0])
	# print(coeff)
	# axb.plot(times[1:zoom_range], norm_fit(times[1:zoom_range], *coeff), ':', color = colors[j])

	# anom_fit = lambda t,D,a: 4*D*t**a
	# coeff, _ = fit_curve_to_data(anom_fit, times[1:zoom_range], tamsd[1:zoom_range], p0=[0.35, 0.8])
	# print(coeff)

# axb.plot(times[:zoom_range], 4*0.18*times[:zoom_range]**0.72+4.4, '--')
# axb.plot(times[:zoom_range], 4*1.07*times[:zoom_range]**0.67+4.4, '--')

axa.plot([0.0], [0.0], 'x', color='black')
axb.plot([0.0], [0.0], 'x', color='black')

axa.legend(fontsize=8)

####################
# Save the beast
####################
name=os.path.basename(sys.argv[0])[:-2]+'pdf'
plt.savefig(name, bbox_inches = 'tight', dpi = 100)
name=os.path.basename(sys.argv[0])[:-2]+'png'
plt.savefig(name, bbox_inches = 'tight', dpi = 300)