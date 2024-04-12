from __future__ import division
import numpy as np
import os
import matplotlib as plt
from pylab import *


def power_spectrum(data, prm):
    ps = np.abs(np.fft.fft(data))**2

    time_step = 1 / 30  # 30 Hz sampling
    freqs = np.fft.fftfreq(data.size, time_step)
    idx = np.argsort(freqs)
    return freqs, idx, ps



def plot_power_spectrum(freqs, idx, ps, prm):
    save_path = prm.get_file_path() + '/plots/'
    if os.path.exists(save_path) is False:
        os.makedirs(save_path)

    plot(freqs[idx], ps[idx])                  # Plot spectrum vs frequency
    xlim([0, 20])                          # Select frequency range
    xlabel('Frequency [Hz]')                # Label the axes
    ylabel('Power [$\mu V^2$/Hz]')
    savefig( prm.get_file_path() + '/plots/power_spectrum2.png')



