import pandas as pd

import filter
from datetime import datetime

STATIONS_FILEPATH = 'C:\\Users\\patry\\Documents\\ProjPrzej\\resources\\stations.csv'
COUNTRIES_FILEPATH = 'C:\\Users\\patry\\Documents\\ProjPrzej\\filtered_resources\\country-list.txt'
FROM_YEAR = 2000
TO_YEAR = 2020
FINISHED_DF_FILEPATH = 'C:\\Users\\patry\\Documents\\ProjPrzej\\filtered_resources\\finished_df.csv'
FEATURE_SCORES_DIR = 'C:\\Users\\patry\\Documents\\ProjPrzej\\figures'
UNWANTED_COLUMNS = ['Liquid_Precipitation_Depth_Dimension_1hr_Mean',
                    'Liquid_Precipitation_Depth_Dimension_1hr_Median',
                    'Liquid_Precipitation_Depth_Dimension_1hr_Min',
                    'Liquid_Precipitation_Depth_Dimension_1hr_Max',
                    'Liquid_Precipitation_Depth_Dimension_6hrs_Mean',
                    'Liquid_Precipitation_Depth_Dimension_6hrs_Median',
                    'Liquid_Precipitation_Depth_Dimension_6hrs_Min',
                    'Liquid_Precipitation_Depth_Dimension_6hrs_Max']


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

    # stat_list = filter.get_daily_station_list(2020)
    #
    # daily_stations = []
    #
    # for stat in stat_list:
    #     for st in stations:
    #         if st.usaf == stat[0] and st.wban == stat[1]:
    #             daily_stations.append(st)
    #
    # finished_df = filter.process_all_weather_dataframes(daily_stations, 2000, 2020)
    # finished_df.to_csv(FINISHED_DF_FILEPATH, index=False)
    #
    # df_to_f
    # clean_up = pd.read_csv(FINISHED_DF_FILEPATH)
    # clean_df = filter.remove_unwanted_features_from_df(df_to_clean_up, UNWANTED_COLUMNS)
    # clean_df.to_csv(FINISHED_DF_FILEPATH, index=False)

    fdf = pd.read_csv(FINISHED_DF_FILEPATH)
    filter.plot_feature_scores(fdf, 'Air_Temperature_Mean', FEATURE_SCORES_DIR, True)

    print("\nProgram finished.")
    print(f'{datetime.now()}\n')
