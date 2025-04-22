import numpy as np
import os
import sys

import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator, FuncFormatter)

from common import norm_diff, norm_diff_stat_loc_err, norm_diff_fixed_stat_loc_err, anom_diff, anom_diff_stat_loc_err, anom_diff_fixed_stat_loc_err, perform_weighted_fit, perform_unweighted_fit

tamsd_system = sys.argv[1]
model = eval(sys.argv[2])
min_time = float(sys.argv[3])
max_time = float(sys.argv[4])
weighted = int(sys.argv[5])
shift = float(sys.argv[6])

print(weighted)

tamsd_filename = 'data/tamsd_{}.dat'.format(tamsd_system)
tamsd_errorbars_filename = 'data/tamsd_errorbars_{}.dat'.format(tamsd_system)

times, tamsd = np.transpose( np.genfromtxt(tamsd_filename, skip_header=1) )
if weighted: _, _, dtamsd, _ = np.transpose( np.genfromtxt(tamsd_errorbars_filename, skip_header=1) )

min_index = np.argmax(times>min_time)
max_index = np.argmax(times>max_time)

if weighted: perform_weighted_fit(model, times, tamsd-shift, dtamsd, min_index, max_index)
else: perform_unweighted_fit(model, times, tamsd-shift, min_index, max_index)

# import matplotlib.pyplot as plt
# plt.plot(times[min_index:max_index], tamsd[min_index:max_index])
# plt.plot(times[min_index:max_index], tamsd[min_index:max_index]-shift)
# plt.show()

####################
# Save the beast
####################
name=os.path.basename(sys.argv[0])[:-2]+'pdf'
plt.savefig(name, bbox_inches = 'tight', dpi = 100)