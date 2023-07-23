from time import sleep
from django.core.mail import send_mail
from celery import shared_task


@shared_task()
def send_feedback_message_task(email, subject, text):
	"""
	This task is performed by celery worker
	ever time the user sends a new feedback.
	"""
	sleep(10)
	send_mail(
			subject=subject,
			message=f"{text}\n Thank you for your feedback!",
			from_email="super-recipes.com",
			recipient_list=[email],
			fail_silently=False,
		)
