# Проект YaMDb

«Отзывы на произведения»

## Описание

Проект собирает отзывы пользователей на произведения. Произведения делятся на категории книги, фильмы и музыка.

## Технологии

    asgiref==3.2.10
    requests==2.26.0
    django==2.2.16
    djangorestframework==3.12.4
    djangorestframework-simplejwt==4.7.2
    gunicorn==20.0.4
    psycopg2-binary==2.8.6
    PyJWT==2.1.0
    django-filter~=21.1
    pytz==2020.1
    sqlparse==0.3.1

## Шаблон наполнения env-файла лежит по адресу: 

[infra/example.env](./infra/example.env)

## Запуск проекта:

### Для запуска проекта, применения миграций, создания суперюзера, загрузки статики и добавления в БД данных из фикстур соответственно необходимо в папке infra выполнить команды:
    
    docker-compose up -d --build
    docker-compose exec web python manage.py migrate
    docker-compose exec web python manage.py createsuperuser
    docker-compose exec web python manage.py collectstatic --no-input
    docker-compose exec web python manage.py loaddata fixtures.json

после чего будет собран и запущен контейнер, админка доступна по адресу:  

[http://localhost/admin/](http://localhost/admin/)


для остановки контейнера необходимо в папке infra выполнить:

     docker-compose down -v


## Документация с примерами запросов доступна по адресу:

    http://localhost/redoc/

## Самостоятельная регистрация новых пользователей:

Пользователь отправляет POST-запрос с параметрами email  и username на эндпоинт
   
    /api/v1/auth/signup/

Сервис отправляет письмо с кодом подтверждения на указанный адрес.

Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт

    /api/v1/auth/token/

В ответ на запрос приходит токен, который необходимо передавать в заголовке всех запросов с параметром Bearer

После регистрации и получения токена пользователь может отправить PATCH-запрос на эндпоинт
    
    /api/v1/users/me/ 

и заполнить поля в своём профайле

## Создание пользователя администратором

Пользователя может создать администратор — через админ-зону сайта или через POST-запрос на специальный эндпоинт 

    api/v1/users/

(описание полей запроса для этого случая — в документации). В этот момент письмо с кодом подтверждения пользователю отправлять не нужно.
После этого пользователь должен самостоятельно отправить свой email и username на эндпоинт

    /api/v1/auth/signup/

в ответ ему должно прийти письмо с кодом подтверждения.
Далее пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт 

    /api/v1/auth/token/

в ответе на запрос ему приходит token (JWT-токен), как и при самостоятельной регистрации.

## Примеры запросов


Сам API доступен по адресу

    GET..../api/v1/

Примеры запросов к API:

Пример POST-запроса с токеном Администратора (Добавлять и вносить изменения в категории может только администратор, чтение доступно любому незарегистрированному пользователю): 

Добавление новой категории:

    POST .../api/v1/categories/

    {
        "name": "string",
        "slug": "string"
    }

Ответ:
    
    {
        "name": "string",
        "slug": "string"
    }

Пример POST-запроса с токеном Администратора (Добавлять и вносить изменения в жанры может только администратор, чтение доступно любому незарегистрированному пользователю): 

Добавление жанра:

    POST .../api/v1/genres/

    {
        "name": "string",
        "slug": "string"
    }

Ответ:

    {
        "name": "string",
        "slug": "string"
    }

Пример POST-запроса с токеном Администратора (Добавлять и вносить изменения в произведения может только администратор, чтение доступно любому незарегистрированному пользователю): 

Добавление произведения:

    POST .../api/v1/titles/

    {
        "name": "string",
        "year": 0,
        "description": "string",
        "genre": 
            [
                "string"
            ],
        "category": "string"
    }

Ответ:

    {
        "id": 0,
        "name": "string",
        "year": 0,
        "rating": 0,
        "description": "string",
        "genre":
            [
                {
                    "name": "string",
                    "slug": "string"
                }
            ],
        "category":
            {
                "name": "string",
                "slug": "string"
            }
    }


Пример GET-запроса незарегистрированного пользователя (без токена):

Получаем список всех произведений/жанров/категорий по 5 на странице.

    GET .../api/v1/titles/
    GET .../api/v1/genres/
    GET .../api/v1/categories/

Ответ (для произведений):

    [
        {
            "count": 0,
            "next": "string",
            "previous": "string",
            "results":
                [
                    {
                        "id": 0,
                        "name": "string",
                        "year": 0,
                        "rating": 0,
                        "description": "string",
                        "genre":
                            [
                                {
                                    "name": "string",
                                    "slug": "string"
                                }
                            ],
                        "category":
                            {
                                "name": "string",
                                "slug": "string"
                            }
                    }
                ]
        }

    ]
    


Авторы: [__Паша Калинин__](https://github.com/Pavelkalininn), [__Марина Бузина__](https://github.com/Marina-ui), [__Виталий Осташов__](https://github.com/h0t0sh0)
