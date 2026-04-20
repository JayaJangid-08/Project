from django.apps import AppConfig


class TasksConfig(AppConfig):
    name = 'Tasks'
    def ready(self):
        # Import signals to connect them
        from . import signals