import pandas as pd

import filter
from datetime import datetime
import time
from xgboost import XGBRegressor
import numpy as np
from sklearn.model_selection import RepeatedKFold, cross_validate, train_test_split
from sklearn.preprocessing import OrdinalEncoder, LabelEncoder
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.metrics import accuracy_score, mean_absolute_error, r2_score


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

    variable_to_predict = 'Air_Temperature_Mean'

    print(f'Loading data from file...')

    fdf = pd.read_csv(FINISHED_DF_FILEPATH)
    # chosen_features = filter.get_feature_scores_plots(fdf, variable_to_predict, FEATURE_SCORES_DIR, True, 10)
    chosen_features = list(fdf.columns.values)[1: 11]

    print(f'\nBest features:')
    for feat in chosen_features:
        print(feat)

    data_for_reg = fdf[chosen_features]

    print(f'\nEncoding nominal features...')

    ord_enc = OrdinalEncoder()
    encoded_cols = ord_enc.fit_transform(data_for_reg[['Station', 'Date']])
    data_for_reg.loc[:, ['Station', 'Date']] = encoded_cols

    print(f'\nImputing missing data...')

    imp = IterativeImputer(max_iter=20, random_state=41)
    imputed_data = imp.fit_transform(data_for_reg)
    impudata_df = pd.DataFrame(imputed_data)
    impudata_df.columns = data_for_reg.columns
    data_for_reg = impudata_df

    print(f'\nModel cross validation started... ')

    x = data_for_reg
    y = data_for_reg[variable_to_predict]
    x = x.drop(x.iloc[[-1]].index)
    y = y.drop(y.iloc[[0]].index)

    model = XGBRegressor()

    rskf = RepeatedKFold(n_splits=10, n_repeats=10, random_state=144)

    start = time.time()
    n_scores = cross_validate(model, x, y, scoring=['r2', 'neg_mean_absolute_error', 'max_error'], n_jobs=1, cv=rskf)
    print(f'Cross validation time: {round(time.time() - start, 2)} seconds')

    merr = n_scores['test_max_error']
    mae = n_scores['test_neg_mean_absolute_error']
    r2 = n_scores['test_r2']

    print(f'Max Error from Cross Validation:\n'
          f"Mean = {np.mean(merr):.3f}, STD = {np.std(merr):.3f}, Min = {np.min(merr)}, Max = {np.mean(merr)}")

    print(f'Mean Absolute Error from Cross Validation:\n'
          f"Mean = {np.mean(mae):.3f}, STD = {np.std(mae):.3f}, Min = {np.min(mae)}, Max = {np.mean(mae)}")

    print(f'r2 from Cross Validation:\n'
          f"Mean = {np.mean(r2):.3f}, STD = {np.std(r2):.3f}, Min = {np.min(r2)}, Max = {np.mean(r2)}")

    # y_pred = model.predict(X=x.iloc[len(x) // 2 - 30: len(x) // 2])
    # y_true = y.iloc[len(x) // 2 - 30: len(x) // 2]
    # for i, pred in enumerate(y_pred):
    #     print(f'Correct value: {y_true.iloc[i]}')
    #     print(f'Predicted value: {pred}\n')

    print("\nProgram finished.")
    print(f'{datetime.now()}\n')

    # mae, r2, max mae
    # kfold crossvalidation
    # 5 różnych seedów i uśrednić statystyki
    # serialize model
    # check params for xgb (r2 > 0.9)
    # grid search (parametry) - r2 lub mae