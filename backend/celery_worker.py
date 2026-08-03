from celery import Celery, Task
from app import app

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["tasks"]
)


class FlaskTask(Task):

    def __call__(self, *args, **kwargs):

        with app.app_context():
            return self.run(*args, **kwargs)


celery_app.Task = FlaskTask