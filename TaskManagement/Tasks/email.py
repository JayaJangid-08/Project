from django.conf import settings
from django.core.mail import EmailMessage


def send_task_assignment_email(assigned_to, task, assigned_by):
    subject = "New Task Assigned"
    message = f"You have been assigned a new task: {task.title} in project {task.project.name} by {assigned_by.username}"
    email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[assigned_to.email],
            reply_to=[assigned_by.email],
        )
    email.send(fail_silently=False)


