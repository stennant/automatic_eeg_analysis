import parameters
import sys
import os.path
import numpy as np
from numpy import *
import os
import mne
import pandas as pd
from scipy import stats


prm = parameters.Parameters()


def filter_data(cropped_raw, all_channels):
    print('Applying highpass filter to data....')
    filtered_data = cropped_raw.filter(l_freq=0.2, h_freq=120, picks = all_channels) # filter the data between 0.2 to 120 Hz
    return filtered_data


def fill_outliers(data):
    print('Removing outliers from data....')
    #plt.plot(data.iloc[:, 0], data.iloc[:, 1])
    #plt.show()
    data['zscore'] = np.abs(stats.zscore(data['main_eeg_channel']))
    data.loc[data.zscore > 4.5, 'main_eeg_channel'] = np.nan
    data['main_eeg_channel'].interpolate(method='linear', inplace=True)
    data.drop(['zscore'], axis=1, inplace=True)
    #plt.plot(data.iloc[:, 0], data.iloc[:, 1])
    #plt.show()
    return data


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
    data_with_time = pd.DataFrame(np.hstack((time, main_eeg_channel)), columns = ["time", "main_eeg_channel"])
    return data_with_time

def save_main_eeg_channel_as_csv(data_with_time, animal_id, main_eeg, output_data_path):
    print('Saving channel ' + str(main_eeg) + ' to csv file....')
    data_with_time.to_csv(output_data_path + '/' + str(animal_id) + '_channnels_test_nonseiz3.csv', index=False)
    plot_check_data(data_with_time)
    return data_with_time


def run_sleep_analysis(cropped_raw, animal_id, all_channels, main_eeg, output_data_path, output_figure_path):

    filtered_data = filter_data(cropped_raw, all_channels)

    data_with_time = remove_dc_component(filtered_data, main_eeg)

    data_with_time = fill_outliers(data_with_time)

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
