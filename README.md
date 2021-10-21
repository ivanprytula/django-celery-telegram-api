# Table of Contents
1. [Short project description](#project-decription)
2. [Tech stack (dockerized)](#tech-stack)
3. [Project setup](#project-setup)
   1. [Dev/local](#project-setup-local)
   2. [Production grade](#project-setup-prod)
4. [TODOs](#to-dos)


---
**Handy commands:**

## General
```shell
chmod +x ./setup-scripts/*.sh
cat /etc/*-release


```

## Docker related
```shell
# Activate rootless client:
# 1. To specify the socket path using $DOCKER_HOST:
export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/docker.sock
 # example: docker run -d -p 8080:80 nginx
# 2. To specify the CLI context using docker context:
docker context use rootless
# example: docker run -d -p 8080:80 nginx

docker rmi -f $(docker images -f "dangling=true" -q)
docker-compose exec --user root web python manage.py makemigrations
# apt-get install sudo -y
docker-compose exec --user root web coverage run --source='.' manage.py test  blog/ -v 3 --timing
docker-compose exec web python manage.py test blog/ --force-color --timing


```

## PostgreSQL related
```shell
# How to check if Postgres is running? ver.1
pgrep -u postgres -fa -- -D
# OUTPUT:
# 69612 /usr/lib/postgresql/13/bin/postgres -D /var/lib/postgresql/13/main -c config_file=/etc/postgresql/13/main/postgresql.conf

# ver.2
service postgresql status

# Find PostgreSQL location
sudo find /usr -wholename '*/bin/postgres'
# OUTPUT: /usr/lib/postgresql/13/bin/postgres

# Find your post
sudo sed -n 4p <$PGDATA>/postmaster.pid
sudo sed -n 4p /var/lib/postgresql/13/main/postmaster.pid

# Run PostgreSQL client:
sudo -u postgres psql

pg_lsclusters
# Ver Cluster Port Status Owner    Data directory              Log file
13  main    5432 online postgres /var/lib/postgresql/13/main /var/log/postgresql/postgresql-13-main.log

```

## Python related
```shell
python -c "import django; print(django.__path__)"
# After new package was installed >> turn off VPN (if any) >> rebuild image
pylint --ignore=migrations --load-plugins=pylint_django --django-settings-module=core_config.settings project/
flake8 project/
python -Wa manage.py test
python3.9 -m webbrowser -t "https://www.python.org"
coverage run --source='.' manage.py test accounts/ -v 3 --timing
```

```python
import keyword
print(keyword.kwlist)
```

---


# <a id="project-decription">Short project description</a>
## What?
Newly published articles/posts from Django blog to Telegram channel.

## When?
Every defined period of time (x min) run task/-s with celery-beat.

## Why?
Learn how to work with task queue/periodic tasks and Telegram API.

Bot's username: DjCeleryPosts_Bot

# <a id="tech-stack">Tech Stack(dockerized)</a>
- Python 3.9.6
- Django 3.2.5
- PostgreSQL 13.3 | latest
- Celery & celery beat & Flower
- Redis 6.2.5 | latest
- Telegram API (bot for channel management)
- Extras for production grade:
  - Gunicorn ~=20.1
  - Nginx 1.21.1-alpine


# <a id="project-setup">Project setup</a>

## <a id="project-setup-local">Dev/local</a>
Clone the repo. It's easy.
Next. In root directory...

### docker-compose way: build and run multi-container applications.

#### Manually

- Refer to [setup_scripts/dev_setup_docker.sh](./setup_scripts/dev_setup_docker.sh) for detailed description:
  - `docker-compose up --build`
  - `docker-compose exec web python manage.py migrate`
  - `docker-compose exec web python manage.py createsuperuser`
- When you're done, don't forget to close down your containers
  - `docker-compose down [-v]` option `-v` to remove the volumes (and all changes in the DB) along with the containers

#### Automated flow with scripts:

1. `chmod +x ./setup-scripts/*.sh`
3. `setup_scripts/dev_setup_docker.sh`


## <a id="project-setup-prod">Production grade</a>
- Refer to `setup_scripts/prod_setup_docker.sh` for detailed description:
  - `$ docker-compose -f docker-compose.prod.yml up --build`
  - `$ docker-compose -f docker-compose.prod.yml exec web REQUIRED_COMMAND [REQUIRED_COMMAND ...]`


# <a id="to-dos">TODOs</a>
### What role of Nginx?

user <-> nginx <-> app_server <-> django
