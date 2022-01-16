### Авторизация

POST запрос на http://localhost:8080/api/auth/login
с данными 
{
  "username": "user0@mail.com",
  "password": "user0"
}
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