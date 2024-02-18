from celery import shared_task
import time  



@shared_task
def test():
    for x in range(10):
        print(x)
        time.sleep(1)