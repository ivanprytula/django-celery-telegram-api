# Layer 0. Pull official base image
FROM python:3.9-slim-buster
LABEL maintainer="Ivan Prytula <ivanprytula87@gmail.com>"

# Set environment variables which will be used below in Dockerfile
ENV PYTONUNBUFFERED 1
# Python won't try to write .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
ENV USER pyivan

# Create the appropriate directories
ENV USERAPPHOME /usr/src/app

# Set up the app directory (Docker will create it for us)
# The WORKDIR instruction sets the working directory for any
# RUN, CMD, ENTRYPOINT, COPY and ADD instructions
# that follow it in the Dockerfile. --> /path/to/workdir
RUN mkdir $USERAPPHOME
RUN mkdir $USERAPPHOME/staticfiles
WORKDIR $USERAPPHOME


# Install psycopg2 and other dependencies
RUN apt-get update &&  \
    apt-get install -qq -y --no-install-recommends build-essential libpq-dev gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pipenv to `/usr/local/bin/pipenv`
RUN pip install --upgrade pip && pip install pipenv

# In order to launch our Python code, we must import it into our image.
# We use the keyword 'COPY' to do that.
# COPY <SRC> <DES>
# Although ADD and COPY are functionally similar,
# generally speaking, COPY is preferred.
# OR shorthand: Pipfile* [ /usr/src/...]
COPY project/Pipfile project/Pipfile.lock $USERAPPHOME/

# --system — install a Pipfile’s contents into its parent system,
# i.e. `/usr/local/lib/python3.9/site-packages/`
#--deploy — Make sure the packages are properly locked in Pipfile.lock,
# and abort if the lock file is out-of-date.
RUN pipenv install --system --deploy

# Copy project
COPY project $USERAPPHOME/

# Create and switch to a new user
RUN adduser --quiet --disabled-login --disabled-password $USER

# Set password
RUN echo "pyivan:pyivan" | chpasswd

# Chown all the files to the pyivan user
RUN chown -R $USER:$USER $USERAPPHOME

# Change to the new user
USER $USER
