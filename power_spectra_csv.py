import csv
import pandas as pd
import numpy as np
import os
from pylab import *

data = pd.read_csv("/Users/sarahtennant/Work_Alfredo/Analysis/EOUBE/OUTPUT/EOUBE/EOUBE_445redo/EOUBE_1044_BL1_Channels.csv")

file_path = '/Users/sarahtennant/Work_Alfredo/Analysis/EOUBE/OUTPUT/EOUBE/EOUBE_445redo'



def calculate_power_spectra(data):
    print('plotting snippet of data...')

    x = np.array(data.iloc[:, 0]) # extract the channel we want to analyse
    t = np.array(data.index/250.4)  # ... extract the t variable
    dt = t[1] - t[0]  # Define the sampling interval

    N = x.shape[0]    # Define the total number of data points
    T = N * dt        # Define the total duration of the data
    xf = fft(x - x.mean())                  # Compute Fourier transform of x
    Sxx = 2 * dt ** 2 / T * (xf * conj(xf)) # Compute spectrum
    Sxx = Sxx[:int(len(x) / 2)]             # Ignore negative frequencies

    df = 1 / T.max()                        # Determine frequency resolution
    fNQ = 1 / dt / 2                        # Determine Nyquist frequency
    faxis = arange(0,fNQ,df)                # Construct frequency axis

    print('plotting power spectra of data...')

    plot(faxis, real(Sxx))                  # Plot spectrum vs frequency
    xlim([0, 100])                          # Select frequency range
    ylim([0, 1.25])                          # Select frequency range
    xlabel('Frequency [Hz]')                # Label the axes
    ylabel('Power [$\mu V^2$/Hz]')
    savefig( file_path + '/channel4_powerspec.png')


    return real(Sxx)




x = calculate_power_spectra(data)
