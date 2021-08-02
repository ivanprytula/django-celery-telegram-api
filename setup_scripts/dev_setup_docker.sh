#!/bin/bash

# Step 1. Login locally into a Docker registry/hub

# Build & Run: separate commands
#docker-compose build
#docker-compose up
# OR with one-liner
docker-compose up --build
# If some work was done which demands image re-building: build and start services again

#[OPTIONAL] Database flush: if we want delete data from previous db volumes (but keep DB tables):
#docker-compose exec web python manage.py flush --no-input

# Migrate command
docker-compose exec web python manage.py migrate

#[OPTIONAL] Post-check whether migrations were applied successfully
#docker-compose exec web python manage.py showmigrations -l --verbosity 2

# [OPTIONAL] Ensure the default Django tables were created
#docker-compose exec db psql --username=<user_name> --dbname=<your_db_name>
# postgres=# \l
# postgres=# \c <your_db_name>
# postgres=# \dt
# postgres=# \q

#Create superuser
docker-compose exec web python manage.py createsuperuser
