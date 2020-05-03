## User guide

В файле `config.py` должна быть следующая информация:
```python
DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost / your host',
    'port': '5432 / your port',
    'username': 'your username',
    'password': 'your password',
    'database': 'your db'
}
```
При первом запуске, перейдите в  `/create_db`, чтобы создать таблицу для записи данных.

#### Приложением можно пользоваться через браузер. 
Чтобы отключить оформление и видеть только возращаемый json, в [`app.py`](app.py) 
измените значение переменной `BROWSER` с *'from_browser'* на любую другую строку (можно пустую).

В [html-коде](templates) страниц [`/`](templates/index.html) и 
[`/<model_id>`](templates/predict.html) внутри текстовых полей форм записаны примеры данных,
они не несут в себе никакого смысла.

В качестве [модели](model.py) для обучения я использую переделанную 
`_BaseRidgeCV` [[src](https://github.com/scikit-learn/scikit-learn/blob/95d4f0841/sklearn/linear_model/_ridge.py#L1520)].
Все изменения отмечены комментариями внутри кода.

##### /model/%MODEL_ID%/predict
Доступна для POST-запроса с телом вида `{"data": "c,b\n0.0,2.0\n0.0,2.0"}`.
Я убрала `"model_id": 1234` из передаваемых данных, потому что это значение и так берется
из самой ручки. Олсо, мне кажется странно иметь возможность попытаться отправить запрос с одним id 
в ручку с другим id.