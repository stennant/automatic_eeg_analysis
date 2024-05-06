import parameters
import sys
import os.path
import os
import mne
import numpy as np
import pandas as pd
import scipy
from OpenEphys import file_utility
from OpenEphys import Load_OpenEphys_AllTetrodes
import downsample_dat
import matplotlib.pyplot as plt

prm = parameters.Parameters()


# set global parameters
def parameters(recording_folder):
    prm.set_file_path(recording_folder)
    prm.set_local_recording_folder_path(recording_folder)
    prm.set_output_path(recording_folder)
    prm.set_sampling_rate(2000)
    prm.set_number_of_channels(32)
    prm.set_sample_datatype('int16')
    prm.set_display_decimation(1)
    file_utility.init_data_file_names(prm, '100_RhythmData_CH', '')  # currently used


def init_data_file_names(prm, beginning, end):
    prm.set_continuous_file_name(beginning)
    prm.set_continuous_file_name_end(end)


def set_continuous_data_path(prm):
    file_path = prm.get_file_path()
    continuous_file_name = '100_RhythmData_CH'
    continuous_file_name_end = ''

    recording_path = file_path + continuous_file_name + str(1) + continuous_file_name_end + '.continuous'
    if os.path.isfile(recording_path) is True:
        init_data_file_names(prm, continuous_file_name, continuous_file_name_end)


def process_dir(file_name):

    # Load the raw (1-D) data
    file_utility.set_continuous_data_path(prm)

    custom_raw = Load_OpenEphys_AllTetrodes.load_continuous(prm)

    return custom_raw



def plot_raw(eeg_data,file_name):
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

    return eeg_data



def downsample_dat(trace, down):
    downsampled = scipy.signal.resample(trace, int(np.shape(trace)[0] / down))
    return downsampled


def downsample_all_traces(eeg_data):
    data = eeg_data.to_data_frame()
    print("downsampling data...")

    for channel in range((prm.get_number_of_channels())):
        print(channel)
        trace = data.iloc[:3600000, channel]
        downsampled_trace = downsample_dat(trace, 8)
        if channel == 0:
            downsampled_eeg_data = downsampled_trace
        else:
            downsampled_eeg_data = np.hstack((downsampled_eeg_data, downsampled_trace))

    return downsampled_eeg_data



def save_dat_files(data):
    output_df_1 = pd.DataFrame(data)
    output_df_1.to_csv('/Users/sarahtennant/Work_Alfredo/Analysis/SYNGAPE8/DATA/SYNGAPE8/SYNGAPE8_1755488/1755488_continuous_downsampled.dat')




def main():
    print('-------------------------------------------------------------')
    print('-------------------------------------------------------------')

    #path to the recording .dat file
    file_name = '/Users/sarahtennant/Work_Alfredo/Analysis/OpenEphys/15W/1755485_20240310/5485_1 15W2024-03-10_10-31-27/RecordNode101/'

    parameters(file_name)
    #print('Processing ' + str(file_path + recording))

    # LOAD DATA
    eeg_data = process_dir(file_name) # overall data

    # PLOT DATA
    #plot_raw(eeg_data, output_path)

    # DOWNSAMPLE DATA
    data = downsample_all_traces()

    # SAVE DATA AS .DAT
    save_dat_files()


if __name__ == '__main__':
    main()

