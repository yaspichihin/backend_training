import smtplib
import ssl
from pathlib import Path

from PIL import Image
from pydantic import EmailStr

from app.config import settings
from app.tasks.celery import celery_app
from app.tasks.email_template import create_booking_confirmation_template


@celery_app.task
def process_pic(path: str):
    im_path = Path(path)
    im = Image.open(im_path)
    im_resized_1000_500 = im.resize((1000, 500))
    im_resized_200_100 = im.resize((200, 100))
    im_resized_1000_500.save(f"app/static/images/resized_1000_500_{im_path.name}")
    im_resized_200_100.save(f"app/static/images/resized_200_100_{im_path.name}")

# @celery_app.task # Отклчить декоратор если используем BackgroundTasks
def send_booking_confirmation_email(booking: dict, email_to: EmailStr):
    email_to_mock = settings.smtp_user  # Отправим письмо самому себе для тестирования
    msg_content = create_booking_confirmation_template(booking, email_to_mock)

    # context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(settings.smtp_host, settings.smtp_port, context=context) as server:
        server.login(settings.smtp_user, settings.smtp_password)
        server.send_message(msg_content)
