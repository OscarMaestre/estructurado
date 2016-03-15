from django.apps import AppConfig


class ModeladoBdConfig(AppConfig):
    name = 'modelado_bd'
    
    def ready(self):
        import signal