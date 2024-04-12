import parameters
import sys
import os.path
import numpy as np
from numpy import *
import os
import mne
import pandas as pd


prm = parameters.Parameters()


def filter_data(cropped_raw, all_channels):
    print('Applying highpass filter to data....')
    filtered_data = cropped_raw.filter(l_freq=0.2, h_freq=120, picks = all_channels) # filter the data between 0.2 to 120 Hz
    return filtered_data


def fill_outliers(filtered_data):
    print('Removing outliers from data....')
    data = filtered_data.to_data_frame()
    return filtered_data

def plot_check_data(data):
    import matplotlib.pylab as plt
    plt.plot(data[["time"]], data[["main_eeg_channel"]])
    #plt.ylim(2300, 3000)
    plt.show()

def remove_dc_component(filtered_data, main_eeg):
    data = filtered_data.to_data_frame()
    main_eeg_channel = data[[str(main_eeg)]]
    time = data[["time"]]
    mean_of_channel = np.mean(main_eeg_channel)
    main_eeg_channel = main_eeg_channel - mean_of_channel
    #data_with_time = pd.DataFrame({"time" : time, "data" : main_eeg_channel}, index=[i for i in range(main_eeg_channel.shape[0])])
    data_with_time = pd.DataFrame(np.hstack((time, main_eeg_channel)), columns = ["time", "main_eeg_channel"])
    return data_with_time

def save_main_eeg_channel_as_csv(data_with_time, animal_id, main_eeg, output_data_path):
    print('Saving channel ' + str(main_eeg) + ' to csv file....')
    #data = filtered_data.to_data_frame()
    #main_eeg_channel = data[["time", str(main_eeg)]]
    data_with_time.to_csv(output_data_path + '/' + str(animal_id) + '_channnels_test_nonseiz3.csv', index=False)
    plot_check_data(data_with_time)
    return data_with_time


def run_sleep_analysis(cropped_raw, animal_id, all_channels, main_eeg, output_data_path, output_figure_path):

    filtered_data = filter_data(cropped_raw, all_channels)

    data_with_time = remove_dc_component(filtered_data, main_eeg)

    main_eeg_channel = save_main_eeg_channel_as_csv(data_with_time, animal_id, main_eeg, output_data_path)

    return



#  this is here for testing
def main():
    print('-------------------------------------------------------------')
    print('-------------------------------------------------------------')

    params = parameters.Parameters()

    run_sleep_analysis()



if __name__ == '__main__':
    main()
