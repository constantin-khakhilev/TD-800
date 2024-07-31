import json
import pandas as pd
import numpy as np
from keras.src.utils import to_categorical
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras import Sequential
from tensorflow.keras.layers import LSTM, Dense
from vars import *


def run():
    with open(INITIAIL_FILE_PATH, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Пример данных с метками
    # data = [
    #     {"time": "2024-07-25 13:00:00+00", "speed": 0, "weight": 1, "event": 0},
    #     {"time": "2024-07-25 13:05:00+00", "speed": 5, "weight": 10, "event": 1},  # Погрузка
    #     {"time": "2024-07-25 13:10:00+00", "speed": 15, "weight": 10, "event": 0},
    #     {"time": "2024-07-25 13:15:00+00", "speed": 0, "weight": 1, "event": 2},  # Разгрузка
    #     {"time": "2024-07-25 13:20:00+00", "speed": 0, "weight": 1, "event": 0},
    #     # Добавьте больше данных по мере необходимости
    # ]

    df = pd.DataFrame(data)
    df['time'] = pd.to_datetime(df['time'])

    # Создание признаков
    df['speed_diff'] = df['speed'].diff().fillna(0)
    df['weight_diff'] = df['weight'].diff().fillna(0)

    # Выбор признаков и метки
    features = df[['speed', 'weight', 'speed_diff', 'weight_diff']].values
    labels = df['state'].values

    # Стандартизация данных
    scaler = StandardScaler()
    features = scaler.fit_transform(features)

    # Преобразование меток в категориальные
    labels = to_categorical(labels)

    # Формирование последовательностей
    def create_sequences(data, labels, seq_length=3):
        sequences = []
        labels_seq = []
        for i in range(len(data) - seq_length + 1):
            sequences.append(data[i:i + seq_length])
            labels_seq.append(labels[i + seq_length - 1])
        return np.array(sequences), np.array(labels_seq)

    seq_length = 5
    X, y = create_sequences(features, labels, seq_length)

    # Разделение данных на обучающую и тестовую выборки
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Создание модели LSTM
    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=(seq_length, X_train.shape[2])))
    model.add(Dense(2, activation='softmax'))  # Три класса: нет события, погрузка, разгрузка

    # Компиляция модели
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # Обучение модели
    model.fit(X_train, y_train, epochs=20, batch_size=16, validation_split=0.2)


    with open(TEST_DATA_FILE_PATH, 'r', encoding='utf-8') as file:
        new_data = json.load(file)

    new_df = pd.DataFrame(new_data)
    new_df['time'] = pd.to_datetime(new_df['time'])
    new_df['speed_diff'] = new_df['speed'].diff().fillna(0)
    new_df['weight_diff'] = new_df['weight'].diff().fillna(0)

    # Подготовка новых данных
    new_features = new_df[['speed', 'weight', 'speed_diff', 'weight_diff']].values
    new_features = scaler.transform(new_features)


    # X_new, _ = create_sequences(new_features, np.zeros((len(new_features), 3)), seq_length)
    #
    # # Предсказание событий на новых данных
    # new_df['event'] = np.argmax(model.predict(X_new), axis=1)

    # print(new_df)

    if len(new_features) >= seq_length:
        X_new, _ = create_sequences(new_features, np.zeros((len(new_features), 3)), seq_length)
        predictions = np.argmax(model.predict(X_new), axis=1)

        # Добавление меток событий обратно к DataFrame
        new_df = new_df.iloc[seq_length - 1:].copy()
        new_df['state'] = predictions


    new_df.to_json(FORECAST_FILE_PATH, orient='records', date_format='iso')
    # print(new_df)