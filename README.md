# FastAPI example project for DB connections

In this repo, we have a FastAPI example project that

- you can develop with Docker and docker-compose
- connects to a PostgreSQL database with SQLModel and sqlalchemy with CRUD operations examples
- connects to Redis with CRUD operations examples
- connects to S3 with CRUD operations examples
- has basic unit tests
- has a simple CI pipeline yaml file for CircleCI


## How to develop it?

Spin up docker-compose

```sh
$ docker-compose up -d --build
```

Now under `localhost:8004/docs`, you can find the APIs.

### Tests

With 

```sh
$ docker-compose exec web pytest .
```

you can run the tests and with something like

```sh
$ docker-compose exec web pytest tests/test_user.py
```

you can run specific tests, in this case for the rights endpoints of the API.

Use `docker-compose logs web` to check the logs of the FastAPI server.

To bring the docker containers down, simply run

```sh
$ docker-compose down -v
```

## Push to Docker Hub

You can use something analogous to the following to push the image to Docker Hub:

```shell
docker build -f src/Dockerfile -t scraiber/fastapi-db-example:v1.0.0 .
docker push scraiber/fastapi-db-example:v1.0.0
```

## Setup PyCharm virtual environment (for Python 3.12)

First, create a virtual environment for Python 3.12. Then run

```sh
python3.12 -m ensurepip --upgrade
python3.12 -m pip install --upgrade setuptools
```

in the terminal. After this, you can install the packages in `requirements.txt`.

