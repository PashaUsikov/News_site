# Новостной сайт
Это WEB-приложение - Новостной сайт о последних событиях в Крыму, погоде, а также можно зарегистрироваться на сайте и оставлять комментарии.

## Установка

Скачайте проект с githab:
```
git clone https://
```

Создайте виртуальное окружение и установите зависимости:
```
pip install -r requirements.txt
```

Создайте файл config.py и задайте в нём базовые переменные:
```
from datetime import timedelta
import os

basedir = os.path.abspath(os.path.dirname(__file__))

WEATHER_DEFAULT_CITY = "Moscow,Russia"
WEATHER_API_KEY = "Your secret key here"
WEATHER_URL = "http://api.worldweatheronline.com/premium/v1/weather.ashx"
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'webapp.db')

SECRET_KEY = "Your secret key here"

REMEMBER_COOKIE_DURATION = timedelta(days=5)
```

## Создание миграций

Linux и Mac: 
Создание папки migrations
```
export FLASK_APP=webapp && flask db init
```
Добавим новое поле в модель или внесём изменения

Создадим миграцию 

```
flask db migrate -m "Описание того, что создаётся"
```
и выполним её
```
flask db upgrade
```

Windows: 
Создание папки migrations
```
set FLASK_APP=webapp && flask db init
```

Когда есть уже база данных и в качестве примера работы сделаем перемещение
```
move webapp.db webapp.db.old
```

Делаем первую миграцию
```
set FLASK_APP=webapp && flask db migrate -m "users and news tables"
```

Миграция применяется командой
```
flask db upgrade
```

Делаем обратное перемещение
```
move webapp.db.old webapp.db
```

Чтобы работать с миграциями на существующей базе, нам нужно пометить нашу миграцию как выполненную командой (у вас номер миграции будет другой)
```
flask db stamp 14d6f881e6a3
```
Добавим новое поле в модель или внесём изменения

Создадим миграцию 
```
flask db migrate -m "Specify what has been added or changed"
```
и выполним её
```
flask db upgrade
```

## Для парсинга по расписанию:

Windows:

Установить Linux-подсистему (Ubuntu) для Windows.
В командной строке Windows вызвать Linux-подсистему (Ubuntu) - `wsl`. Далее здесь же:
При первой установке
```
sudo apt-get install redis-server
```
```
sudo systemctl enable redis-server.service
```
В следующий раз можно начинать с этой строки
```
sudo service redis-server start
```
```
redis-cli
```
```
monitor
```
Запустить celery в отдельной командной строке Windows в папке приложения или окне терминала:
```
celery -A tasks worker -l info --pool=solo
```
Чтобы запуск задач по расписанию работал, мы должны запустить celery-beat также в отдельной командной строке Windows в папке приложения или окне терминала:
```
celery -A tasks beat
```


## Запуск программы

Для запуска программы и вывода в браузер запустите файл:

Скрипт для Linux и MacOs

Linux и Mac: 
В корне проекта создайте файл run.sh:
#!/bin/sh
export FLASK_APP=webapp && export FLASK_ENV=development && flask run
Сохраните файл и в корне проекта выполните в консоли команду chmod +x run.sh - это сделает файл исполняемым. Теперь для запуска проекта нужно писать 
```
./run.sh. 
```

Windows:
```
run.bat
```
или 

```
set FLASK_APP=webapp && set FLASK_ENV=development && set FLASK_DEBUG=1 && flask run
```
