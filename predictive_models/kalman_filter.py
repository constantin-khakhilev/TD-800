import json
import numpy as np
from filterpy.kalman import KalmanFilter
from vars import *


def run():
    # Чтение JSON файла
    with open(FORECAST_FILE_PATH, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Инициализация фильтра Калмана для сглаживания поля state
    kf = KalmanFilter(dim_x=1, dim_z=1)
    kf.x = np.array([[0.]])  # начальное значение
    kf.F = np.array([[1.]])  # модель перехода
    kf.H = np.array([[1.]])  # матрица наблюдения
    kf.P *= 1000.            # ковариационная матрица ошибки
    kf.R = 25                 # ковариационная матрица шума измерений
    kf.Q = 0.3               # ковариационная матрица шума процесса

    # Применение фильтра Калмана к полю state
    for item in data:
        state = item['state']
        kf.predict()
        kf.update(state)
        item['state'] = kf.x[0, 0]

    # Сохранение обновленных данных обратно в JSON файл
    with open(KM_FORECAST_FILE_PATH, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
