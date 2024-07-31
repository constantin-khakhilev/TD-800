import os


# #  Настройки для подготовки начальных данных
# INITIAIL_PATH = 'initial_data'
# ARCHIVE_FILE_PATH = 'raw_data_from_v8/eventarchive_1045_25072024_820.json'
# TRIP_FILE_PATH = 'raw_data_from_v8/trip_1045_25072024_820.json'
# START_STATE = 0  # С какого состояния начинаются данные в архиве 0 - разгрузен; 1 - погружен

#  Настройки для подготовки начальных данных
INITIAIL_PATH = os.path.abspath('initial_data')
INITIAIL_FILE_NAME = 'initial_data'
ARCHIVE_FILE_PATH = os.path.abspath('raw_data_from_v8/eventarchive_1045_25072024_820.json')
TRIP_FILE_PATH = os.path.abspath('raw_data_from_v8/trip_1045_25072024_820.json')
START_STATE = 1  # С какого состояния начинаются данные в архиве 0 - разгрузен; 1 - погружен

#  Настройки для запуска прогнозной модели
INITIAIL_FILE_PATH = os.path.abspath('initial_data/initial_data.json')
TEST_DATA_FILE_PATH = os.path.abspath('test_data/eventarchive_1045_26072024_820_test.json')
FORECAST_FILE_PATH = os.path.abspath('forecast_data/forecast_data.json')

FORECAST_LINEAR_FILE_PATH = os.path.abspath("forecast_data/forecast_linear_data.json")

# _path = os.path.abspath(INITIAIL_PATH)
# print(INITIAIL_FILE_PATH)