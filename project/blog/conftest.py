import pytest


@pytest.fixture(scope='session')
def celery_config():
    """Setup Celery test app configuration."""
    return {
        'broker_url': 'redis://',
        'result_backend': 'redis://'
    }


@pytest.fixture(scope='session')
def celery_parameters():
    """Setup Celery test app parameters."""
    return {
        'strict_typing': False,
    }


@pytest.fixture(scope='session')
def celery_worker_parameters():
    """Setup Celery worker parameters."""
    return {
        'queues': ('high-prio', 'low-prio'),
        'exclude_queues': ('celery'),
        "without_heartbeat": False,
    }


@pytest.fixture(scope='session')
def celery_enable_logging():
    """Enable logging in embedded workers."""
    return True


@pytest.fixture(scope='session')
def use_celery_app_trap():
    """Raise exception on falling back to default app."""
    return True
