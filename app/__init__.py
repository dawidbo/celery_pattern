from flask import Flask
from celery import Celery
import os

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

def create_app():
    app = Flask(__name__)
    
    app.config.update(
        CELERY_BROKER_URL='redis://redis:6379/0',
        CELERY_RESULT_BACKEND='redis://redis:6379/0',
        CELERYBEAT_SCHEDULE={
            'print-every-5-seconds': {
                'task': 'app.tasks.print_heartbeat',
                'schedule': 5.0,  # co 5 sekund
            },
        }
    )

    celery = make_celery(app)

    @app.route('/add/<int:a>/<int:b>')
    def add(a, b):
        result = celery.send_task('app.tasks.add_together', args=[a, b])
        return str(result)

    return app, celery
