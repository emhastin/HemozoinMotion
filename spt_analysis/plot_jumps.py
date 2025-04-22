import numpy as np
import os
import sys

import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator, FuncFormatter)

from common import fit_curve_to_data

chosen_lag = int(sys.argv[1])
jump_systems = sys.argv[2:]

# Import config (FIXME: change the path accordingly)
configfile = 'Config.pyc'
sys.path.append(os.path.dirname(os.path.expanduser(configfile)))
from Config import (plot_config,my_formatter)
# Set the config
plot_config()

fig, ax = plt.subplots()
DefaultSize = fig.get_size_inches()
fig.set_size_inches( (DefaultSize[0]/2, DefaultSize[1]/2) )

# label formatter (in Config.py)
formatter = FuncFormatter(my_formatter)

# create grid
nx=1
ny=1
grid = plt.GridSpec(nrows=ny, ncols=nx, wspace=0.2, hspace=0.8)

################
# Subplot a
################
axa = plt.subplot(grid[0, 0])
# axa.axis('off')
# axa.text(-0.15, 1.1, r'\bf{a}', {'color': 'black', 'fontsize': 14}, horizontalalignment='left', 
        # verticalalignment='center', rotation=0, clip_on=False, transform=axa.transAxes)

axa.set_xlabel(r'$\vert \Delta r \vert$ ($\si{\micro\meter}$)')
axa.set_ylabel(r'$\mathcal{P}(\vert \Delta r \vert)$ $(\si{\per\micro\meter})$')

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
# axb = plt.subplot(grid[0, 1])
# axb.axis('off')
# axb.text(-0.15, 1.1, r'\bf{b}', {'color': 'black', 'fontsize': 14}, horizontalalignment='left', 
#         verticalalignment='center', rotation=0, clip_on=False, transform=axb.transAxes)

# axb.set_xlabel(r'$\vert \Delta r \vert$ ($\si{\micro\meter}$)')

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

for j, jump_system in enumerate(jump_systems):

	jump_filename = 'data/jumps_{}_lag_{}.dat'.format(jump_system, chosen_lag)

	jumps, prob = np.transpose( np.genfromtxt(jump_filename, skip_header=1) )

	axa.plot(jumps, prob, '-', color = colors[j], label = '{}'.format(jump_system))

axa.set_title(r'Lag = {}'.format(chosen_lag))

axa.legend(fontsize=8)

# norm_diff = lambda x,D: 4*D*x
# norm_diff_stat_loc_err = lambda x,D,s: 2*s**2+4*D*x
# anom_diff = lambda x,D,a: 4*D*x**a 
# anom_diff_stat_loc_err = lambda x,D,a,s: 2*s**2+4*D*x**a 

# coeff, _ = fit_curve_to_data(norm_diff, times, tamsd, fitting_range=[1,5])
# print(coeff)

# axb.plot(times, norm_diff(times, *coeff), ':', color = 'black')

# coeff, _ = fit_curve_to_data(norm_diff_stat_loc_err, times, tamsd, fitting_range=[1,5])
# print(coeff)

# axb.plot(times, norm_diff_stat_loc_err(times, *coeff), ':', color = 'black')

# coeff, _ = fit_curve_to_data(anom_diff_stat_loc_err, times, tamsd, fitting_range=[1,5])
# print(coeff)

# axb.plot(times, anom_diff_stat_loc_err(times, *coeff), ':', color = 'black')

# coeff, _ = fit_curve_to_data(anom_diff_stat_loc_err, times, tamsd, fitting_range=[1,151])
# print(coeff)

# # axb.plot(times, anom_diff_stat_loc_err(times, *coeff), ':', color = 'black')
# print()

# axb.plot(times, 4*0.5*times, ':', color = 'black')
# axb.plot(times, 4*1.4*times, ':', color = 'black')
# axb.plot(times, 4*2.0*times, ':', color = 'black')
# axb.plot(times, 4*3.0*times, ':', color = 'black')

# axb.plot(times, msds, '-', color = colors[index], label = 'Exp. {}'.format(index+1))
# axb.fill_between(times, np.array(msds)+np.array(dmsds), np.array(msds)-np.array(dmsds), color = colors[index], alpha = 0.4)
# axb.plot(times, msds_no_ta[:len(times)], '--', color = colors[index])
# axb.plot(times, linear_einstein(times, Dprime), ':', color = 'red', label = r'fit, $D=$' + '{:.2f}'.format(Dprime) + r'$\si{\micro\meter\squared\per\second}$')

# axb.legend()

####################
# Save the beast
####################
name=os.path.basename(sys.argv[0])[:-2]+'pdf'
plt.savefig(name, bbox_inches = 'tight', dpi = 100)