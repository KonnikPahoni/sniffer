# Sniffer

Currently, collects the following data:

- Bitfinex tickers

## Deployment

### Install Docker and Docker Compose

### Populate .env file

```
cp .env.dist .env
```

### Build and run containers

```
docker-compose build && docker-compose up
```

## App updating

### Connect to the docker container

```
docker container exec -it sniffer_app /bin/bash
```

### To apply migrations:

```
python3 manage.py migrate
```

### To collect static files:

```
python manage.py collectstatic
```

### To purge the queue:

```
docker container exec -it sniffer_celery celery -A celery purge -f
```

### TODO:

- Cex tickers https://cex.io/api/tickers/USD
- Trip reports parsing