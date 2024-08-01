import pandas as pd
import numpy as np
import json
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv1D, GlobalMaxPooling1D, Dense
from keras.src.utils import to_categorical
from vars import *


def run():

    with open(INITIAIL_FILE_PATH, 'r', encoding='utf-8') as file:
        data = json.load(file)

    df = pd.DataFrame(data)
    df['time'] = pd.to_datetime(df['time'])

    # Создание признаков
    df['speed_diff'] = df['speed'].diff().fillna(0)
    df['weight_diff'] = df['weight'].diff().fillna(0)
    df['lon_diff'] = df['lon'].diff().fillna(0)
    df['lat_diff'] = df['lat'].diff().fillna(0)

    # Выбор признаков и метки
    features = df[['speed', 'weight', 'lon', 'lat', 'speed_diff', 'weight_diff', 'lon_diff', 'lat_diff']].values
    labels = df['state'].values

    # Стандартизация данных
    scaler = StandardScaler()
    features = scaler.fit_transform(features)

    # Преобразование меток в категориальные
    labels = to_categorical(labels)

    # Формирование последовательностей
    def create_sequences(data, labels, seq_length=5):
        sequences = []
        labels_seq = []
        for i in range(len(data) - seq_length + 1):
            sequences.append(data[i:i + seq_length])
            labels_seq.append(labels[i + seq_length - 1])
        return np.array(sequences), np.array(labels_seq)

    seq_length = 3
    X, y = create_sequences(features, labels, seq_length)

    # Разделение данных на обучающую и тестовую выборки
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    X_train = X
    y_train = y

    # Создание модели Conv1D
    model = Sequential()
    model.add(Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(seq_length, X_train.shape[2])))
    model.add(GlobalMaxPooling1D())
    model.add(Dense(50, activation='relu'))
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
    new_df['lon_diff'] = new_df['lon'].diff().fillna(0)
    new_df['lat_diff'] = new_df['lat'].diff().fillna(0)

    # Подготовка новых данных
    new_features = new_df[['speed', 'weight', 'lon', 'lat', 'speed_diff', 'weight_diff', 'lon_diff', 'lat_diff']].values
    new_features = scaler.transform(new_features)

    # Убедитесь, что длины совпадают
    if len(new_features) >= seq_length:
        X_new, _ = create_sequences(new_features, np.zeros((len(new_features), 3)), seq_length)
        predictions = np.argmax(model.predict(X_new), axis=1)

        # Добавление меток событий обратно к DataFrame
        new_df = new_df.iloc[seq_length - 1:].copy()
        new_df['state'] = predictions

    # Запись DataFrame в файл JSON
    new_df.to_json(FORECAST_FILE_PATH, orient='records', date_format='iso')

    print(new_df)
