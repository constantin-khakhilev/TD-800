import json
import random
import csv
from datetime import datetime
from vars import *


def get_trip_state_events() -> dict:
    """
    Формируем события переключения в состояние гружености/порожности по таблице рейсов.
    """
    with open(TRIP_FILE_PATH, 'r', encoding='utf-8') as file:
        data_events = json.load(file)

    state_map_switches = {
        'to_load': [],
        'to_unload': []
    }

    for i in data_events:
        if i['begin_time'] not in state_map_switches['to_load']:
            state_map_switches['to_load'].append(
                datetime.strptime(i['begin_time'][:19], '%Y-%m-%d %H:%M:%S')
                # i['begin_time'][:19]
            )
        if i['end_time'] not in state_map_switches['to_unload']:
            state_map_switches['to_unload'].append(
                datetime.strptime(i['end_time'][:19], '%Y-%m-%d %H:%M:%S')
                # i['end_time'][:19]
            )
    return state_map_switches


def read_eventarchive_data() -> list[dict]:
    """
    Читаем данные архива
    """

    with open(ARCHIVE_FILE_PATH, 'r', encoding='utf-8') as file:
        ea_data = json.load(file)

    for i in ea_data:
        i['time'] = datetime.strptime(i['time'][:19], '%Y-%m-%d %H:%M:%S')
    return ea_data


def set_state(ea_data, state_map_switches):
    """
    Проставляем состояние к данным архива
    """

    state = START_STATE
    for item in sorted(ea_data, key=lambda x: x['time']):
        if item['time'] in state_map_switches['to_load']:
            state = 1
        elif item['time'] in state_map_switches['to_unload']:
            state = 0

        item['state'] = state
    return ea_data


def write_data(data, name='initial_data', formats=None):
    """
    Сохраняем данные
    """
    if formats is None:
        formats = ['json', 'csv']

    # Форматируем время
    for i in data:
        i['time'] = i['time'].strftime(format='%Y-%m-%d %H:%M:%S')

    if 'json' in formats:
        with open(f'{INITIAIL_PATH}/{name}.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Данные сформированы и сохранены в '{INITIAIL_PATH}/{name}.json'")

    if 'csv' in formats:
        with open(f'{INITIAIL_PATH}/{name}.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['time', 'lon', 'lat', 'speed', 'weight', 'state']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print(f"Данные сформированы и сохранены в '{INITIAIL_PATH}/{name}.csv'")


def prepare():
    state_map_switches = get_trip_state_events()
    clean_ea_data = read_eventarchive_data()
    ea_data = set_state(clean_ea_data, state_map_switches)
    write_data(ea_data, name=INITIAIL_FILE_NAME)


# if __name__ == '__main__':
#     prepare()