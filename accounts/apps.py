from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        import accounts.signals


"""
This file is created to help the user include any application configuration for the app.
Using this, you can configure some of the attributes of the application.
From Application Configuration documentation:
    Application configuration objects store metadata for an application.
"""
