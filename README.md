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

### To update the website:

```
python update.py
```

### To retrieve Google Sentiment for reviews:

```
python analyze_reviews.py
```

### Retrieving Let’s Encrypt certificate (one-time action)

- Run server in http mode
- Run `./init-letsencrypt.sh` from the project folder (outside docker)
- Add https configuration to nginx

## TODO
