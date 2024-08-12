import math

from pylab import *
from mne import io
import pandas as pd
import itertools
import os
import numpy as np


def process_dir(file_path):
    # Load sleep state score from .csv
    data = pd.read_csv(file_path, delimiter=",") # read .csv file with sleep score
    return data

def round_down(num, divisor):
    return num - (num % divisor)

def correct_seizures(data, seizure_times_path):
    # Load seizure correction from .csv
    seizure_times = pd.read_csv(seizure_times_path, delimiter=",") # read .csv file with sleep score
    seizure_number = len(np.array(seizure_times['dur']))

    for rowcount, row in enumerate(range(len(seizure_times))):
        seizure_start_time = seizure_times.at[rowcount, 'sec_start']
        seizure_duration = round_down(seizure_times.at[rowcount, 'dur'], 1)
        epoch_start_number = seizure_start_time/5
        epoch = int(round(epoch_start_number))
        if data.at[epoch, "sleep.score"] != 4:
            data.at[epoch, "sleep.score"] = 4
        if seizure_duration > 5:
            if data.at[epoch+1, "sleep.score"] != 4:
                data.at[epoch+1, "sleep.score"] = 4
        if seizure_duration > 10:
            if data.at[epoch+2, "sleep.score"] != 4:
                data.at[epoch+2, "sleep.score"] = 4
    return data, seizure_number

def calculate_total_states(data):
    df = pd.DataFrame(columns=['hour','total_wake_epochs','total_nrem_epochs','total_rem_epochs','total_swd_epochs'])

    df.at[0, "total_wake_epochs"] = np.count_nonzero(data == 0)
    df.at[0, "total_nrem_epochs"] = np.count_nonzero(data == 1)
    df.at[0, "total_rem_epochs"] = np.count_nonzero(data == 2)
    df.at[0, "total_swd_epochs"] = np.count_nonzero(data == 4)
    return df

def plot_total_states(df, output_path):
    wake = np.nanmean(np.array(df.loc[:, "total_wake_epochs"]))
    nrem = np.nanmean(np.array(df.loc[:, "total_nrem_epochs"]))
    rem = np.nanmean(np.array(df.loc[:, "total_rem_epochs"]))
    swd = np.nanmean(np.array(df.loc[:, "total_swd_epochs"]))

    print("total number of seizure epochs is " + str(swd))

    color = ['LightSkyBlue', 'DodgerBlue', 'Blue', 'MidnightBlue']
    total_epochs = [wake, nrem, rem, swd]
    bins = np.arange(4)

    percent_histogram = plt.figure(figsize=(6, 4))
    ax = percent_histogram.add_subplot(1, 1, 1)  # specify (nrows, ncols, axnum)
    ax.bar(bins, total_epochs, color= color)
    plt.ylabel('Total number of epochs', fontsize=12, labelpad=10)
    plt.xlabel('Sleep state', fontsize=12, labelpad=10)
    plt.locator_params(axis='x', nbins=5)
    ax.set_xticklabels(['', 'Wake', 'nrem', 'rem', 'swd'])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    plt.subplots_adjust(hspace=.35, wspace=.35, bottom=0.2, left=0.22, right=0.87, top=0.92)
    plt.savefig(output_path + '/total_epochs_per_state' + '.png', dpi=200)



# Calculates the number of epochs spent in each sleep state for each hour of the 24 hour recording
def calculate_states_per_hour(data):

    epochs_array = np.arange(0,17281, 720)
    df = pd.DataFrame(columns=['hour','total_wake_epochs','total_nrem_epochs','total_rem_epochs','total_swd_epochs'])
    df["hour"] = pd.Series(np.arange(24))

    for rowcount, row in enumerate(range(24)):
            epoch_start = epochs_array[rowcount]
            epoch_end = epochs_array[rowcount+1]
            hourly_epochs = data[epoch_start:epoch_end]
            df.at[rowcount,"total_wake_epochs"] = np.count_nonzero(hourly_epochs == 0)
            df.at[rowcount,"total_nrem_epochs"] = np.count_nonzero(hourly_epochs == 1)
            df.at[rowcount,"total_rem_epochs"] = np.count_nonzero(hourly_epochs == 2)
            df.at[rowcount,"total_swd_epochs"] = np.count_nonzero(hourly_epochs == 4)
    return df


# Calculates the percentage of time spent in each sleep state for each hour of the 24 hour recording
def calculate_percent_states_per_hour(df):

    for rowcount, row in enumerate(range(24)):
        total = np.sum(df.iloc[rowcount,:])
        df.at[rowcount, "percent wake"] = df.at[rowcount, "total_wake_epochs"] / total *100
        df.at[rowcount, "percent nrem"] = df.at[rowcount, "total_nrem_epochs"] / total *100
        df.at[rowcount, "percent rem"] = df.at[rowcount, "total_rem_epochs"] / total *100
        df.at[rowcount, "percent swd"] = df.at[rowcount, "total_swd_epochs"] / total *100
    return df

# Plot
def plot_states_per_hour(df,output_path):
    print('plotting histogram of sleep states per hour...')

    wake = np.array(df.loc[:, "total_wake_epochs"])
    nrem = np.array(df.loc[:, "total_nrem_epochs"])
    rem = np.array(df.loc[:, "total_rem_epochs"])
    swd = np.array(df.loc[:, "total_swd_epochs"])
    bins = np.arange(24)

    epochs_histogram = plt.figure(figsize=(6, 4))
    ax = epochs_histogram.add_subplot(1, 1, 1)  # specify (nrows, ncols, axnum)
    ax.bar(bins, swd, color = "MidnightBlue")
    ax.bar(bins, rem, bottom = swd, color = "Blue")
    ax.bar(bins, nrem, bottom = swd + rem, color = "DodgerBlue")
    ax.bar(bins, wake, bottom = swd + rem + nrem, color = "LightSkyBlue")
    plt.ylabel('Total number of epochs', fontsize=12, labelpad=10)
    plt.xlabel('Hour', fontsize=12, labelpad=10)
    plt.legend(["swd", "rem", "nrem", "wake"])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    plt.subplots_adjust(hspace=.35, wspace=.35, bottom=0.2, left=0.12, right=0.87, top=0.92)
    plt.savefig(output_path + '/epochs_per_hour' + '.png', dpi=200)
    plt.close()

    wake = np.array(df.loc[:, "percent wake"])
    nrem = np.array(df.loc[:, "percent nrem"])
    rem = np.array(df.loc[:, "percent rem"])
    swd = np.array(df.loc[:, "percent swd"])

    percent_histogram = plt.figure(figsize=(6, 4))
    ax = percent_histogram.add_subplot(1, 1, 1)  # specify (nrows, ncols, axnum)
    ax.bar(bins, swd, color = "MidnightBlue")
    ax.bar(bins, rem, bottom = swd, color = "Blue")
    ax.bar(bins, nrem, bottom = swd + rem, color = "DodgerBlue")
    ax.bar(bins, wake, bottom = swd + rem + nrem, color = "LightSkyBlue")
    plt.ylabel('Percentage', fontsize=12, labelpad=10)
    plt.xlabel('Hour', fontsize=12, labelpad=10)
    plt.legend(["swd", "rem", "nrem", "wake"])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    plt.subplots_adjust(hspace=.35, wspace=.35, bottom=0.2, left=0.12, right=0.87, top=0.92)
    plt.savefig(output_path + '/percent_per_hour' + '.png', dpi=200)
    plt.close()


def calculate_total_bouts(data):
    data = np.array(data)
    df = pd.DataFrame(columns=['wake_bouts','nrem_bouts','rem_bouts'])

    for rowcount, row in enumerate(range(len(data))):
        current_state = data[rowcount][0]
        if current_state == 0:
            df.at[rowcount,"rem_bouts"] = 0
            df.at[rowcount,"nrem_bouts"] = 0
            df.at[rowcount,"wake_bouts"] = 1
        elif current_state == 1:
            df.at[rowcount,"rem_bouts"] = 0
            df.at[rowcount,"nrem_bouts"] = 1
            df.at[rowcount,"wake_bouts"] = 0
        elif current_state == 2:
            df.at[rowcount,"rem_bouts"] = 1
            df.at[rowcount,"nrem_bouts"] = 0
            df.at[rowcount,"wake_bouts"] = 0
        elif current_state == 4:
            df.at[rowcount,"rem_bouts"] = 0
            df.at[rowcount,"nrem_bouts"] = 0
            df.at[rowcount,"wake_bouts"] = 0
    return df


def calculate_duration(data):

    bout_start_times = []
    bout_end_times = []
    bout_start = False
    for rowcount, row in enumerate(data):
        current_state = data[rowcount]
        if current_state == 1 and bout_start == False:
            bout_start_time = rowcount
            bout_start = True
        elif current_state == 0 and bout_start == True:
            bout_end_time = rowcount
            bout_start = False
            bout_start_times = np.append(bout_start_times, bout_start_time)
            bout_end_times = np.append(bout_end_times, bout_end_time)

    bout_durations = []
    for rowcount, row in enumerate(range(len(bout_start_times))):
        bout_duration = (bout_end_times[rowcount] - bout_start_times[rowcount])*5
        bout_durations = np.append(bout_durations, bout_duration)
    return bout_durations, bout_start_times, bout_end_times


def calculate_bout_duration(df):
    nrem_bouts, nrem_start_times, nrem_end_times = calculate_duration(np.array(df.loc[:, "nrem_bouts"]))
    rem_bouts, rem_start_times, rem_end_times = calculate_duration(np.array(df.loc[:, "rem_bouts"]))
    wake_bouts, wake_start_times, wake_end_times = calculate_duration(np.array(df.loc[:, "wake_bouts"]))

    df["rem_bout_durations"] = pd.Series(rem_bouts)
    df["nrem_bout_durations"] = pd.Series(nrem_bouts)
    df["wake_bout_durations"] = pd.Series(wake_bouts)

    df["rem_start_times"] = pd.Series(rem_start_times)
    df["nrem_start_times"] = pd.Series(nrem_start_times)
    df["wake_start_times"] = pd.Series(wake_start_times)
    return df


def plot_bout_durations(df, seizure_number, output_path):
    print('plotting histogram of average bout durations...')

    wake = np.nanmean(np.array(df.loc[:, "wake_bout_durations"]))
    nrem = np.nanmean(np.array(df.loc[:, "nrem_bout_durations"]))
    rem = np.nanmean(np.array(df.loc[:, "rem_bout_durations"]))

    wake_array = np.array(df.loc[:, "wake_bout_durations"])
    nrem_array = np.array(df.loc[:, "nrem_bout_durations"])
    rem_array = np.array(df.loc[:, "rem_bout_durations"])

    wake_shape = np.shape(wake_array[~np.isnan(wake_array)])[0]
    nrem_shape = np.shape(nrem_array[~np.isnan(nrem_array)])[0]
    rem_shape = np.shape(rem_array[~np.isnan(rem_array)])[0]

    wake_sd = np.nanstd(np.array(df.loc[:, "wake_bout_durations"]))/math.sqrt(wake_shape)
    nrem_sd = np.nanstd(np.array(df.loc[:, "nrem_bout_durations"]))/math.sqrt(nrem_shape)
    rem_sd = np.nanstd(np.array(df.loc[:, "rem_bout_durations"]))/math.sqrt(rem_shape)

    average_durations = [wake, nrem, rem]
    average_sd = [wake_sd, nrem_sd, rem_sd]
    bins = np.arange(3)

    color = ['LightSkyBlue', 'DodgerBlue', 'Blue']

    percent_histogram = plt.figure(figsize=(6, 4))
    ax = percent_histogram.add_subplot(1, 1, 1)  # specify (nrows, ncols, axnum)
    ax.bar(bins, average_durations, color = color)
    #ax.plot(np.random.uniform(low=0.6, high=1.4, size=(len(np.array(df.loc[:, "wake_bout_durations"])))), np.array(df.loc[:, "wake_bout_durations"]), color = "LightSkyBlue")
    ax.plot(np.random.uniform(low=1.6, high=2.4, size=(len(np.array(df.loc[:, "nrem_bout_durations"])))), np.array(df.loc[:, "nrem_bout_durations"]), color = "DodgerBlue")
    ax.plot(np.random.uniform(low=2.6, high=3.4, size=(len(np.array(df.loc[:, "rem_bout_durations"])))), np.array(df.loc[:, "rem_bout_durations"]), color = "Blue")
    plt.errorbar(bins, average_durations, average_sd, fmt='none', ls='', marker='o', capsize=5, capthick=1, ecolor='black')
    plt.ylabel('Average bout time (seconds)', fontsize=12, labelpad=10)
    plt.xlabel('Sleep state', fontsize=12, labelpad=10)
    plt.locator_params(axis='x', nbins=5)
    ax.set_xticklabels(['', 'Wake', 'nrem', 'rem'])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    plt.subplots_adjust(hspace=.35, wspace=.35, bottom=0.2, left=0.22, right=0.87, top=0.92)
    plt.savefig(output_path + '/average_bout_duration' + '.png', dpi=200)

    wake_array = np.array(df.loc[:, "wake_bout_durations"])
    wake = np.shape(wake_array[~np.isnan(wake_array)])[0]
    nrem_array = np.array(df.loc[:, "nrem_bout_durations"])
    nrem = np.shape(nrem_array[~np.isnan(nrem_array)])[0]
    rem_array = np.array(df.loc[:, "rem_bout_durations"])
    rem = np.shape(rem_array[~np.isnan(rem_array)])[0]

    average_durations = [wake, nrem, rem, seizure_number]
    bins = np.arange(4)

    percent_histogram = plt.figure(figsize=(6, 4))
    ax = percent_histogram.add_subplot(1, 1, 1)  # specify (nrows, ncols, axnum)
    ax.bar(bins, average_durations, color= color)
    plt.ylabel('Total number of bouts', fontsize=12, labelpad=10)
    plt.xlabel('Sleep state', fontsize=12, labelpad=10)
    plt.locator_params(axis='x', nbins=5)
    ax.set_xticklabels(['', 'Wake', 'nrem', 'rem', 'swd'])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    plt.subplots_adjust(hspace=.35, wspace=.35, bottom=0.2, left=0.22, right=0.87, top=0.92)
    plt.savefig(output_path + '/total_bout_number' + '.png', dpi=200)


def find_hourly_durations(durations, start_times):
    epochs_array = np.arange(0,17281, 720)
    hourly_duration = np.zeros((24))

    for rowcount, row in enumerate(range(24)):
        epoch_start = epochs_array[rowcount]
        epoch_end = epochs_array[rowcount + 1]
        times = durations[(start_times > epoch_start) & (start_times <= epoch_end)]
        hourly_duration[rowcount] = np.nanmean(times)
        if len(times) == 0:
            hourly_duration[rowcount] = 0

    return hourly_duration


def calculate_duration_per_hour(df):

    nrem_bouts = find_hourly_durations(np.array(df.loc[:, "nrem_bout_durations"]), np.array(df.loc[:, "nrem_start_times"]))
    rem_bouts = find_hourly_durations(np.array(df.loc[:, "rem_bout_durations"]), np.array(df.loc[:, "rem_start_times"]))
    wake_bouts = find_hourly_durations(np.array(df.loc[:, "wake_bout_durations"]), np.array(df.loc[:, "wake_start_times"]))

    df["rem_bout_duration_per_hour"] = pd.Series(rem_bouts)
    df["nrem_bout_duration_per_hour"] = pd.Series(nrem_bouts)
    df["wake_bout_duration_per_hour"] = pd.Series(wake_bouts)
    return df


def plot_total_durations(df, output_path):
    print('plotting histogram of total duration of each sleep state...')

    wake = np.array(df.loc[0:23, "wake_bout_duration_per_hour"])
    nrem = np.array(df.loc[0:23, "nrem_bout_duration_per_hour"])
    rem = np.array(df.loc[0:23, "rem_bout_duration_per_hour"])

    bins = np.arange(24)

    epochs_histogram = plt.figure(figsize=(6, 4))
    ax = epochs_histogram.add_subplot(1, 1, 1)  # specify (nrows, ncols, axnum)
    ax.bar(bins, rem, color = "Blue")
    ax.bar(bins, nrem, bottom = rem, color = "DodgerBlue")
    ax.bar(bins, wake, bottom = rem + nrem, color = "LightSkyBlue")
    plt.ylabel('Time (seconds)', fontsize=12, labelpad=10)
    plt.xlabel('Hour', fontsize=12, labelpad=10)
    plt.legend(["rem", "nrem", "wake"])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    plt.subplots_adjust(hspace=.35, wspace=.35, bottom=0.2, left=0.12, right=0.87, top=0.92)
    plt.savefig(output_path + '/bout_duration_per_hour' + '.png', dpi=200)
    return df


def save_states_to_csv(df, output_path):
    df.to_csv(output_path + 'sleep_states_per_hour.csv', sep='\t', encoding='utf-8', index=False, header=True)

def save_bout_durations_to_csv(df, output_path):
    df.to_csv(output_path + 'bout_durations.csv', columns = ['wake_bout_durations', 'nrem_bout_durations', 'rem_bout_durations'], sep='\t', encoding='utf-8', index=False, header=True)

def save_bout_durations_per_hour_to_csv(df, output_path):
    df["hour"] = pd.Series(np.arange(24))
    df.to_csv(output_path + 'bout_durations_per_hour.csv', columns = ['hour', 'wake_bout_duration_per_hour', 'nrem_bout_duration_per_hour', 'rem_bout_duration_per_hour'], sep='\t', encoding='utf-8', index=False, header=True)


def Analyse_SleepScore(sleep_state_path, seizure_times_path, output_path):
    # LOAD DATA
    data = process_dir(sleep_state_path) # overall data

    # SEIZURE CORRECTION
    data, seizure_number = correct_seizures(data, seizure_times_path)

    # CALCULATE TOTAL STATES
    df = calculate_total_states(data)
    plot_total_states(df, output_path)

    # CALCULATE STATES PER HOUR
    df = calculate_states_per_hour(data)
    df = calculate_percent_states_per_hour(df)
    plot_states_per_hour(df, output_path)

    save_states_to_csv(df, output_path)

    # CALCULATE NUMBER AND LENGTH OF BOUTS
    df = calculate_total_bouts(data)
    df = calculate_bout_duration(df)
    plot_bout_durations(df, seizure_number, output_path)

    save_bout_durations_to_csv(df, output_path)

    # CALCULATE TOTAL TIME IN EACH STATE
    df = calculate_duration_per_hour(df)
    plot_total_durations(df, output_path)

    save_bout_durations_per_hour_to_csv(df, output_path)





def main():
    print('-------------------------------------------------------------')
    print('-------------------------------------------------------------')

    #path to the recording .dat file
    file_name = '/Volumes/Sarah/SYNGAPE8/OUTPUT/SYNGAPE8/12W/SYNGAPE8_3131/SYNGAPE8_3131_BL1-dge_swd.csv'
    seizure_times_path = '/Volumes/Sarah/SYNGAPE8/OUTPUT/SYNGAPE8/12W/SYNGAPE8_3131/24h/seiz/SYNGAPE8_3131_BL1_Seizures.csv'
    output_path = '/Volumes/Sarah/SYNGAPE8/OUTPUT/SYNGAPE8/12W/SYNGAPE8_3131/'

    # LOAD DATA
    data = process_dir(file_name) # overall data

    # SEIZURE CORRECTION
    data, seizure_number = correct_seizures(data, seizure_times_path)

    # CALCULATE TOTAL STATES
    df = calculate_total_states(data)
    plot_total_states(df, output_path)

    # CALCULATE STATES PER HOUR
    df = calculate_states_per_hour(data)
    df = calculate_percent_states_per_hour(df)
    plot_states_per_hour(df, output_path)

    save_states_to_csv(df, output_path)

    # CALCULATE NUMBER AND LENGTH OF BOUTS
    df = calculate_total_bouts(data)
    df = calculate_bout_duration(df)
    plot_bout_durations(df, seizure_number, output_path)

    save_bout_durations_to_csv(df, output_path)

    # CALCULATE TOTAL TIME IN EACH STATE
    df = calculate_duration_per_hour(df)
    plot_total_durations(df, output_path)

    save_bout_durations_per_hour_to_csv(df, output_path)

    #COUNT SEIZURES 2 MIN EITHER SIZE OF SLEEP
    df = calculate_seizures_around_sleep(data, df)
    save_seizure_data_to_csv(df, output_path)

if __name__ == '__main__':
    main()

