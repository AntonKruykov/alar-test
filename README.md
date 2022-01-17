## Описание

Проект состоит из 3х микросервисов. Все миктосервисы взаимодействуют друг
с другом по http.

### route_storage
Хранит данных о пользователях, точках и маршрутах.
Функционал авторизации и выдача информации о точках и маршрутах.

Запускается на localhost:8080

### route_calculator
Микросервис занимается вычислением опитимальных маршрутов. 
После вычисления маршрут отсылается route_storage

Запускается на localhost:8081

### route_report
Хранит преагрегированные отчеты и выдает данные для отчета. 
С помощью планировщика заданий ежеминутно забирает данные о свежих маршрутах и 
обновляет отчеты. 

Актуальность отчета запаздывает на 1 минуту.

Запускается на localhost:8081

## Устновка 
```
https://github.com/AntonKruykov/alar-test.git
cd alar-test/
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
Для запуска понадобятся 2 posgresql базы даннфх с именами  alar_routes и alar_report

Для изменения названий бд или параметоров подключения можно отредактировать 
route_storage/config.yml и route_report/config.sh

## Запуск

```
./run_all.sh
```
Выполнятся все необходимые миграции, заполнятся тестовые данные, 
запустятся микросервисы и планировщик заданий.

Также можно запускть проекты по отдельности:
````
./run_storage.sh
./run_calculator.sh
./run_report.sh
./run_report_scheduler.sh
````

## Работа с пректом
### Авторизация

POST запрос на http://localhost:8080/api/auth/login
с данными
```json
{
  "username": "user0@mail.com",
  "password": "user0"
}
```
выдаст jwt токен авторизации. 

Токен нужно указывать в последющих запросах в заголовке: 

Authorization: Bearer [токен]

### Получение списка точек

http://localhost:8080/api/routes/points

Все списочные методы поддерживают limit-offset пагинацию 
http://localhost:8080/api/routes/points?limit=100&offset=200 


### Получение списка маршрутов
http://localhost:8080/api/routes/routes

### Получение детальной информации о маршруте со списком точек

http://localhost:8080/api/routes/routes/{id}

### Добавление маршрута в бд
POST запрос на http://localhost:8080/api/routes/create

Пример тела POST запроса
```json
{
    "name": "Route New",
    "items": [
        {
            "order": 0,
            "point_id": 331
        },
        {
            "order": 1,
            "point_id": 652
        },
        {
            "order": 2,
            "point_id": 558
        }
    ]
}
``` 

### Вычисление оптимального маршрута

На эндпонит http://localhost:8081/api/optimal/optimal
нужно отправить POST запрос

```json
{
    "name": "New route",
    "point_a": {
        "latitude": 730,
        "longitude": 564,
        "id": 753,
        "name": "Point 752"
    },
    "point_b": {
        "latitude": 730,
        "longitude": 564,
        "id": 753,
        "name": "Point 752"
    },
    "items": [
        {
            "point": {
                "latitude": 730,
                "longitude": 564,
                "id": 753,
                "name": "Point 752"
            }
        },
        {
            "point": {
                "latitude": 818,
                "longitude": 237,
                "id": 621,
                "name": "Point 620"
            }
        },
        {
            "point": {
                "latitude": 268,
                "longitude": 92,
                "id": 688,
                "name": "Point 687"
            }
        },
        {
            "point": {
                "latitude": 440,
                "longitude": 371,
                "id": 129,
                "name": "Point 128"
            }
        }
    ]
}
```

Вычислением оптимального маршрута занимается отдельный микросервис. 
Он сразу же вернет ответ "New route will be create soon." и запустит вычисление в фоновом режиме.
После вычисления результат запишется в базу маршрутов от имени пользователя, который инициировал запрос.

### Отчет по маршрутам

http://localhost:8082/api/report/routes