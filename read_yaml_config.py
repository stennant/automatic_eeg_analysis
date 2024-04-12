import parameters
import datetime
import yaml
import pandas as pd

prm = parameters.Parameters()

def round_minutes(dt, direction, resolution):
    new_minute = (dt.minute // resolution + (1 if direction == 'up' else 0)) * resolution
    return dt + datetime.timedelta(minutes=new_minute - dt.minute)

def extract_date_and_time(yaml_path):
    # Read YAML file
    with open(yaml_path, 'r') as stream:
        data_loaded = yaml.safe_load(stream)

    print("I have loaded yaml configuration file")

    recording = data_loaded['recording']
    start_datetime = recording['start_datetime']
    timestamp = pd.Timestamp(start_datetime)

    timestamp_round = round_minutes(timestamp, "up", 1)
    timestamp_round = timestamp_round.round(freq='min')  # minute
    print("recording started at " + str(timestamp_round))

    return timestamp_round, start_datetime

def calculate_recording_start_and_end(timestamp, start_datetime):
    day = start_datetime.day + 1
    month = start_datetime.month
    year = start_datetime.year

    analysis_start = pd.Timestamp(year=year, month=month, day=day, hour=7)
    analysis_start = analysis_start.round(freq='min')  # minute
    analysis_end = pd.Timestamp(year=year, month=month, day=day+1, hour=7)

    print("analysing data from " + str(analysis_start) + " to " + str(analysis_end))

    total_seconds_day = 86400
    sampling_rate = 250.4
    samples_in_day = total_seconds_day*sampling_rate

    difference = analysis_start - timestamp
    difference_seconds = difference.total_seconds()
    difference_samples = difference_seconds * sampling_rate
    start_time = difference_samples
    end_time = start_time + samples_in_day

    print("sample start is " + str(start_time) + " sample end is " + str(end_time))

    return start_time, end_time


def calculate_recording_duration(yaml_path):

    timestamp, start_datetime = extract_date_and_time(yaml_path)

    starttime, endtime = calculate_recording_start_and_end(timestamp, start_datetime)

    prm.set_start_sample(starttime)
    prm.set_end_sample(endtime)
    return