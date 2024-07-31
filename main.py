from prepare_initial_data import prepare as prepare_data
from predictive_models import lstm
from show_graph import show
import sys
# sys.path.append('vars')




if __name__ == '__main__':
    arg = sys.argv[1]
    if arg == '-build':
        prepare_data()  # готовим данные
        lstm.run()  # запускаем обучение и формирования прогноза
    elif arg == '-show':
        show()
    else:
        print('Передайте аргументы -build или -show')

