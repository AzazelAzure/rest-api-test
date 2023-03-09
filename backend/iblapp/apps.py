from django.apps import AppConfig


class IblappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "iblapp"

    def read(self):
        import iblapp.signals
