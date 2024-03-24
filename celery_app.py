'''
This module contains configurations and tasks for celery
'''

import os
import asyncio

from celery import Celery
from dotenv import load_dotenv

from sendmes.productinfo import service_send_info

load_dotenv()

app = Celery('celery_app',
             broker=f'pyamqp://{os.getenv("RABBIT_USER")}@{os.getenv("RABBIT_HOST")}//')

app.conf.timezone = 'UTC'
app.control.purge()

@app.task
def periodic_send_info():
    ''' The task is to periodically send information about the product '''
    loop = asyncio.get_event_loop()
    loop.run_until_complete(service_send_info())

app.conf.beat_schedule = {
   "periodic_rask": {
      "task": "celery_app.periodic_send_info",
      "schedule": 300.0
   }
}


if __name__ == "__main__":
    pass
