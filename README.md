# TD-800
TripDetector - 800
Прогнозируем состояния гружености/порожности с помощью ML

### Настройка окружения

```
pip install matplotlib
pip install pandas
pip install -U scikit-learn
pip install tensorflow
```

* * *

### Запуск


**raw_data_from_v8** - содержит данный из таблицы архива и рейсов  
**initial_data** - содержит данные для обучения модели, эти данные готовятся из данных raw_data_from_v8  
**test_data** - содержит тестовый набор данных(сырую телеметрию из архива) для применения прогнозов обученной моделью
**forecast_data** - содержит тестовный набор с уже примененными прогнозами. По умолчанию отображется в графике при вызове show

  
Запуск подготовки данных, обучения и формирования прогноза:  
`python main.py -build`

  
Запуск построения графика  
`python main.py -show`

В файле **vars.py** содержатся настройки для подготовки и обучения. Необходимо корректно их заполнить перед запуском.


####Альтернативно есть линейная модель
Запуск построения графика для линейной модели
`python linear_model.py`
