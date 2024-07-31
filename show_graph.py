import json
import matplotlib.pyplot as plt
from datetime import datetime
from vars import *

def show():

    with open(FORECAST_FILE_PATH, 'r', encoding='utf-8') as file:
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
