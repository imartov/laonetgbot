from celery import Celery
from service import service_send_info
import asyncio
from functools import wraps
from app import service_send_info


# app = Celery('celery_app', broker='pyamqp://guest@localhost//')
app = Celery('celery_app', broker='pyamqp://guest@rabbit//') # Docker

# app = Celery('celery_app', 'amqp://laoneuser:laonepassword@localhost:5672//')

# app = Celery('celery_app', broker='redis://localhost:6379/1')
# app = Celery('celery_app', broker='redis://redis:6379/0') # Docker
# app = Celery('celery_app', 'amqp://guest@localhost//')

app.conf.timezone = 'UTC'
app.control.purge()


@app.task
def periodic_send_info():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(service_send_info())

app.conf.beat_schedule = {
   "periodic_rask": {
      "task": "celery_app.periodic_send_info",
      "schedule": 10.0
   }
}

def main() -> None:
    pass

if __name__ == "__main__":
    main()
