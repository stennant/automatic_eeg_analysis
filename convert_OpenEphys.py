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
    prm.set_sampling_rate(1000)
    prm.set_number_of_channels(64)
    prm.set_sample_datatype('int16')
    prm.set_display_decimation(1)
    file_utility.init_data_file_names(prm, '100_CH', '')  # currently used


def init_data_file_names(prm, beginning, end):
    prm.set_continuous_file_name(beginning)
    prm.set_continuous_file_name_end(end)


def set_continuous_data_path(prm):
    file_path = prm.get_file_path()
    continuous_file_name = '100_CH'
    continuous_file_name_end = ''

    recording_path = file_path + continuous_file_name + str(1) + continuous_file_name_end + '.continuous'
    if os.path.isfile(recording_path) is True:
        init_data_file_names(prm, continuous_file_name, continuous_file_name_end)


def process_dir(file_name):
    # Load the raw (1-D) data
    file_utility.set_continuous_data_path(prm)

    custom_raw = Load_OpenEphys_AllTetrodes.load_continuous_64(prm)
    return custom_raw



def plot_raw(dat_raw):
    channel_names = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']
    channel_types = ['emg', 'misc', 'eeg', 'misc', 'misc', 'misc', 'emg', 'misc', 'misc', 'misc', 'misc', 'misc', 'eeg',
                     'misc', 'misc', 'eeg']
    # This creates the info that goes with the channels, which is names, sampling rate, and channel types
    #info = mne.create_info(channel_names, prm.get_sampling_rate(), channel_types)
    info = mne.create_info(channel_names, 250, channel_types)
    # This makes the object that contains all the data and info about the channels. Computations like plotting, averaging, power spectrums can be performed on this object
    custom_raw = mne.io.RawArray(dat_raw, info)

    import matplotlib.pyplot as plt

    plt.switch_backend('TkAgg')  # need this for plotting interactive plot
    plt.ion()  # need this for plotting interactive plot

    colors = dict(mag='darkblue', grad='b', eeg='k', eog='k', ecg='m',
                  emg='g', ref_meg='steelblue', misc='steelblue', stim='b',
                  resp='k', chpi='k')

    custom_raw.plot(None, 60, 0, 16, color=colors, scalings="auto",
                    order=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], show_options="true")
    return


def downsample_dat(trace, down):
    downsampled = scipy.signal.resample(trace, int(np.shape(trace)[0] / down))
    return downsampled


def downsample_all_traces(eeg_data):
    data = pd.DataFrame(eeg_data)
    print("downsampling data...")

    for channel in range((prm.get_number_of_channels())):
        print('processing channel ' + str(channel))
        trace = data.iloc[channel, :]

        # downsample 1 kHz sampling to 250 Hz i.e. divide by 4
        downsampled_trace = downsample_dat(trace, 4)

        if channel == 0:
            downsampled_eeg_data = downsampled_trace
        else:
            downsampled_eeg_data = np.vstack((downsampled_eeg_data, downsampled_trace))

    return downsampled_eeg_data


def split_recording(downsampled_eeg_data):
    plot_raw(downsampled_eeg_data[:16,10000:30000])

    downsampled_eeg_data = pd.DataFrame(downsampled_eeg_data)

    first_headstage = downsampled_eeg_data.iloc[:16,:]
    second_headstage = downsampled_eeg_data.iloc[16:32, :]
    third_headstage = downsampled_eeg_data.iloc[32:48, :]
    fourth_headstage = downsampled_eeg_data.iloc[48:, :]

    #plot_raw(first_headstage)

    first_headstage = first_headstage.values.flatten()
    second_headstage = second_headstage.values.flatten()
    third_headstage = third_headstage.values.flatten()
    fourth_headstage = fourth_headstage.values.flatten()

    return first_headstage, second_headstage, third_headstage, fourth_headstage


def save_dat_files(first_headstage, second_headstage, third_headstage, fourth_headstage):
    print('saving files...')
    #first_headstage = pd.DataFrame(first_headstage)
    first_headstage.astype('int16').tofile('/Users/sarahtennant/Work_Alfredo/Analysis/OpenEphys/2024-05-02_10-25-03/2876_downsampled.dat')
    #first_headstage.to_csv('/Users/sarahtennant/Work_Alfredo/Analysis/OpenEphys/2024-05-02_10-25-03/headstage1_downsampled.dat')

    second_headstage.astype('int16').tofile('/Users/sarahtennant/Work_Alfredo/Analysis/OpenEphys/2024-05-02_10-25-03/2874_downsampled.dat')
    #second_headstage = pd.DataFrame(second_headstage)
    #second_headstage.to_csv('/Users/sarahtennant/Work_Alfredo/Analysis/OpenEphys/2024-05-02_10-25-03/headstage2_downsampled.dat')

    third_headstage.astype('int16').tofile('/Users/sarahtennant/Work_Alfredo/Analysis/OpenEphys/2024-05-02_10-25-03/empty_downsampled.dat')
    #third_headstage = pd.DataFrame(third_headstage)
    #third_headstage.to_csv('/Users/sarahtennant/Work_Alfredo/Analysis/OpenEphys/2024-05-02_10-25-03/headstage3_downsampled.dat')

    fourth_headstage.astype('int16').tofile('/Users/sarahtennant/Work_Alfredo/Analysis/OpenEphys/2024-05-02_10-25-03/2877_downsampled.dat')
    #fourth_headstage = pd.DataFrame(fourth_headstage)
    #fourth_headstage.to_csv('/Users/sarahtennant/Work_Alfredo/Analysis/OpenEphys/2024-05-02_10-25-03/headstage4_downsampled.dat')



def load_dat(file_name1, file_name2):

    # Load the raw (1-D) data
    #input_df = pd.read_table(file_name2)
    input_df1 = np.fromfile(file_name1, dtype=prm.get_sample_datatype())
    input_df2 = np.fromfile(file_name2, dtype=prm.get_sample_datatype())
    #with open(file_name, 'r') as file:
    #    input_df = file.read()

    return input_df2



def main():
    print('-------------------------------------------------------------')
    print('-------------------------------------------------------------')

    #path to the recording .dat file
    file_name = '/Users/sarahtennant/Work_Alfredo/Analysis/OpenEphys/2024-05-02_10-25-03/'

    # set parameters
    parameters(file_name)

    # LOAD DATA
    eeg_data = process_dir(file_name) # overall data

    # PLOT DATA
    #plot_raw(eeg_data[:16,:])

    # DOWNSAMPLE DATA
    downsampled_eeg_data = downsample_all_traces(eeg_data)

    # split by four headstages
    first_headstage, second_headstage, third_headstage, fourth_headstage = split_recording(downsampled_eeg_data)

    # SAVE DATA AS .DAT
    save_dat_files(first_headstage, second_headstage, third_headstage, fourth_headstage)

    dat_filename1 = '/Users/sarahtennant/Work_Alfredo/Analysis/SYNGAPE8/DATA/SYNGAPE8/SYNGAPE8_2777/TAINI_1044_2777_EM40-2024_04_03-0000.dat'
    dat_filename2 = '/Users/sarahtennant/Work_Alfredo/Analysis/OpenEphys/2024-05-02_10-25-03/2877_downsampled.dat'
    #check the .dat file
    load_dat(dat_filename1, dat_filename2)


if __name__ == '__main__':
    main()

