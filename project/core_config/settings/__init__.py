"""/home/iprytul
Main idea of such configuration is to use default "python manage.py runserver"
in 'production mode by default' (BUT on local machine) without need of
changing manage.py

If you have development.py then try/except will handle settings "swapping"
"""
import sys

from .common import *
from .production import *

# On production server remove dev settings file or don't push it to the branch
# which will be used for production [staging] deployment
try:
    from .development import *
except ImportError:
    sys.exc_info()
