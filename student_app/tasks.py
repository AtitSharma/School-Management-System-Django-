from django.contrib.auth import get_user_model
from celery import shared_task
from django.core.mail import send_mail
from student_home import settings

@shared_task(bind=True)
def send_mail_func(self):
    users=get_user_model().objects.all()
    for user in users:
        mail_subject="Hi celery testing"
        message="HELLO GUYZ"
        to_email="sunilnepali844@gmail.com"
        send_mail(
            subject=mail_subject,
            message=message,
            from_email="atit.sharma694161@gmail.com",
            recipient_list=[to_email],
            fail_silently=True


        )

    return "DONE"

