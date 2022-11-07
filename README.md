# YaMDb project

«Reviews of works»

## Description

The project collects user reviews of the works. The works are divided into categories of books, films and music.

![Workflow](https://github.com/Pavelkalininn/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
## Technologies

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

### The project is available at http://51.250.108.40 or http://kalinin.hopto.org /, all further descriptions of requests are made on these domains (at the moment the server is disabled)
## The template for filling the env file lies at:

[infra/example.env](./infra/example.env)

## Project launch:

### To launch a project, apply migrations, create a superuser, load static and add data from fixtures to the database, respectively, you need to run the commands in the infra folder:
    
    docker-compose up -d --build
    sudo docker-compose exec web python manage.py migrate
    sudo docker-compose exec web python manage.py createsuperuser
    sudo docker-compose exec web python manage.py collectstatic --no-input
    sudo docker-compose exec web python manage.py loaddata fixtures.json

after that, the container will be assembled and launched, the admin panel is available at:

    /admin/


to stop the container, run in the infra folder:

     docker-compose down -v


## Documentation with sample requests is available at:

    /redoc/

## Self-registration of new users:

The user sends a POST request with the email and username parameters to the endpoint
   
    /api/v1/auth/signup/

The service sends an email with a confirmation code to the specified address.

The user sends a POST request with the username and confirmation_code parameters to the endpoint

    /api/v1/auth/token/

In response to the request, a token is received, which must be passed in the header of all requests with the Bearer parameter

After registering and receiving the token, the user can send a PATCH request to the endpoint.
    
    /api/v1/users/me/ 

and fill in the fields in your profile

## Creating a user by an administrator

The user can be created by the administrator — through the admin zone of the site or through a POST request for a special endpoint

    /api/v1/users/

(the description of the request fields for this case is in the documentation). At this point, the user does not need to send an email with a confirmation code.
After that, the user must independently send his email and username to the endpoint

    /api/v1/auth/signup/

in response, he should receive an email with a confirmation code.
Next, the user sends a POST request with the username and confirmation_code parameters to the endpoint

    /api/v1/auth/token/

in response to the request, he receives a token (JWT token), as with self-registration.

## Request examples

API доступен по URL

    GET..../api/v1/

Examples of API requests:

Example of a POST request with an Administrator token (Only an administrator can add and make changes to categories, reading is available to any unregistered user):

Adding a new category:

    POST .../api/v1/categories/

    {
        "name": "string",
        "slug": "string"
    }

Answer:
    
    {
        "name": "string",
        "slug": "string"
    }

Example of a POST request with an Administrator token (Only an administrator can add and make changes to genres, reading is available to any unregistered user):

Adding a genre:

    POST .../api/v1/genres/

    {
        "name": "string",
        "slug": "string"
    }

Answer:

    {
        "name": "string",
        "slug": "string"
    }

Example of a POST request with an Administrator token (Only an administrator can add and make changes to works, reading is available to any unregistered user):

Adding a work:

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

Answer:

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


Example of an unregistered user's GET request (without a token):

We get a list of all the works /genres/ categories of 5 on the page.

    GET .../api/v1/titles/
    GET .../api/v1/genres/
    GET .../api/v1/categories/

Answer (for works):
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


Authors: [__Pavel Kalinin__](https://github.com/Pavelkalininn), [__Marina Buzina__](https://github.com/Marina-ui), [__Vitaly Ostashov__](https://github.com/h0t0sh0)
