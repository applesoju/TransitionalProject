import filter
from datetime import datetime

STATIONS_FILEPATH = 'C:\\Users\\patry\\Documents\\ProjPrzej\\resources\\stations.csv'
COUNTRIES_FILEPATH = 'C:\\Users\\patry\\Documents\\ProjPrzej\\filtered_resources\\country-list.txt'
FROM_YEAR = 2000
TO_YEAR = 2020
FINISHED_DF_FILEPATH = 'C:\\Users\\patry\\Documents\\ProjPrzej\\filtered_resources\\finished_df.csv'


if __name__ == '__main__':
    print("Program started.")
    print(f'{datetime.now()}\n')
    
    stations = filter.get_stations_from_country_list(
        STATIONS_FILEPATH, COUNTRIES_FILEPATH)

    print('All relevant stations loaded.\n')
    # filter.get_weather_data(stations, FROM_YEAR, TO_YEAR)
    
    # daily_stations_dict = filter.check_years_with_daily_reports(stations)
    # filter.save_daily_station_list(daily_stations_dict)

    # stat = stations[1]
    # wdf = filter.get_dataframe(2000, stat)

    # stat_name = f'{stat.usaf}-{stat.wban}'
    # print(f'{stat_name}:\n{wdf}')

    # pwd = filter.process_weather_dataframe(wdf)
    # print(pwd.iloc[0])

    stat_list = filter.get_daily_station_list(2020)
    daily_stations = []
    for stat in stat_list:
        for st in stations:
            if st.usaf == stat[0] and st.wban == stat[1]:
                daily_stations.append(st)

    finished_df = filter.process_all_weather_dataframes(daily_stations, 2000, 2020)
    finished_df.to_csv(FINISHED_DF_FILEPATH)

    print("\nProgram finished.")
    print(f'{datetime.now()}\n')
