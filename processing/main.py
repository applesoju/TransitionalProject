import filter
from datetime import datetime

STATIONS_FILEPATH = 'C:\\Users\\patry\\Documents\\ProjPrzej\\resources\\stations.csv'
COUNTRIES_FILEPATH = 'C:\\Users\\patry\\Documents\\ProjPrzej\\filtered_resources\\country-list.txt'
FROM_YEAR = 2000
TO_YEAR = 2022

if __name__ == '__main__':
    print("Program started.")
    print(f'{datetime.now()}\n')
    
    stations = filter.get_stations_from_country_list(
        STATIONS_FILEPATH, COUNTRIES_FILEPATH)
    # filter.get_weather_data(stations, FROM_YEAR, TO_YEAR)
    
    daily_stations_dict = filter.check_years_with_daily_reports(stations)
    filter.save_daily_station_list(daily_stations_dict)

    print("Program finished.")
    print(f'{datetime.now()}\n')
