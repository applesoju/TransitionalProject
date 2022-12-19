import filter
from datetime import datetime

STATIONS_FILEPATH = 'C:\\Users\\patry\\Documents\\ProjPrzej\\resources\\stations.csv'
COUNTRIES_FILEPATH = 'C:\\Users\\patry\\Documents\\ProjPrzej\\filtered_resources\\country-list.txt'
FROM_YEAR = 2000
TO_YEAR = 2022
WEATHER_DF_COLUMN_NAMES = [
    'Year', 'Month', 'Day', 'Hour',
    'Air_Temperature', 'Dew_Point_Temperature',
    'Sea_Level_Pressure', 'Wind_Direction', 'Wind_Speed_Rate',
    'Sky_Condition_Total_Coverage_Code',
    'Liquid_Precipitation_Depth_Dimension_1hr', 'Liquid_Precipitation_Depth_Dimension_6hrs'
]

if __name__ == '__main__':
    print("Program started.")
    print(f'{datetime.now()}\n')
    
    stations = filter.get_stations_from_country_list(
        STATIONS_FILEPATH, COUNTRIES_FILEPATH)

    print('All relevant stations loaded.\n')
    # filter.get_weather_data(stations, FROM_YEAR, TO_YEAR)
    
    # daily_stations_dict = filter.check_years_with_daily_reports(stations)
    # filter.save_daily_station_list(daily_stations_dict)

    stat = stations[1]
    out = filter.get_dataframe(2000, stat, WEATHER_DF_COLUMN_NAMES)

    stat_name = f'{stat.usaf}-{stat.wban}'
    print(f'{stat_name}:\n{out}')

    print("\nProgram finished.")
    print(f'{datetime.now()}\n')
