"""
Main idea of such configuration is to use default "python manage.py runserver"
in 'production mode by default' (BUT on local machine) without need of
changing manage.py

If you have development.py then try/except will handle settings "swapping"
"""
import importlib
import os

from .common import *

ENV_ROLE = os.getenv('ENV_ROLE', 'development')

env_settings = importlib.import_module(f'core_config.settings.{ENV_ROLE}')

# Add to 'common envs' corresponding dev/prod variables
globals().update(vars(env_settings))
