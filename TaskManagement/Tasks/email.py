from django.conf import settings
from django.core.mail import EmailMessage
from celery import shared_task


@shared_task
def send_task_assignment_email(assigned_to, task, assigned_by):
    subject = "New Task Assigned"
    message = f"You have been assigned a new task: {task.title} in project {task.project.name} by {assigned_by.username}"
    email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[assigned_to.email],
            )
    
    try:
        email.send(fail_silently=False)
        print("EMAIL SENT to", assigned_to.email)
        return True
    
    except Exception as e:
        print("EMAIL FAILED", e)
        return False


