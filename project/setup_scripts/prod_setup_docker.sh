#!/bin/bash

# After some work was done which demands image re-building: build and start services again
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up

#[OPTIONAL] Database flush: if we want delete data from previous db volumes (but keep DB tables):
#docker-compose -f docker-compose.prod.yml exec web python manage.py flush --no-input`

# *** Run the commands below in new terminal window

#[OPTIONAL] Searches for one or more relative paths with the enabled finders.
#docker-compose -f docker-compose.prod.yml exec web python manage.py findstatic staticfile [staticfile ...]
# for example, ... css/base.css

docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
# Migrate command
docker-compose -f docker-compose.prod.yml exec web python manage.py makemigrations

#[OPTIONAL] Post-check whether migrations were applied successfully
#docker-compose -f docker-compose.prod.yml exec web python manage.py showmigrations -l --verbosity 2

docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# [OPTIONAL] Ensure the default Django tables were created
#docker-compose -f docker-compose.prod.yml exec db psql --username=postgres --dbname=postgres)
# postgres=# \l
# postgres=# \c postgres
# postgres=# \dt
# postgres=# \q

#Create superuser
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
