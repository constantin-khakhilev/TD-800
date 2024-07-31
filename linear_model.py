from sklearn.linear_model import RidgeClassifier
import pandas as pd
from vars import *
import json
import matplotlib.pyplot as plt
from datetime import datetime


if __name__ == "__main__":
    data = pd.read_csv("initial_data/initial_data.csv")
    X = data.drop(columns=['time', 'state'])
    y = data['state']
    reg = RidgeClassifier().fit(X, y)

    with open(TEST_DATA_FILE_PATH, 'r', encoding='utf-8') as file:
        test_data = json.load(file)
    test_data = pd.DataFrame(test_data)

    test_data['state'] = reg.predict(test_data.drop(columns=['time']))
    test_data['time'] = pd.to_datetime(test_data['time'])

    test_data.to_json(FORECAST_LINEAR_FILE_PATH, orient='records', date_format='iso')

    with open(FORECAST_LINEAR_FILE_PATH, 'r', encoding='utf-8') as file:
        data = json.load(file)

    FORMAT_1 = '%Y-%m-%dT%H:%M:%S.%fZ'
    FORMAT_2 = '%Y-%m-%d %H:%M:%S'


    speed_x = [datetime.strptime(i['time'], FORMAT_1) for i in data]
    speed_y = [i['speed'] for i in data]

    weight_x = [datetime.strptime(i['time'], FORMAT_1) for i in data]
    weight_y = [i['weight'] for i in data]

    state_x = [datetime.strptime(i['time'], FORMAT_1) for i in data]
    state_y = [i['state'] for i in data]

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax3 = ax1.twinx()

    ax1.plot(speed_x, speed_y, color='tab:blue')
    ax2.plot(weight_x, weight_y, color='tab:red')
    ax3.plot(state_x, state_y, color='yellow')

    plt.xlabel('x - axis')
    plt.ylabel('y - axis')
    plt.title('Forecast graph!')

    # function to show the plot
    plt.show()