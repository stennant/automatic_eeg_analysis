import parameters as parameters

import parameters
import sys
import os.path
import numpy as np
from numpy import *
import os
import matplotlib.pyplot as plt
import mne
from scipy import signal
from pylab import *
from numpy.fft import fft, rfft
from scipy.signal import spectrogram
import csv


prm = parameters.Parameters()

# set global parameters
def parameters(recording_folder):
    prm.set_file_path(recording_folder)
    prm.set_local_recording_folder_path(recording_folder)
    prm.set_output_path(recording_folder)
    prm.set_sampling_rate(250.4)
    prm.set_number_of_channels(16)
    prm.set_sample_datatype('int16')
    prm.set_display_decimation(1)
    prm.set_start_sample(15054049)
    prm.set_end_sample(36688608)


def process_dir(file_name):
    # Load the raw (1-D) data
    dat_raw = np.fromfile(file_name, dtype=prm.get_sample_datatype())

    # Reshape the (2-D) per channel data
    step = prm.get_number_of_channels() * prm.get_display_decimation()
    dat_chans = [dat_raw[c::step] for c in range(prm.get_number_of_channels())]

    # Build the time array
    data=np.array(dat_chans)

    del(dat_chans)
    channel_names=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']
    channel_types=['emg','misc','eeg','misc','misc','misc','emg','misc','misc','misc','misc','misc','eeg','misc','misc','eeg']

    # This creates the info that goes with the channels, which is names, sampling rate, and channel types
    info = mne.create_info(channel_names, prm.get_sampling_rate(), channel_types)

    # This makes the object that contains all the data and info about the channels. Computations like plotting, averaging, power spectrums can be performed on this object
    custom_raw = mne.io.RawArray(data, info)

    return custom_raw



def power_spectra(eeg_data):
    print('plotting snippet of data...')
    save_path = prm.get_file_path + '/plots'
    if os.path.exists(save_path) is False:
        os.makedirs(save_path)
    x = np.array(eeg_data.iloc[:, 3]) # extract the channel we want to analyse
    t = np.array(eeg_data.index/250.4)  # ... extract the t variable
    dt = t[1] - t[0]  # Define the sampling interval

    plot(t, x)                            # Plot the data versus time
    xlabel('Time [s]')                      # Label the time axis
    ylabel('Voltage [$\mu V$]')             # ... and the voltage axis
    autoscale(tight=True)                   # Minimize white space
    savefig(prm.get_file_path + '/plots/channel4.png')

    N = x.shape[0]    # Define the total number of data points
    T = N * dt        # Define the total duration of the data
    xf = fft(x - x.mean())                  # Compute Fourier transform of x
    Sxx = 2 * dt ** 2 / T * (xf * conj(xf)) # Compute spectrum
    Sxx = Sxx[:int(len(x) / 2)]             # Ignore negative frequencies

    df = 1 / T.max()                        # Determine frequency resolution
    fNQ = 1 / dt / 2                        # Determine Nyquist frequency
    faxis = arange(0,fNQ,df)                # Construct frequency axis

    plot(faxis, real(Sxx))                  # Plot spectrum vs frequency
    xlim([0, 100])                          # Select frequency range
    xlabel('Frequency [Hz]')                # Label the axes
    ylabel('Power [$\mu V^2$/Hz]')
    savefig( prm.get_file_path + '/plots/channel4_powerspec.png')

    return real(Sxx)



def main():
    print('-------------------------------------------------------------')
    print('-------------------------------------------------------------')

    file_path = '/Users/sarahtennant/Work_Alfredo/Analysis/EOUBE/DATA/EOUBE/EOUBE_445redo'
    recording = '/TAINI_1044_C_445redo_EOUBE_EM_10-2024_02_06-0001.dat'
    file_name = file_path + recording

    parameters(file_path)
    print('Processing ' + str(file_path + recording))

    # LOAD DATA
    eeg_data = process_dir(file_name) # overall data

    data = eeg_data.to_data_frame()
    eeg_data = data.head(n=1000)

    # Power spectra on all data
    power_spectra(eeg_data)

if __name__ == '__main__':
    main()

