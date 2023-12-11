from django.apps import AppConfig


class SerialmonitorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'serialMonitor'

    def ready(self):
        from .serial import start_serial_handler

        # Start the MQTT handler when the Django application is ready
        start_serial_handler()