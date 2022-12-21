import csv
import os
import subprocess
from datetime import datetime
import gzip
import io
import pandas as pd
import numpy as np

import requests

from station import Station

WEATHER_DATA_URL = 'https://www1.ncdc.noaa.gov/pub/data/noaa/isd-lite/'
SAVE_DATA_DIR = 'C:\\Users\\patry\\Documents\\ProjPrzej\\filtered_resources\\data'
SAVE_DAILY_STATION_LIST_DIR = 'C:\\Users\\patry\\Documents\\ProjPrzej\\filtered_resources'
FILE_ROW_LENGHT = 62
WEATHER_DF_COLUMN_NAMES = [
    'Year', 'Month', 'Day', 'Hour',
    'Air_Temperature', 'Dew_Point_Temperature',
    'Sea_Level_Pressure', 'Wind_Direction', 'Wind_Speed_Rate',
    'Sky_Condition_Total_Coverage_Code',
    'Liquid_Precipitation_Depth_Dimension_1hr', 'Liquid_Precipitation_Depth_Dimension_6hrs'
]
WEATHER_STATS_COLUMN_NAMES = WEATHER_DF_COLUMN_NAMES[:3] +\
                             WEATHER_DF_COLUMN_NAMES[4:7] +\
                             WEATHER_DF_COLUMN_NAMES[-2:]


# Gets a list of FIPS IDs from a '.txt' file
def get_fips_list(countries_filepath):
    # Get all rows from the file
    with open(countries_filepath, 'r') as countries_file:
        countries_rows = countries_file.readlines()

    # Create a list of FIPS IDs of countries
    fips_id_list = []
    for row in countries_rows[1:]:
        fips_id_list.append(row[:2])

    return fips_id_list


# Gets a list of Station objects that are from countries provided in file
def get_stations_from_country_list(stations_csv_path, countries_filepath):
    # Get a list of countries' FIPS IDs
    countries_list = get_fips_list(countries_filepath)
    stations_list = []

    # Open a file containing the list of all stations
    with open(stations_csv_path, newline='') as csv_file:
        stations_reader = csv.reader(csv_file, delimiter=';')

        for row in stations_reader:
            # Ignore stations that are not in the country from the list
            if row[3] not in countries_list:
                continue
            # Ignore stations that didn't work after 01.01.1970
            if int(row[-1]) < 19700101:
                continue
            # Ignore stations that are too far east
            if row[7] != '' and float(row[7]) > 69.03333:
                continue

            # Get all relevant station information and save it in a list
            usaf, wban, station_name, country, lat, long = \
                row[0], row[1], row[2], row[3], row[6], row[7]
            new_station = Station(usaf, wban, station_name, country, lat, long)
            stations_list.append(new_station)

    return stations_list


# Gets all weather data from specified year range and stations
def get_weather_data(stations_list, from_year, to_year):
    year_range = range(from_year, to_year + 1)

    # Create a directory for data storage if it doesn't exist
    if not os.path.exists(SAVE_DATA_DIR):
        subprocess.call(['mkdir', SAVE_DATA_DIR], shell=True)

    # For every year from a given range
    for year in year_range:
        print(f'Started file donwloading for {year}')

        dir_url = WEATHER_DATA_URL + f'/{year}'
        save_data_in = SAVE_DATA_DIR + f'\\{year}'
        station_count = 0

        # Create a directory for a specific year if it doesn't exist
        if not os.path.exists(save_data_in):
            subprocess.call(['mkdir', save_data_in], shell=True)

        # For every station from the list
        for station in stations_list:
            station_count += 1

            # Print a notice every 500 files
            if station_count % 500 == 0:
                print(f'Checked {station_count} files.')

            file_name = f'{station.usaf}-{station.wban}-{year}.gz'
            station_data_url = f'{dir_url}/{file_name}'

            # If station data from this year already exists then skip this file
            #   unless it's the current year
            if os.path.exists(f'{save_data_in}\\{file_name}') and datetime.today().year != year:
                continue

            # Try to download the file
            response = requests.get(station_data_url)
            if response.status_code == 404:
                continue

            # If the file download is successful then save it
            with open(save_data_in + f'\\{file_name}', 'wb') as data_file:
                data_file.write(response.content)

        # Print a notice when the year is done
        print(f'Year {year} done.')
        print(f'{datetime.now()}\n')


def check_years_with_daily_reports(stations):
    days_in_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    years = os.listdir(SAVE_DATA_DIR)[:-1]

    daily_rep_count = {}
    for s in stations:
        station_id = f'{s.usaf}-{s.wban}'
        daily_rep_count[station_id] = []

    for y in years:
        year_path = f'{SAVE_DATA_DIR}\\{y}'
        file_list = os.listdir(year_path)

        for f in file_list:
            file_path = f'{year_path}\\{f}'

            column_names = ['y', 'm', 'd']
            records_df = pd.read_csv(file_path,
                                     sep=' ',
                                     skipinitialspace=True,
                                     names=column_names,
                                     usecols=column_names)

            month_count = len(records_df.m.unique())
            if month_count != 12:
                continue

            day_lists = records_df.groupby('m').d.unique()
            day_counts = [len(i) for i in day_lists]

            dim = days_in_months.copy()
            if int(y) % 4 == 0 and not int(y) % 100 == 0:
                dim[1] += 1

            elif int(y) % 400 == 0:
                dim[1] += 1

            if day_counts != dim:
                continue

            station_id = f[:-8]
            daily_rep_count[station_id].append(y)

    return daily_rep_count


def save_daily_station_list(stations_dict):
    output_str = ''
    year_range = [str(i) for i in range(2000, 2022)]
    daily_rep_every_year_count = [0 for _ in year_range]

    for station in stations_dict:
        year_list = stations_dict[station]
        output_str += f'{station}: ' + ', '.join(year_list) + '\n'

        for i in range(0, 22):
            if len(year_list) == i + 1 and year_list == year_range[:(i + 1)]:
                daily_rep_every_year_count[i] += 1

    output_str += '\n'
    for i, count in enumeratte(daily_rep_every_year_count):
        output_str += f'Number of stations that have daily report every year until year {2000 + i}: {count}\n'

    if not os.path.exists(SAVE_DAILY_STATION_LIST_DIR):
        subprocess.call(['mkdir', SAVE_DAILY_STATION_LIST_DIR], shell=True)

    with open(f'{SAVE_DAILY_STATION_LIST_DIR}\\daily_check.txt', 'w') as save_file:
        save_file.write(output_str)


def get_daily_station_list(to_year):
    daily_stations_ids = []
    wanted_year_sequence = [str(i) for i in range(2000, to_year + 1)]

    daily_check_file_path = f'{SAVE_DAILY_STATION_LIST_DIR}\\daily_check.txt'
    if not os.path.exists(daily_check_file_path):
        print('No daily_check.txt file.')
        raise FileExistsError

    with open(daily_check_file_path, 'r') as dcf:
        lines = dcf.readlines()

        for line in lines:
            if len(line) == 1:
                break

            stat_id, year_str = line.split(':')
            year_list = [y.strip() for y in year_str.split(',')]

            if year_list == wanted_year_sequence:
                usaf, wban = stat_id.split('-')
                daily_stations_ids.append((usaf, wban))

    return daily_stations_ids


def get_dataframe(year, station):
    col_names = WEATHER_DF_COLUMN_NAMES
    file_path = f'{SAVE_DATA_DIR}\\{year}\\{station.usaf}-{station.wban}-{year}.gz'

    if not os.path.exists(file_path):
        return None

    weather_df = pd.read_csv(file_path,
                             sep=' ',
                             skipinitialspace=True,
                             names=col_names)

    # return weather_df.loc[0]      # for testing
    return weather_df


def process_weather_dataframe(weather_dataframe):
    new_df = pd.DataFrame()

    wdf_replaced = weather_dataframe.replace(-9999, np.NaN)
    df_mean = wdf_replaced.groupby(WEATHER_STATS_COLUMN_NAMES[:3]).mean().reset_index()
    df_med = wdf_replaced.groupby(WEATHER_STATS_COLUMN_NAMES[:3]).median().reset_index()
    df_min = wdf_replaced.groupby(WEATHER_STATS_COLUMN_NAMES[:3]).min().reset_index()
    df_max = wdf_replaced.groupby(WEATHER_STATS_COLUMN_NAMES[:3]).max().reset_index()

    df_stats = [df_mean, df_med, df_min, df_max]
    stat_names = ['_Mean', '_Median', '_Min', '_Max']

    sample_df = df_mean

    for ymd in WEATHER_STATS_COLUMN_NAMES[:3]:
        new_df[ymd] = sample_df[ymd]

    for col in WEATHER_STATS_COLUMN_NAMES[3:]:
        for i, stat in enumerate(df_stats):
            new_name = col + stat_names[i]
            new_df[new_name] = stat[col]

    return new_df


def process_all_weather_dataframes(stations, y_start, y_stop):
    all_data_df = pd.DataFrame()

    for y in range(y_start, y_stop + 1):
        for st in stations:
            st_df = get_dataframe(y, st)
            processed_df = process_weather_dataframe(st_df)
            processed_df['Station'] = f'{st.usaf}-{st.wban}'

            columns = list(processed_df.columns.values)
            new_cols = columns[-1:] + columns[:-1]
            processed_df = processed_df[new_cols]

            all_data_df = pd.concat([all_data_df, processed_df])

    return all_data_df
