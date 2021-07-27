# Project description

## What?
Newly published articles/posts from Django blog (added on admin page) to Telegram channel.

## When?
Every defined period of time (x min) run task/-s with django-celery-beat.

## Why?
Learn how to work with Celery/Celery Beat and Telegram API.

## How?
1. Create task with @shared_task decorator for app logic in <app_name>/tasks.py
2. Create celery-beat Periodic Tasks in Django admin page.
3. Run Redis server (in Docker or system-wide): 
```shell
docker run -p 6379:6379 --name some-redis -d redis
```
4. Run Celery worker from project root (where manage.py is located): 
```shell
celery -A core_config worker -l INFO
```
5. Run Celery Beat with scheduler:
```shell
celery -A core_config beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

Bot's username: DjCeleryPosts_Bot

## How to start _local_ development?
Clone the repo. It's easy.  
Next. In application's root directory...

### Classic way:

- `pipenv install --dev`
- See NB:comments
    - in `deploy/dev/.env`
    - in `dj_posts_to_tg_project/core_config/settings/__init__.py`
- `./manage.py migrate --settings=core_config.settings.development`
- [OPTIONAL] Check that all migrations were applied
  - `./manage.py showmigrations -l`
- `./manage.py runserver 8001`

### Docker-compose way: define and run multi-container applications.

#### Manually

```shell
docker rmi -f $(docker images -f "dangling=true" -q)
python -c "import django; print(django.__path__)"
```

- Refer to `setup_scripts/dev_setup_docker.sh` for detailed description:
  - `chmod +x ./entrypoint.sh`
  - `docker-compose up --build`
  - `docker-compose exec web python manage.py makemigrations`
  - `docker-compose exec web python manage.py migrate`
  - `docker-compose exec web python manage.py createsuperuser`
- When you're done, don't forget to close down your containers
  - `docker-compose down [-v]` option `-v` to remove the volumes (and all changes in the DB) along with the containers

#### Automated flow with scripts:

1. `chmod +x ./setup-scripts/*.sh`
3. `setup_scripts/dev_setup_docker.sh`

## Build _production grade_ image
- Refer to `setup_scripts/prod_setup_docker.sh` for detailed description:
  - `$ docker-compose -f docker-compose.prod.yml build`
  - `$ docker-compose -f docker-compose.prod.yml up`
  - `$ docker-compose -f docker-compose.prod.yml exec web REQUIRED_COMMAND [REQUIRED_COMMAND ...]`

### What role of Nginx?

user <-> nginx <-> app_server <-> django