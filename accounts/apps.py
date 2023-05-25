from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    # ready function is responsible for making the singls works
    def readt(self):
        import accounts.signals
