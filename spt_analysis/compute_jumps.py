import numpy as np
import sys

analyzed_system = sys.argv[1]
chosen_lag = int(sys.argv[2])
n_bins = int(sys.argv[3])

data_filename = 'data/displacements_{}.dat'.format(analyzed_system)

times = []
jumps = []

with open(data_filename, 'r') as input_file:
        for line in input_file:
                if line[0] == '#': continue
                line_split = line.split(' ')
                start = int( line_split[0] )
                lag = int( line_split[1] )
                if lag != chosen_lag: continue
                dr = np.array( [float(line_split[2]), float(line_split[3]), float(line_split[4])] )
                dt = float( line_split[5] )
                jump = np.sqrt( np.sum(dr**2) )
                times.append(chosen_lag*dt)
                jumps.append(jump)

jumps_counts, jumps_bins = np.histogram(jumps, n_bins, density = True)
jumps_counts_hist, _ = np.histogram(jumps, n_bins, density = False)
jumps_counts_hist = jumps_counts_hist/np.sum(jumps_counts_hist)
jumps_bin_centers = 0.5 * (jumps_bins[1:] + jumps_bins[:-1])

jumps_tdiv_counts, jumps_tdiv_bins = np.histogram(jumps/np.sqrt(times), n_bins, density = True)
jumps_tdiv_counts_hist, _ = np.histogram(jumps/np.sqrt(times), n_bins, density = False)
jumps_tdiv_counts_hist = jumps_tdiv_counts_hist/np.sum(jumps_tdiv_counts_hist)
jumps_tdiv_bin_centers = 0.5 * (jumps_tdiv_bins[1:] + jumps_tdiv_bins[:-1])

np.savetxt('data/jumps_{}_lag_{}.dat'.format(analyzed_system, chosen_lag), np.transpose([jumps_bin_centers, jumps_counts]), header = 'jump P(jump)')
np.savetxt('data/jumps_tdiv_{}_lag_{}.dat'.format(analyzed_system, chosen_lag), np.transpose([jumps_tdiv_bin_centers, jumps_tdiv_counts]), header = 'jump/sqrt(time_res) P(jump/sqrt(time_res))')

np.savetxt('data/jumps_hist_{}_lag_{}.dat'.format(analyzed_system, chosen_lag), np.transpose([jumps_bin_centers, jumps_counts_hist]), header = 'jump P(jump)')
np.savetxt('data/jumps_tdiv_hist_{}_lag_{}.dat'.format(analyzed_system, chosen_lag), np.transpose([jumps_tdiv_bin_centers, jumps_tdiv_counts_hist]), header = 'jump/sqrt(time_res) P(jump/sqrt(time_res))')