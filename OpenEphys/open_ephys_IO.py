from OpenEphys import Load_OpenEphys
import numpy as np
import matplotlib.pylab as plt


def get_data_continuous(prm, file_path):
    data = Load_OpenEphys.load(file_path)
    signal = data['data']
    signal = np.asanyarray(signal)
    return signal


def get_events(prm, file_path):
    events = Load_OpenEphys.load(file_path)
    return events