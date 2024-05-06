'''
Functions for converting open ephys data to mountainsort's mda format

'''

import glob
import os
import numpy as np

import open_ephys_IO

import file_utility


def try_to_figure_out_non_default_file_names(folder_path, ch_num):
    beginning = glob.glob(folder_path + '*.continuous')[0].split('/')[-1].split('_')[0]
    end = glob.glob(folder_path + '*.continuous')[0].split('/')[-1].split('CH')[-1].split('.')[0].split('_')[1:]
    if len(end) == 2:
        file_path = folder_path + beginning + '_CH' + str(ch_num) + '_' + end[0] + '_' + end[1] + '.continuous'
    else:
        file_path = folder_path + beginning + '_CH' + str(ch_num) + '_' + end[0] + '.continuous'
    return file_path


# this is for putting all tetrodes together
def load_continuous(prm):
    folder_path = prm.get_file_path()
    continuous_file_name = prm.get_continuous_file_name()
    continuous_file_name_end = prm.get_continuous_file_name_end()

    file_path = folder_path + continuous_file_name + str(1) + continuous_file_name_end + '.continuous'
    if os.path.exists(file_path):
        first_ch = open_ephys_IO.get_data_continuous(prm, file_path)
    else:
        file_path = try_to_figure_out_non_default_file_names(folder_path, 1)
        first_ch = open_ephys_IO.get_data_continuous(prm, file_path)

    live_channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    number_of_live_channels = len(live_channels)

    recording_length = len(first_ch)
    channels_all = np.zeros((number_of_live_channels, recording_length))

    live_ch_counter = 0
    for channel in range(16):
        if (channel + 1) in live_channels:
            file_path = folder_path + continuous_file_name + str(channel + 1) + continuous_file_name_end + '.continuous'
            if os.path.exists(file_path):
                channel_data = open_ephys_IO.get_data_continuous(prm, file_path)
            else:
                file_path = try_to_figure_out_non_default_file_names(folder_path, channel + 1)
                channel_data = open_ephys_IO.get_data_continuous(prm, file_path)

            channels_all[live_ch_counter, :] = channel_data
            live_ch_counter += 1
    return channels_all







# this is for putting all tetrodes together
def load_continuous_2(prm):
    folder_path = prm.get_file_path()
    continuous_file_name = prm.get_continuous_file_name()
    continuous_file_name_end = prm.get_continuous_file_name_end()

    file_path = folder_path + continuous_file_name + str(1) + continuous_file_name_end + '.continuous'
    if os.path.exists(file_path):
        first_ch = open_ephys_IO.get_data_continuous(prm, file_path)
    else:
        file_path = try_to_figure_out_non_default_file_names(folder_path, 1)
        first_ch = open_ephys_IO.get_data_continuous(prm, file_path)

    live_channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    number_of_live_channels = len(live_channels)

    recording_length = len(first_ch)
    channels_all = np.zeros((number_of_live_channels, recording_length))

    live_ch_counter = 0
    for channel in range(16):
        if (channel + 1) in live_channels:
            file_path = folder_path + continuous_file_name + str(channel + 1) + continuous_file_name_end + '.continuous'
            if os.path.exists(file_path):
                channel_data = open_ephys_IO.get_data_continuous(prm, file_path)
            else:
                file_path = try_to_figure_out_non_default_file_names(folder_path, channel + 1)
                channel_data = open_ephys_IO.get_data_continuous(prm, file_path)

            channels_all[live_ch_counter, :] = channel_data
            live_ch_counter += 1
    return channels_all




