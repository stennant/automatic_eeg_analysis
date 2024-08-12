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
from sklearn import preprocessing

prm = parameters.Parameters()


# set global parameters
def parameters(recording_folder):
    prm.set_file_path(recording_folder)
    prm.set_local_recording_folder_path(recording_folder)
    prm.set_output_path(recording_folder)
    prm.set_sampling_rate(2000)
    prm.set_number_of_channels(16)
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



def plot_raw(dat_raw, sampling_rate):
    channel_names = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']
    channel_types = ['emg', 'misc', 'misc', 'misc', 'misc', 'eeg', 'eeg', 'misc', 'misc', 'misc', 'misc', 'misc', 'misc',
                     'misc', 'misc', 'misc']
    # This creates the info that goes with the channels, which is names, sampling rate, and channel types
    info = mne.create_info(channel_names, sampling_rate, channel_types)
    # This makes the object that contains all the data and info about the channels. Computations like plotting, averaging, power spectrums can be performed on this object
    custom_raw = mne.io.RawArray(dat_raw, info)

    plt.switch_backend('TkAgg')  # need this for plotting interactive plot
    plt.ion()  # need this for plotting interactive plot

    custom_raw.plot(None, 1, 0,
                    order=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], show_options="true", block=True)
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
        downsampled_trace = downsample_dat(trace, 8)

        if channel == 0:
            downsampled_eeg_data = downsampled_trace
        else:
            downsampled_eeg_data = np.vstack((downsampled_eeg_data, downsampled_trace))

    return downsampled_eeg_data


def split_recording(downsampled_eeg_data):

    downsampled_eeg_data = pd.DataFrame(downsampled_eeg_data)

    first_headstage = downsampled_eeg_data.iloc[:16,:]
    second_headstage = downsampled_eeg_data.iloc[16:32, :]
    third_headstage = downsampled_eeg_data.iloc[32:48, :]
    fourth_headstage = downsampled_eeg_data.iloc[48:, :]

    #plot_raw(first_headstage)

    first_headstage = first_headstage.values.flatten("F")
    second_headstage = second_headstage.values.flatten("F")
    third_headstage = third_headstage.values.flatten("F")
    fourth_headstage = fourth_headstage.values.flatten("F")

    return first_headstage, second_headstage, third_headstage, fourth_headstage


def save_dat_files(first_headstage, second_headstage, third_headstage, fourth_headstage):
    print('saving files...')
    first_headstage.astype('int16').tofile('/Users/sarahtennant/Work_Alfredo/Analysis/OpenEphys/2024-05-02_10-25-03/2876_downsampled.dat')
    second_headstage.astype('int16').tofile('/Users/sarahtennant/Work_Alfredo/Analysis/OpenEphys/2024-05-02_10-25-03/2874_downsampled.dat')
    third_headstage.astype('int16').tofile('/Users/sarahtennant/Work_Alfredo/Analysis/OpenEphys/2024-05-02_10-25-03/empty_downsampled.dat')
    fourth_headstage.astype('int16').tofile('/Users/sarahtennant/Work_Alfredo/Analysis/OpenEphys/2024-05-02_10-25-03/2877_downsampled.dat')



def load_dat(file_name2):

    # Load the raw (1-D) data
    input_df = np.fromfile(file_name2, dtype=prm.get_sample_datatype())
    shape = np.shape(input_df)[0]/16
    output_df = np.reshape(input_df, (16,int(shape)))

    return output_df


def downsample_sarahg():
    file_path = '/Users/sarahtennant/Work_Alfredo/Analysis/OpenEphys/15W/1755485/continuous.dat' # for GNU mice

    input_df2 = np.fromfile(file_path, dtype=prm.get_sample_datatype())
    #shape = np.shape(input_df2)[0]/32
    #input_df = np.reshape(input_df2, (32,int(shape)))
    step = prm.get_number_of_channels() * prm.get_display_decimation()
    dat_chans = [input_df2[c::step] for c in range(prm.get_number_of_channels())]

    # Build the time array
    data=np.array(dat_chans)

    downsampled_eeg_data = downsample_all_traces(data)

    downsampled_eeg_data = pd.DataFrame(downsampled_eeg_data)

    #first_headstage = downsampled_eeg_data.iloc[:16,:]
    #second_headstage = downsampled_eeg_data.iloc[16:32, :]

    #first_headstage = first_headstage.values.flatten("F")
    downsampled_eeg_data = downsampled_eeg_data.values.flatten("F")

    downsampled_eeg_data.astype('int16').tofile('/Users/sarahtennant/Work_Alfredo/Analysis/OpenEphys/15W/1755485/1755485_downsampled.dat')
    #second_headstage.astype('int16').tofile('/Volumes/Sarah/SYNGAPE8/DATA/SYNGAPE8/12W/SYNGAPE8_1755486/1755486_downsampled.dat')



def process_dir2(file_name):
    # Load the raw (1-D) data
    dat_raw = np.fromfile(file_name, dtype=prm.get_sample_datatype())
    # Reshape the (2-D) per channel data
    step = prm.get_number_of_channels() * prm.get_display_decimation()

    dat_chans = [dat_raw[c::step] for c in range(prm.get_number_of_channels())]

    # Build the time array
    data=np.array(dat_chans)

    del(dat_chans)
    channel_names=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']
    channel_types=['misc','misc','misc','misc','misc','misc','misc','misc','misc','misc','misc','misc','misc','misc','misc','misc']

    # This creates the info that goes with the channels, which is names, sampling rate, and channel types
    info = mne.create_info(channel_names, prm.get_sampling_rate(), channel_types)
    # This makes the object that contains all the data and info about the channels. Computations like plotting, averaging, power spectrums can be performed on this object
    custom_raw = mne.io.RawArray(data, info)

    return custom_raw


def plot_raw2(eeg_data):

    mne.viz.set_browser_backend('matplotlib', verbose=None)
    colors=dict(mag='darkblue', grad='b', eeg='k', eog='k', ecg='m', emg='g', ref_meg='steelblue', misc='steelblue', stim='b', resp='k', chpi='k')
    plt.switch_backend('TkAgg') # need this for plotting interactive plot
    plt.ion() # need this for plotting interactive plot
    fig = eeg_data.crop(5000,5100).plot(None, 60, 0, 16,color = colors, scalings = "auto", order=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], show_options = "true" )
    print("done")


def main():
    print('-------------------------------------------------------------')
    print('-------------------------------------------------------------')

    #path to the recording .dat file
    file_name = '/Users/sarahtennant/Work_Alfredo/Analysis/OpenEphys/13W/1755485/1755485_continuous.dat'

    # set parameters
    parameters(file_name)

    downsample_sarahg()

    # LOAD DATA
    #eeg_data = process_dir(file_name) # overall data

    # PLOT DATA
    #plot_raw(eeg_data[:16,5000000:5010000], 1000)

    # DOWNSAMPLE DATA
    #downsampled_eeg_data = downsample_all_traces(eeg_data)

    # split by four headstages
    #first_headstage, second_headstage, third_headstage, fourth_headstage = split_recording(downsampled_eeg_data)

    # SAVE DATA AS .DAT
    #save_dat_files(first_headstage, second_headstage, third_headstage, fourth_headstage)

    #dat_filename2 = '/Users/sarahtennant/Work_Alfredo/Analysis/OpenEphys/2024-05-02_10-25-03/2876_downsampled.dat'
    #check the .dat file
    #dat = load_dat(dat_filename2)
    #plot_raw(dat[:,1250000:1260000], 250)

    #dat2 = process_dir2(dat_filename2)
    #plot_raw2(dat2)

if __name__ == '__main__':
    main()

