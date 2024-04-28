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
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar

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

def make_folder_structure(output_figure_path, output_data_path):
    # if the output path does not exist, make it
    if os.path.exists(output_figure_path) is False:
        os.makedirs(output_figure_path)
    if os.path.exists(output_data_path) is False:
        os.makedirs(output_data_path)
    return

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


def plot_interactive(custom_raw):
    import matplotlib.pyplot as plt
    plt.switch_backend('TkAgg') # need this for plotting interactive plot
    plt.ion() # need this for plotting interactive plot

    colors = dict(mag='darkblue', grad='b', eeg='k', eog='k', ecg='m',
                  emg='g', ref_meg='steelblue', misc='steelblue', stim='b',
                  resp='k', chpi='k')

    custom_raw.plot(None, 60, 0, 16, color = colors, scalings = "auto", order=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], show_options = "true" )


def crop_by_start_and_end(custom_raw):
    print('Cropping recording based on start and end times....')
    #plot_interactive(custom_raw)

    #custom_raw = custom_raw.crop(prm.get_start_sample(), prm.get_end_sample()) # take full 24 hour recording
    cropped_raw = custom_raw.crop(52790, 52808) # testing dataset - 52800, 52805 for seizure, 52910, 52915 for non seizure, 52782, 52812 for both
    return cropped_raw


def plot_example(custom_raw, output_figure_path ):
    eeg_data = custom_raw.to_data_frame()

    eeg_channel5 = eeg_data.iloc[:,5]
    mean_of_channel = np.mean(eeg_channel5)
    main_eeg_channel = eeg_channel5 - mean_of_channel

    eeg = plt.figure(figsize=(16, 12))
    ax = eeg.add_subplot(4, 1, 1)  # specify (nrows, ncols, axnum
    ax.plot(main_eeg_channel, color='Black', markersize=2.5)
    plt.ylabel('uV', fontsize=18, labelpad=0)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tick_params(
        axis='x',  # changes apply to the x-axis
        which='both',  # both major and minor ticks are affected
        bottom=False,  # ticks along the bottom edge are off
        labelbottom=False)  # labels along the bottom edge are off

    eeg_channel8 = eeg_data.iloc[:,8]
    mean_of_channel = np.mean(eeg_channel8)
    main_eeg_channel = eeg_channel8 - mean_of_channel

    ax = eeg.add_subplot(4, 1, 2)  # specify (nrows, ncols, axnum
    ax.plot(main_eeg_channel, color='Black', markersize=2.5)
    plt.ylabel('uV', fontsize=18, labelpad=0)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tick_params(
        axis='x',  # changes apply to the x-axis
        which='both',  # both major and minor ticks are affected
        bottom=False,  # ticks along the bottom edge are off
        labelbottom=False)  # labels along the bottom edge are off

    eeg_channel5 = eeg_data.iloc[:,5]
    mean_of_channel = np.mean(eeg_channel5)
    main_eeg_channel = eeg_channel5 - mean_of_channel

    ax = eeg.add_subplot(4, 1, 3)  # specify (nrows, ncols, axnum
    ax.plot(main_eeg_channel, color='Black', markersize=2.5)
    plt.ylabel('uV', fontsize=18, labelpad=0)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tick_params(
        axis='x',  # changes apply to the x-axis
        which='both',  # both major and minor ticks are affected
        bottom=False,  # ticks along the bottom edge are off
        labelbottom=False)  # labels along the bottom edge are off

    eeg_channel8 = eeg_data.iloc[:,8]
    mean_of_channel = np.mean(eeg_channel8)
    main_eeg_channel = eeg_channel8 - mean_of_channel

    ax = eeg.add_subplot(4, 1, 4)  # specify (nrows, ncols, axnum
    ax.plot(main_eeg_channel, color='Black', markersize=2.5)
    plt.ylabel('uV', fontsize=18, labelpad=0)
    plt.xlabel('Time (seconds)', fontsize=18, labelpad=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    #plt.tight_layout(pad=0.4, w_pad=1, h_pad=1.0)
    plt.subplots_adjust(hspace=.35, wspace=.35, bottom=0.25, left=0.1, right=0.9, top=0.9)
    #plt.locator_params(axis='y', nbins=4)
    #plt.locator_params(axis='x', nbins=3)
    #plt.xlim(0, 200)
    #plt.ylim(0)
    plt.savefig(output_figure_path + '/' + 'exampletrace.png', dpi=200)
    plt.close()




def main():
    print('-------------------------------------------------------------')
    print('-------------------------------------------------------------')

    #path to the recording .dat file

    recording_folder = '/Users/sarahtennant/Work_Alfredo/Analysis/SYNGAPE8/DATA/SYNGAPE8/SYNGAPE8_176923/TAINI_1044_176923-EM3-2024_03_27-0000.dat'  # for syngape8 rats
    configuration_path = '/Users/sarahtennant/Work_Alfredo/Analysis/SYNGAPE8/DATA/SYNGAPE8/SYNGAPE8_176923/TAINI_1044_176923-EM3-2024_03_27-0000_configuration.yaml'  # for syngape8 rats
    output_figure_path = '/Users/sarahtennant/Work_Alfredo/Analysis/SYNGAPE8/Figures'
    output_data_path = '/Users/sarahtennant/Work_Alfredo/Analysis/SYNGAPE8/Data_output'

    # if the output path does not exist, make it
    make_folder_structure(output_figure_path, output_data_path)

    parameters(recording_folder)

    # set start and end time by extracting from the configuration file
    #read_yaml_config.calculate_recording_duration(file_path + configuration_path)

    # LOAD DATA
    eeg_data = process_dir(recording_folder) # overall data

    cropped_eeg = crop_by_start_and_end(eeg_data)

    # PLOT DATA
    #plot_interactive(cropped_eeg)

    plot_example(cropped_eeg, output_figure_path)



if __name__ == '__main__':
    main()

