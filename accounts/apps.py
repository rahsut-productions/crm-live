from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'

    # for signals.py
    def ready(self):
        # accounts.signals work because of how apps
        # is set up in settings.py
        import accounts.signals