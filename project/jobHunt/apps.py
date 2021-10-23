from django.apps import AppConfig


class JobhuntConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jobHunt'
    # def ready(self):
    #     from webScrapping import updater
    #     updater.start()