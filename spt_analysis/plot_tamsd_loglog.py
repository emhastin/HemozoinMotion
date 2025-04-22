import numpy as np
import os
import sys

import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator, FuncFormatter)

from common import fit_curve_to_data, weighted_fit_curve_to_data, norm_diff, norm_diff_stat_loc_err, anom_diff, anom_diff_stat_loc_err, perform_weighted_fit

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
fig.set_size_inches( (3*DefaultSize[0]/2, DefaultSize[1]/2) )

# label formatter (in Config.py)
formatter = FuncFormatter(my_formatter)

# create grid
nx=3
ny=1
grid = plt.GridSpec(nrows=ny, ncols=nx, wspace=0.2, hspace=0.8)

################
# Subplot a
################
axa = plt.subplot(grid[0, 0])
# axa.axis('off')
axa.text(-0.15, 1.1, r'\bf{a}', {'color': 'black', 'fontsize': 14}, horizontalalignment='left', 
        verticalalignment='center', rotation=0, clip_on=False, transform=axa.transAxes)

axa.set_xlabel(r'$t$ $(\si{\second})$')
axa.set_ylabel(r'TAMSD ($\si{\micro\meter\squared}$)')

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

axb.set_xlabel(r'$t$ $(\si{\second})$')

# axb.set_xlim(0, 150)
# axb.set_ylim(0, 1000)

# # Ticks
# axb.xaxis.set_major_locator(MultipleLocator(0.01))
# axb.xaxis.set_major_formatter(formatter)
# axb.xaxis.set_minor_locator(MultipleLocator(0.002))
# axb.yaxis.set_major_locator(MultipleLocator(0.05))
# axb.yaxis.set_major_formatter(formatter)
# axb.yaxis.set_minor_locator(MultipleLocator(0.01))

################
# Subplot c
################
axc = plt.subplot(grid[0, 2])
# axb.axis('off')
axc.text(-0.15, 1.1, r'\bf{c}', {'color': 'black', 'fontsize': 14}, horizontalalignment='left', 
        verticalalignment='center', rotation=0, clip_on=False, transform=axc.transAxes)

axc.set_xlabel(r'$t$ $(\si{\second})$')

axc.set_xscale('log')
axc.set_yscale('log')

colors = ['black', 'red', 'blue', 'green', 'orange', 'pink']

for j, tamsd_system in enumerate(tamsd_systems):

	tamsd_filename = 'data/tamsd_{}.dat'.format(tamsd_system)
	tamsd_errorbars_filename = 'data/tamsd_errorbars_{}.dat'.format(tamsd_system)
	print(tamsd_filename)

	times, tamsd = np.transpose( np.genfromtxt(tamsd_filename, skip_header=1) )
	_, _, dtamsd, _ = np.transpose( np.genfromtxt(tamsd_errorbars_filename, skip_header=1) )

	dtamsd[np.isinf(dtamsd)] = 1000000
	dtamsd[np.isnan(dtamsd)] = 1000000

	# perform_weighted_fit(norm_diff_stat_loc_err, times, tamsd, dtamsd, 0, 5)

	# perform_weighted_fit(anom_diff_stat_loc_err, times, tamsd, dtamsd, 0, 200)
	# perform_weighted_fit(norm_diff_stat_loc_err, times, tamsd, dtamsd, 0, 200)

	# perform_weighted_fit(anom_diff_stat_loc_err, times, tamsd, dtamsd, 20, 100)
	# perform_weighted_fit(norm_diff_stat_loc_err, times, tamsd, dtamsd, 20, 100)

	# perform_weighted_fit(anom_diff_stat_loc_err, times, tamsd, dtamsd, 20, 200)
	# perform_weighted_fit(norm_diff_stat_loc_err, times, tamsd, dtamsd, 20, 200)
	# print()

	# my_Ds = [0.488, 0.488/3.55, 0.488/14.85]
	# axb.plot(times[:zoom_range], 4*my_Ds[j]*times[:zoom_range], ':', color = colors[j])
	# axb.set_xlim(0,1)
	# axb.set_ylim(0,0.5)

	dtamsd[dtamsd == 1000000] = np.nan

	axa.plot(times, tamsd, '-', color = colors[j], label = '{}'.format(tamsd_system))
	axb.errorbar(times[:zoom_range], tamsd[:zoom_range], dtamsd[:zoom_range], None, '.', color = colors[j], label = '{}'.format(tamsd_filename), fillstyle='none', elinewidth = 0.5, capsize = 1, capthick = 0.5, barsabove = True, markersize=0.5)

	axc.plot(times, tamsd, '-', color = colors[j], label = '{}'.format(tamsd_system))

axa.plot([0.0], [0.0], 'x', color='black')
axb.plot([0.0], [0.0], 'x', color='black')

# axb.plot(times[:zoom_range], 4*0.09950*times[:zoom_range]+0.02294, '--')

axa.legend(fontsize=8)

norm_diff = lambda x,D: 4*D*x
norm_diff_stat_loc_err = lambda x,D,s: 2*s**2+4*D*x
anom_diff = lambda x,D,a: 4*D*x**a 
anom_diff_stat_loc_err = lambda x,D,a,s: 2*s**2+4*D*x**a 

# print('normal, from 0 to zoom range')
# coeff, _ = fit_curve_to_data(norm_diff, times, tamsd, fitting_range=[0,zoom_range])
# print(coeff)

# print('normal, from 5 to zoom range')
# coeff, _ = fit_curve_to_data(norm_diff, times, tamsd, fitting_range=[5,zoom_range])
# print(coeff)

# print('anom, from 0 to zoom range')
# coeff, _ = fit_curve_to_data(anom_diff, times, tamsd, fitting_range=[0,zoom_range])
# print(coeff)

# print('anom, from 5 to zoom range')
# coeff, _ = fit_curve_to_data(anom_diff, times, tamsd, fitting_range=[5,zoom_range])
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