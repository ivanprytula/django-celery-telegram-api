"""
1. If we want to run project locally with default db.sqlite3 >>
>> comment out DATABASE_URL variable in deploy/dev/.env

2. We can use SQLite or PostgreSQL to run tests.
    - If PostgreSQL >> run tests as usual
    - If SQLite:
        - don't add/use testing/.env
"""
import importlib
import os
import sys

from .common import *

ENV_ROLE = os.getenv('ENV_ROLE', 'development')

env_settings = importlib.import_module(f'core_config.settings.{ENV_ROLE}')

# Add to 'common envs' corresponding dev/prod variables
globals().update(vars(env_settings))

AutoConfig = globals().get('AutoConfig')
ENV_BASE_DIR = globals().get('ENV_BASE_DIR')
dj_database_url = globals().get('dj_database_url')

if 'test' in sys.argv or 'test_coverage' in sys.argv:
    config = AutoConfig(search_path=ENV_BASE_DIR / 'deploy/testing/.env')

    # Option Zero. Don't use this file and run tests with dev/.env file >> easiest option :)
    # Creating test database for alias 'default' ('test_<your_regular_db_name>')...

    # Option 1. Need to provide separate testing/.env file
    DATABASES = {
        'default': config(
            'DATABASE_URL',
            default=f'sqlite:///{str(BASE_DIR)}/db.sqlite3',
            cast=dj_database_url.parse
        )
    }

    # Option 2. "Old-school" style with classic dictionary values (i.g. w/o using dj_database_url)
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.postgresql',
    #         'NAME': 'postgres' or <your_db_name>,
    #         'HOST': 'localhost',
    #         'USER': '<user_name>',
    #         'PASSWORD': '<pass_word>',
    #         'POST': 5432,
    #     }
    # }
    # pass
