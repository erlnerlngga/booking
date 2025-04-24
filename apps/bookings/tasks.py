from huey.contrib.djhuey import task
from .methods import send_booking_email

@task()
def process_send_email_task(id: str):
    send_booking_email(id=id)