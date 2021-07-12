from celery import shared_task


@shared_task
def add(x_var, y_var):
    return x_var + y_var
