from django.apps import AppConfig


class CeleryAppConfig(AppConfig):
    name = 'celery_app'

    def ready(self):
        import celery_app.signals