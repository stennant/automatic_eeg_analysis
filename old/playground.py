import Parameters
import sys
import os.path
import numpy as np
from numpy import *
import os
import matplotlib.pyplot as plt
import mne
from scipy import signal

prm = Parameters.parameters()


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


def plot_raw_eeg_data(egg_data, prm):
    print('plotting ...')
    save_path = prm.get_file_path() + '/python'
    if os.path.exists(save_path) is False:
        os.makedirs(save_path)

    stops_on_track = plt.figure(figsize=(3,6))
    ax = stops_on_track.add_subplot(2, 1, 1)  # specify (nrows, ncols, axnum)
    window = signal.gaussian(2, std=3)
    channel_1 = np.array(egg_data.loc[:, 4])
    channel_1 = signal.convolve(channel_1, window, mode='same')/ sum(window)
    ax.plot(channel_1, '-', color='Black')
    plt.ylabel('Amplitude (uV)', fontsize=18, labelpad = 0)
    plt.xlabel('Time (sec)', fontsize=18, labelpad = 10)
    #plt.xlim(0,200)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')

    ax = stops_on_track.add_subplot(2, 1, 2)  # specify (nrows, ncols, axnum)
    window = signal.gaussian(2, std=3)
    channel_1 = np.array(egg_data.loc[:, 5])
    channel_1 = signal.convolve(channel_1, window, mode='same')/ sum(window)
    ax.plot(channel_1, '-', color='Black')
    plt.ylabel('Amplitude (uV)', fontsize=18, labelpad = 0)
    plt.xlabel('Time (sec)', fontsize=18, labelpad = 10)
    #plt.xlim(0,200)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    #Python_PostSorting.plot_utility.style_vr_plot(ax)
    #ax.set_xticklabels(['-30', '70', '170'])
    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
    plt.savefig(save_path + '/' + 'eeg_snippet' + '.png', dpi=200)
    plt.close()


def main():
    print('-------------------------------------------------------------')
    print('-------------------------------------------------------------')

    file_path = '/Users/sarahtennant/Work_Alfredo/Analysis/EOUBE/DATA/EOUBE/EOUBE_1044'
    recording = '/TAINI_1044_C_445redo_EOUBE_EM_10-2024_02_06-0001.dat'
    file_name = file_path + recording

    parameters(file_path)
    print('Processing ' + str(file_path + recording))

    # LOAD DATA
    eeg_data = process_dir(file_name) # overall data

    data = eeg_data.to_data_frame()
    eeg_data = data.tail(n=1000)

    # PLOT DATA
    plot_raw_eeg_data(eeg_data, file_name)



if __name__ == '__main__':
    main()

