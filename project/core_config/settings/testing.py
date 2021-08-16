""""
For latter two options either in container or regular setup in virtual environment:
    - You need to override dev/.env settings with default(postgres user/db) or create local database
      (custom db_user/db_name/db_password).
"""
import sys

from .development import *

config = AutoConfig(search_path=ENV_BASE_DIR / 'deploy/testing/.env')

if 'test' in sys.argv or 'test_coverage' in sys.argv:

    # Option Zero. Don't use this file and run tests with dev/.env file >> easiest option :)
    # Creating test database for alias 'default' ('test_<your_regular_db_name>')...

    # Option 1. Need to provide separate testing/.env file
    # DATABASES = {
    #     'default': config(
    #         'DATABASE_URL',
    #         default=f'sqlite:///{str(BASE_DIR)}/db.sqlite3',
    #         cast=dj_database_url.parse
    #     )
    # }

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
    pass
