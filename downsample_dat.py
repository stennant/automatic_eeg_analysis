import parameters
import sys
import os.path
import numpy as np
from numpy import *
import os
import matplotlib.pyplot as plt
import mne
import pandas as pd
import read_yaml_config
import scipy

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

def process_dir(file_name):
    # Load the raw (1-D) data
    dat_raw = np.fromfile(file_name, dtype=prm.get_sample_datatype())

    # Reshape the (2-D) per channel data
    step = prm.get_number_of_channels() * prm.get_display_decimation()
    dat_chans = [dat_raw[c::step] for c in range(prm.get_number_of_channels())]

    # Build the time array
    data=np.array(dat_chans)

    del(dat_chans)
    #channel_names=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']
    #channel_types=['emg','misc','eeg','misc','misc','misc','emg','misc','misc','misc','misc','misc','eeg','misc','misc','eeg']

    channel_names=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32']
    channel_types=['emg','misc','eeg','misc','misc','misc','emg','misc','misc','misc','misc','misc','eeg','misc','misc','eeg', 'emg','misc','eeg','misc','misc','misc','emg','misc','misc','misc','misc','misc','eeg','misc','misc','eeg']

    # This creates the info that goes with the channels, which is names, sampling rate, and channel types
    info = mne.create_info(channel_names, prm.get_sampling_rate(), channel_types)

    # This makes the object that contains all the data and info about the channels. Computations like plotting, averaging, power spectrums can be performed on this object
    custom_raw = mne.io.RawArray(data, info)
    cropped_raw = custom_raw.crop(0, 14400) # testing dataset - 52800, 52805 for seizure, 52910, 52915 for non seizure, 52782, 52812 for both
    return cropped_raw


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
            downsampled_eeg_data_1 = downsampled_trace
        elif channel > 0 and channel < 16:
            downsampled_eeg_data_1 = np.hstack((downsampled_eeg_data_1, downsampled_trace))
        elif channel == 16:
            downsampled_eeg_data_2 = downsampled_trace
        elif channel > 16:
            downsampled_eeg_data_2 = np.hstack((downsampled_eeg_data_2, downsampled_trace))
        else:
            print(channel, "channel")
    return downsampled_eeg_data_1, downsampled_eeg_data_2


def save_dat(data_1, data_2):
    output_df_1 = pd.DataFrame(data_1)
    output_df_1.to_csv('/Users/sarahtennant/Work_Alfredo/Analysis/SYNGAPE8/DATA/SYNGAPE8/SYNGAPE8_1755488/1755488_continuous_downsampled.dat')

    output_df_2 = pd.DataFrame(data_2)
    output_df_2.to_csv('/Users/sarahtennant/Work_Alfredo/Analysis/SYNGAPE8/DATA/SYNGAPE8/SYNGAPE8_1755486/1755486_continuous_downsampled.dat')
    return




def main():
    print('-------------------------------------------------------------')
    print('-------------------------------------------------------------')

    #path to the recording .dat file
    file_path = '/Users/sarahtennant/Work_Alfredo/Analysis/SYNGAPE8/DATA/SYNGAPE8/SYNGAPE8_1755486/' # for syngape8 rats
    recording = '1755488-86_continuous.dat' # for rat 176923

    file_name = file_path + recording
    parameters(file_path)
    print('Processing ' + str(file_path + recording))

    #set path to save data
    output_path = '/Users/sarahtennant/Work_Alfredo/Analysis/SYNGAPE8/Figures'
    # if the output path does not exist, make it
    if os.path.exists(output_path) is False:
        os.makedirs(output_path)

    # LOAD DATA
    eeg_data = process_dir(file_name) # overall data
    print("dataset loaded")

    # Downsample data from 1 kHz to 250 Hz
    downsampled_eeg_data_1,downsampled_eeg_data_2  = downsample_all_traces(eeg_data)
    print("dataset downsampled")

    # SAVE DATA
    save_dat(downsampled_eeg_data_1,downsampled_eeg_data_2)
    print("dataset saved")



if __name__ == '__main__':
    main()

