class DjangoChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Django-Chat'

    def ready(self):
        import Django_Chat.signals  # Adjust path if necessary
