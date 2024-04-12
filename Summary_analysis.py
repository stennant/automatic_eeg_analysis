import parameters
import sys
import os.path
import numpy as np
from numpy import *
import os
import mne
import pandas as pd
import matplotlib.pyplot as plt

seizure_summary_csv_path = '/Users/sarahtennant/Work_Alfredo/Analysis/SYNGAPE8/OUTPUT/SYNGAPE8/SYNGAPE8_176923/seiz/SYNGAPE8_176923_BL1_Seizures.csv'
seizure_totals_csv_path = '/Users/sarahtennant/Work_Alfredo/Analysis/SYNGAPE8/OUTPUT/SYNGAPE8/SYNGAPE8_176923/seiz/SYNGAPE8_176923_BL1_Seiz_Totals.csv'
sleep_score_csv_path = '/Users/sarahtennant/Work_Alfredo/Analysis/SYNGAPE8/OUTPUT/SYNGAPE8/SYNGAPE8_176923/SYNGAPE8_176923_BL1-dge_swd.csv'

output_figure_path = '/Users/sarahtennant/Work_Alfredo/Analysis/SYNGAPE8/Figures'
output_data_path = '/Users/sarahtennant/Work_Alfredo/Analysis/SYNGAPE8/Data_output'

animal_id = "SYNGAPE8_176923"



def main():
    print('-------------------------------------------------------------')
    print('-------------------------------------------------------------')
    print('Processing ' + str(animal_id))





    print('I have processed ' + str(animal_id))
    print('Data is saved in ' + str(output_data_path))
    print('Figures are saved in ' + str(output_figure_path))
    print('-------------------------------------------------------------')
    print('-------------------------------------------------------------')


if __name__ == '__main__':
    main()

