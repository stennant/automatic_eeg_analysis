import math

from pylab import *
from mne import io
import pandas as pd
import itertools
import os
import numpy as np


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
