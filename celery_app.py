import os
from celery import Celery
import asyncio
from dotenv import load_dotenv
from project.handlers.private import service_send_info

load_dotenv()

app = Celery('celery_app', broker=f'pyamqp://{os.getenv("RABBIT_USER")}@{os.getenv("RABBIT_HOST")}//')

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
