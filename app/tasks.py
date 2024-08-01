from .celery import celery

@celery.task(name='app.tasks.add_together')
def add_together(a, b):
    return a + b

@celery.task(name='app.tasks.print_heartbeat')
def print_heartbeat():
    print("hello heartbeat")
