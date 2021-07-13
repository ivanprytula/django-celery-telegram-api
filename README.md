# Project description

## What?
Newly published articles/posts from Django blog to Telegram channel.

## When?
Every defined period of time (x min) run task/-s with django-celery-beat.

## Why?
Learn how to work with Celery/Celery Beat and Telegram API.


"Modus operandi":
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