"""
Author: Sarah Tennant
Date: 8/8/2024
Script: Control_Post_Analysis.py

Description: 

"""

import SleepScore_Analysis
import Seizure_Analysis


def main():
    print('-------------------------------------------------------------')
    print('-------------------------------------------------------------')

    #path to the recording .dat file
    sleep_state_path = '/Volumes/Sarah/SYNGAPE8/OUTPUT/SYNGAPE8/12W/SYNGAPE8_3138/SYNGAPE8_3138_BL1-dge_swd.csv'
    seizure_times_path = '/Volumes/Sarah/SYNGAPE8/OUTPUT/SYNGAPE8/12W/SYNGAPE8_3138/24h/seiz/SYNGAPE8_3138_BL1_Seizures.csv'
    output_path = ('/Volumes/Sarah/SYNGAPE8/OUTPUT/SYNGAPE8/12W/SYNGAPE8_3138/')

    SleepScore_Analysis.Analyse_SleepScore(sleep_state_path, seizure_times_path, output_path)
    Seizure_Analysis.Analyse_SleepScore(sleep_state_path, seizure_times_path, output_path)


if __name__ == '__main__':
    main()

