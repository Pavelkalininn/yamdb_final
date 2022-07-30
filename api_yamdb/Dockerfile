FROM python:3.7-slim

WORKDIR /app

COPY ./static/redoc.yaml /app/static/
COPY requirements.txt .

RUN python -m pip install --upgrade pip && pip3 install -r ./requirements.txt --no-cache-dir

COPY .. .

CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ]


