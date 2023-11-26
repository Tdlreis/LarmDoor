from django.apps import AppConfig


class MqttConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mqtt'

    def ready(self):
        from .mqtt import start_mqtt_handler

        # Start the MQTT handler when the Django application is ready
        start_mqtt_handler()