import subprocess
from station import Station
import csv
import requests
import os
from datetime import datetime


WEATHER_DATA_URL = 'https://www1.ncdc.noaa.gov/pub/data/noaa/isd-lite/'
SAVE_DATA_DIR = 'C:\\Users\\patry\\Documents\\ProjPrzej\\filtered_resources\\data'


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
            usaf, wban, station_name, country, lat, long =\
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


def filter_out_ow_stations():
    raise NotImplementedError
# def count_stations_with_daily_reports():
#     years = os.listdir(SAVE_DATA_DIR)
    
#     for gz_list in 
    
#     return 0
