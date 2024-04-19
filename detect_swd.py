import cepstrum_analysis
import parameters
import sys
import os.path
import numpy as np
from numpy import *
import os
import mne
import pandas as pd
from scipy import stats
import matplotlib.pylab as plt
import cepstrum_plots


def filter_data(cropped_raw, all_channels):
    print('Applying highpass filter to data....')
    filtered_data = cropped_raw.filter(l_freq=0.2, h_freq=120, picks = all_channels) # filter the data between 0.2 to 120 Hz
    return filtered_data

def remove_dc_component(filtered_data, main_eeg):
    data = filtered_data.to_data_frame()
    main_eeg_channel = data[[str(main_eeg)]]
    time = data[["time"]]
    mean_of_channel = np.mean(main_eeg_channel)
    main_eeg_channel = main_eeg_channel - mean_of_channel
    #data_with_time = pd.DataFrame({"time" : time, "data" : main_eeg_channel}, index=[i for i in range(main_eeg_channel.shape[0])])
    data_with_time = pd.DataFrame(np.hstack((time, main_eeg_channel)), columns = ["time", "main_eeg_channel"])
    return data_with_time


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



def flatten_cepstrum_score(cepstrum_score):
    flattened_cepstrum_score = np.zeros(cepstrum_score.shape[0])
    for rowcount, row in enumerate(cepstrum_score):
        sum = np.sum(cepstrum_score[rowcount, :])
        if sum > 2:
            flattened_cepstrum_score[rowcount] = 1
    return flattened_cepstrum_score


def find_seizure_times(cepstrum_score, data, total_duration):
    flattened_cepstrum_score = flatten_cepstrum_score(cepstrum_score)

    data_with_cepstral_score = np.vstack((flattened_cepstrum_score, data.iloc[:total_duration, 0], data.iloc[:total_duration, 1]))
    data_with_cepstral_score = np.transpose(data_with_cepstral_score)

    data = pd.DataFrame({'marker': data_with_cepstral_score[:, 0],
                         'time': data_with_cepstral_score[:, 1],
                         'amplitude': data_with_cepstral_score[:, 2]})

    data["diff"] = data.iloc[:,0].diff()

    start_time_indexes = np.where(data["diff"] == 1)[0]
    end_time_indexes = np.where(data["diff"] == -1)[0]

    seizure_start_times = np.asarray(data['time'].iloc[start_time_indexes])
    seizure_end_times = np.asarray(data['time'].iloc[end_time_indexes])

    return seizure_start_times, seizure_end_times


def remove_false_positives(seizure_start_times, seizure_end_times ):
    new_seizure_start_times = []
    new_seizure_end_times = []
    for rowcount, row in enumerate(seizure_start_times):
        duration = seizure_end_times[rowcount] - seizure_start_times[rowcount]
        if duration >= 1:
            new_seizure_start_times = np.append(new_seizure_start_times, seizure_start_times[rowcount])
            new_seizure_end_times = np.append(new_seizure_end_times, seizure_end_times[rowcount])
        rowcount +=1
    return new_seizure_start_times, new_seizure_end_times


def collapse_seizures_within_one_second(seizure_start_times, seizure_end_times):
    new_seizure_start_times = []
    new_seizure_end_times = []
    for rowcount, row in enumerate(seizure_start_times-1):
        duration = seizure_end_times[rowcount] - seizure_start_times[rowcount+1]
        if duration < 1:
            new_seizure_start_times = np.append(new_seizure_start_times, seizure_start_times[rowcount])
            new_seizure_end_times = np.append(new_seizure_end_times, seizure_end_times[rowcount+1])
            rowcount +=2
        elif duration > 1:
            new_seizure_start_times = np.append(new_seizure_start_times, seizure_start_times[rowcount])
            new_seizure_end_times = np.append(new_seizure_end_times, seizure_end_times[rowcount])
            rowcount+=1
    return new_seizure_start_times, new_seizure_end_times

def calculate_seizure_duration(seizure_start_times, seizure_end_times):
    seizure_durations = []
    for rowcount, row in enumerate(seizure_start_times):
        duration = (seizure_end_times[rowcount] - seizure_start_times[rowcount+1])/250.4
        seizure_durations = np.append(seizure_durations, duration)
    return seizure_durations


def run_swd_detection(cropped_raw, all_channels, main_eeg, output_data_path, output_figure_path):

    filtered_data = filter_data(cropped_raw, all_channels)

    data_with_time = remove_dc_component(filtered_data, main_eeg)

    data_with_time = fill_outliers(data_with_time)

    cepstrum_score, data, total_duration = cepstrum_analysis.control_cepstrum_anaylsis(data_with_time)

    seizure_start_times, seizure_end_times = find_seizure_times(cepstrum_score, data, total_duration)

    cepstrum_plots.plot_data_with_seizures_marked(data, seizure_start_times, seizure_end_times) # if you want to plot the whole continuous data

    new_seizure_start_times, new_seizure_end_times = remove_false_positives(seizure_start_times, seizure_end_times)

    cepstrum_plots.plot_data_with_seizures_marked_without_false_positives(data, seizure_start_times, seizure_end_times) # if you want to plot the whole continuous data

    seizure_start_times, seizure_end_times = collapse_seizures_within_one_second(new_seizure_start_times, new_seizure_end_times)

    cepstrum_plots.plot_data_with_seizures_marked_without_false_positives(data, seizure_start_times, seizure_end_times) # if you want to plot the whole continuous data

    return



#  this is here for testing
def main():
    print('-------------------------------------------------------------')
    print('-------------------------------------------------------------')

    params = parameters.Parameters()

    run_swd_detection()



if __name__ == '__main__':
    main()
