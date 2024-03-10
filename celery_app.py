from threading import Thread
from celery import Celery
from datetime import timedelta
from redbeat import RedBeatSchedulerEntry
from service import service_send_info
import asyncio
from functools import wraps
from asyncio.proactor_events import _ProactorBasePipeTransport
from app import service_send_info
import platform


app = Celery('celery_app', broker='pyamqp://guest@localhost//')
# app = Celery('celery_app', broker='redis://localhost:6379/1')
app.conf.timezone = 'UTC'
app.control.purge()

@app.task
def periodic_send_info():
    # if platform.system()=='Windows':
    #     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # loop = asyncio.new_event_loop()
    # loop = asyncio.set_event_loop(asyncio.new_event_loop())
    # loop.run_until_complete(service_send_info())
    asyncio.get_event_loop().run_until_complete(service_send_info())
    asyncio.run(service_send_info())


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
