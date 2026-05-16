from django.apps import AppConfig


class KappConfig(AppConfig):
    name = 'kapp'

    def ready(self):
        import kapp.signals  # noqa