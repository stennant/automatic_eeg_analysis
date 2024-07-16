'''
Functions for converting open ephys data to mountainsort's mda format

'''

import glob
import os
import numpy as np

from OpenEphys import open_ephys_IO



# this is for putting all tetrodes together
def load_continuous_64(prm):
    folder_path = prm.get_file_path()
    continuous_file_name = prm.get_continuous_file_name()
    continuous_file_name_end = prm.get_continuous_file_name_end()

    file_path = folder_path + continuous_file_name + str(1) + continuous_file_name_end + '.continuous'
    first_ch = open_ephys_IO.get_data_continuous(prm, file_path)


    live_channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                     17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32,
                     33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48,
                     49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64]

    number_of_live_channels = len(live_channels)

    recording_length = len(first_ch)
    channels_all = np.zeros((number_of_live_channels, recording_length))

    live_ch_counter = 0
    for channel in range(64):
        if (channel + 1) in live_channels:
            file_path = folder_path + continuous_file_name + str(channel + 1) + continuous_file_name_end + '.continuous'
            channel_data = open_ephys_IO.get_data_continuous(prm, file_path)

            channels_all[live_ch_counter, :] = channel_data
            live_ch_counter += 1
    return channels_all



def concatenate_continuous_64(prm):
    channels_all = load_continuous_64(prm)
    channels_all_2 = load_continuous_64_2(prm)

    all_channels = np.vstack((channels_all, channels_all_2))

    return all_channels



# this is for putting all tetrodes together
def load_continuous_64_2(prm):
    folder_path = prm.get_file_path()
    continuous_file_name = prm.get_continuous_file_name()
    continuous_file_name_end = "_2"

    file_path = folder_path + continuous_file_name + str(1) + continuous_file_name_end + '.continuous'
    first_ch = open_ephys_IO.get_data_continuous(prm, file_path)


    live_channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                     17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32,
                     33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48,
                     49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64]

    number_of_live_channels = len(live_channels)

    recording_length = len(first_ch)
    channels_all = np.zeros((number_of_live_channels, recording_length))

    live_ch_counter = 0
    for channel in range(64):
        if (channel + 1) in live_channels:
            file_path = folder_path + continuous_file_name + str(channel + 1) + continuous_file_name_end + '.continuous'
            channel_data = open_ephys_IO.get_data_continuous(prm, file_path)

            channels_all[live_ch_counter, :] = channel_data
            live_ch_counter += 1


    return channels_all





# this is for putting all tetrodes together
def load_continuous_32(prm):
    folder_path = prm.get_file_path()
    continuous_file_name = prm.get_continuous_file_name()
    continuous_file_name_end = prm.get_continuous_file_name_end()

    file_path = folder_path + continuous_file_name + str(1) + continuous_file_name_end + '.continuous'
    first_ch = open_ephys_IO.get_data_continuous(prm, file_path)


    live_channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                     17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]

    number_of_live_channels = len(live_channels)

    recording_length = len(first_ch)
    channels_all = np.zeros((number_of_live_channels, recording_length))

    live_ch_counter = 0
    for channel in range(32):
        if (channel + 1) in live_channels:
            file_path = folder_path + continuous_file_name + str(channel + 1) + continuous_file_name_end + '.continuous'
            channel_data = open_ephys_IO.get_data_continuous(prm, file_path)

            channels_all[live_ch_counter, :] = channel_data
            live_ch_counter += 1
    return channels_all



# this is for putting all tetrodes together
def load_continuous_32_1(prm):
    folder_path = prm.get_file_path()
    continuous_file_name = prm.get_continuous_file_name()
    continuous_file_name_end = "_1"

    file_path = folder_path + continuous_file_name + str(1) + continuous_file_name_end + '.continuous'
    first_ch = open_ephys_IO.get_data_continuous(prm, file_path)


    live_channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                     17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]

    number_of_live_channels = len(live_channels)

    recording_length = len(first_ch)
    channels_all = np.zeros((number_of_live_channels, recording_length))

    live_ch_counter = 0
    for channel in range(32):
        if (channel + 1) in live_channels:
            file_path = folder_path + continuous_file_name + str(channel + 1) + continuous_file_name_end + '.continuous'
            channel_data = open_ephys_IO.get_data_continuous(prm, file_path)

            channels_all[live_ch_counter, :] = channel_data
            live_ch_counter += 1
    return channels_all


def load_continuous_32_2(prm):
    folder_path = prm.get_file_path()
    continuous_file_name = prm.get_continuous_file_name()
    continuous_file_name_end = "_1"

    file_path = folder_path + continuous_file_name + str(1) + continuous_file_name_end + '.continuous'
    first_ch = open_ephys_IO.get_data_continuous(prm, file_path)


    live_channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                     17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]

    number_of_live_channels = len(live_channels)

    recording_length = len(first_ch)
    channels_all = np.zeros((number_of_live_channels, recording_length))

    live_ch_counter = 0
    for channel in range(32):
        if (channel + 1) in live_channels:
            file_path = folder_path + continuous_file_name + str(channel + 1) + continuous_file_name_end + '.continuous'
            channel_data = open_ephys_IO.get_data_continuous(prm, file_path)

            channels_all[live_ch_counter, :] = channel_data
            live_ch_counter += 1
    return channels_all


def load_continuous_32_3(prm):
    folder_path = prm.get_file_path()
    continuous_file_name = prm.get_continuous_file_name()
    continuous_file_name_end = "_1"

    file_path = folder_path + continuous_file_name + str(1) + continuous_file_name_end + '.continuous'
    first_ch = open_ephys_IO.get_data_continuous(prm, file_path)


    live_channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                     17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]

    number_of_live_channels = len(live_channels)

    recording_length = len(first_ch)
    channels_all = np.zeros((number_of_live_channels, recording_length))

    live_ch_counter = 0
    for channel in range(32):
        if (channel + 1) in live_channels:
            file_path = folder_path + continuous_file_name + str(channel + 1) + continuous_file_name_end + '.continuous'
            channel_data = open_ephys_IO.get_data_continuous(prm, file_path)

            channels_all[live_ch_counter, :] = channel_data
            live_ch_counter += 1
    return channels_all


def load_continuous_32_4(prm):
    folder_path = prm.get_file_path()
    continuous_file_name = prm.get_continuous_file_name()
    continuous_file_name_end = "_1"

    file_path = folder_path + continuous_file_name + str(1) + continuous_file_name_end + '.continuous'
    first_ch = open_ephys_IO.get_data_continuous(prm, file_path)


    live_channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                     17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]

    number_of_live_channels = len(live_channels)

    recording_length = len(first_ch)
    channels_all = np.zeros((number_of_live_channels, recording_length))

    live_ch_counter = 0
    for channel in range(32):
        if (channel + 1) in live_channels:
            file_path = folder_path + continuous_file_name + str(channel + 1) + continuous_file_name_end + '.continuous'
            channel_data = open_ephys_IO.get_data_continuous(prm, file_path)

            channels_all[live_ch_counter, :] = channel_data
            live_ch_counter += 1
    return channels_all


def load_continuous_32_5(prm):
    folder_path = prm.get_file_path()
    continuous_file_name = prm.get_continuous_file_name()
    continuous_file_name_end = "_1"

    file_path = folder_path + continuous_file_name + str(1) + continuous_file_name_end + '.continuous'
    first_ch = open_ephys_IO.get_data_continuous(prm, file_path)


    live_channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                     17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]

    number_of_live_channels = len(live_channels)

    recording_length = len(first_ch)
    channels_all = np.zeros((number_of_live_channels, recording_length))

    live_ch_counter = 0
    for channel in range(32):
        if (channel + 1) in live_channels:
            file_path = folder_path + continuous_file_name + str(channel + 1) + continuous_file_name_end + '.continuous'
            channel_data = open_ephys_IO.get_data_continuous(prm, file_path)

            channels_all[live_ch_counter, :] = channel_data
            live_ch_counter += 1
    return channels_all

