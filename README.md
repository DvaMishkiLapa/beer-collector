# beer-collector

Cервис на Python (3.9+) с использованием [Sanic](https://sanic.readthedocs.io/en/stable/) для работы с [пивом](https://random-data-api.com/api/beer/random_beer) :)

## Содержание

- [beer-collector](#beer-collector)
  - [Содержание](#содержание)
    - [1. Запуск сервиса](#1-запуск-сервиса)
    - [2. Используемые инструменты](#2-используемые-инструменты)
    - [3. Реализованное API](#3-реализованное-api)
      - [3.1 `GET ​/get_new_beers`](#31-get-get_new_beers)
      - [3.2 `GET ​/stats`](#32-get-stats)

### 1. Запуск сервиса

Для запуска сервиса необходим установленный [Docker](https://docs.docker.com/engine/install/) и [Docker-compose](https://docs.docker.com/compose/install/).

Команда запуска сервиса:

```bash
docker-compose up
```

Команда запуска сервиса в фоновом режиме:

```bash
docker-compose up -d
```

После запуска работу сервиса можно проверить, открыв в браузере <http://127.0.0.1:8000/swagger/>.

### 2. Используемые инструменты

Сервис работает с использованием [Sanic](https://sanic.readthedocs.io/en/stable/).

Для сбора метрик используется [Prometheus Python Client](https://github.com/prometheus/client_python).

Возможность тестового взаимодействия с API реализованно через [Swagger](https://swagger.io/) с помощью [Sanic OpenAPI 3](https://sanic-openapi.readthedocs.io/en/stable/sanic_openapi3/index.html).

### 3. Реализованное API

#### 3.1 `GET ​/get_new_beers`

Метод выгружает асинхронно 5 новых сортов пива с ресурса <https://random-data-api.com/api/beer/random_beer>, выдает ответ в виде JSON с полями `brand`, `name` и `alcohol`.

#### 3.2 `GET ​/stats`

Метод показывает сколько запросов было на сервер (с момента запуска).
