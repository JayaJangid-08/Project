from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Task
from .email import send_task_assignment_email

@receiver(m2m_changed, sender=Task.assigned_to.through)
def send_email_on_assignment(sender, instance, action, pk_set, **kwargs):
    # Only when users are added
    if action == "post_add":
        users = instance.assigned_to.filter(id__in=pk_set)

        for user in users:
            print("EMAIL TRIGGERED")  # debug

            send_task_assignment_email(
                assigned_to= user,
                task= instance,
                assigned_by= instance.created_by, 
            )
