"""
1. If we want to run project locally with default db.sqlite3 >>
>> comment out DATABASE_URL variable in deploy/dev/.env

2. We can use SQLite or PostgreSQL to run tests.
    - If PostgreSQL >> run tests as usual
    - If SQLite:
        1. export ENV_ROLE="testing"
        2. review core_config/settings/testing.py for details.
3. You will switch to PostgreSQL for running tests after this =)

  File "/home/.../lib/python3.9/site-packages/django/db/backends/base/operations.py", line 176, in distinct_sql
    raise NotSupportedError('DISTINCT ON fields is not supported by this database backend')
django.db.utils.NotSupportedError: DISTINCT ON fields is not supported by this database backend
"""
import importlib
import os

from .common import *

ENV_ROLE = os.getenv('ENV_ROLE', 'development')

env_settings = importlib.import_module(f'core_config.settings.{ENV_ROLE}')

# Add to 'common envs' corresponding dev/prod variables
globals().update(vars(env_settings))
