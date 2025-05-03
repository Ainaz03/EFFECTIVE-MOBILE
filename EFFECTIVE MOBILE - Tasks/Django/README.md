# Dog API

REST API на Django для управления информацией о собаках и породах. Реализовано с использованием Django REST Framework и контейнеризировано с помощью Docker.

## Стек технологий

- Python 3.11
- Django 4.2.5
- Django REST Framework 3.14.0
- PostgreSQL (psycopg2-binary 2.9)
- Docker + Docker Compose
- Flake8 + python-dotenv

---

## Установка и запуск

### Клонировать репозиторий
```
git clone https://github.com/your-username/dog-api.git
```
Создать .env файл в корне проекта
```
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DATABASE_NAME=dbname
DATABASE_USER=dbuser
DATABASE_PASSWORD=pass
DATABASE_HOST=database
DATABASE_PORT=5432
```
### Применение миграций и создание суперпользователя
```
docker-compose exec web-api python manage.py migrate
docker-compose exec web-api python manage.py createsuperuser
```
## API эндпоинты
### Собаки
```
GET	/api/dogs/	Получить список собак. Включает средний возраст по породе.
GET	/api/dogs/<id>/	Получить одну собаку. Включает количество собак её породы.
POST	/api/dogs/	Добавить собаку.
PUT	/api/dogs/<id>/	Обновить собаку.
DELETE	/api/dogs/<id>/	Удалить собаку.
```
### Породы
```
GET	/api/breeds/	Получить список пород. Включает количество собак на каждую.
POST	/api/breeds/	Добавить породу.
PUT	/api/breeds/<id>/	Обновить породу.
DELETE	/api/breeds/<id>/	Удалить породу.
```

## Примеры использования API

### Собаки (`/api/dogs/`)

#### Получить список всех собак
**GET** `/api/dogs/`
```
[
  {
    "id": 1,
    "average_breed_age": 5.67,
    "name": "Булка",
    "age": 7,
    "gender": "Мальчик",
    "color": "Черно-рыжий",
    "favorite_food": "Мясо",
    "favorite_toy": "Мячик",
    "breed": 1
  },
  ...
]
```

#### Получить конкретную собаку
**GET** `/api/dogs/4/`
```
{
  "id": 4,
  "same_breed_count": 3,
  "name": "Рекс",
  "age": 4,
  "gender": "Мужской",
  "color": "Чёрный",
  "favorite_food": "Рыба",
  "favorite_toy": "Палка",
  "breed": 1
}
```

#### Создать собаку
**POST** `/api/dogs/`
```
{
  "name": "Тест",
  "age": 4,
  "gender": "Мужской/Женский",
  "color": "Чёрный",
  "favorite_food": "Тест",
  "favorite_toy": "Тест",
  "breed": 1
}
```

#### Полностью обновить собаку
**PUT** `/api/dogs/1/`
```
{
  "name": "Рекс",
  "age": 5,
  "gender": "Мужской",
  "color": "Коричневый",
  "favorite_food": "Курица",
  "favorite_toy": "Мяч",
  "breed": 2
}
```

#### Частично обновить собаку
**PATCH** `/api/dogs/1/`
```
{
  "age": 6
}
```

#### Удалить собаку
**DELETE** `/api/dogs/1/`


### Породы (`/api/breeds/`)

#### Получить все породы
**GET** `/api/breeds/`
```
[
  {
    "id": 1,
    "dogs_count": 3,
    "name": "Немецкая овчарка",
    "size": "Large",
    "friendliness": 5,
    "trainability": 4,
    "shedding_amount": 2,
    "exercise_needs": 1
  },
  ...
]
```

#### Получить конкретную породу
**GET** `/api/breeds/1/`
```
{
  "id": 1,
  "dogs_count": 3,
  "name": "Немецкая овчарка",
  "size": "Large",
  "friendliness": 5,
  "trainability": 4,
  "shedding_amount": 2,
  "exercise_needs": 1
}
```

#### Создать породу
**POST** `/api/breeds/`
```
{
  "name": "Лабрадор",
  "size": "Tiny/Small/Medium/Large",
  "friendliness": 5,
  "trainability": 5,
  "shedding_amount": 4,
  "exercise_needs": 5
}
```

#### Полностью обновить породу
**PUT** `/api/breeds/1/`
```
{
  "name": "Лабрадор",
  "size": "Large",
  "friendliness": 4,
  "trainability": 4,
  "shedding_amount": 3,
  "exercise_needs": 4
}
```

#### Частично обновить породу
**PATCH** `/api/breeds/1/`
```
{
  "friendliness": 3
}
```

#### Удалить породу
**DELETE** `/api/breeds/1/`
