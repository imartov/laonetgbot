from celery import Celery
from celery.schedules import crontab


app = Celery('tasks', broker='pyamqp://guest@localhost//', include=['tasks'])
app.control.purge()

app.conf.timezone = 'UTC'
app.conf.beat_schedule = {
    'send_telegram_message': {
        'task': 'tasks.send_info',
        'schedule': 10,  # every 5 minutes (300 seconds)
    },
}

app.conf.update(
    result_expires=3600,
)

CELERY_IMPORTS = ("tasks", )
