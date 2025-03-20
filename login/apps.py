from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver
import sqlite3  # optional

class LoginConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'login'

@receiver(post_migrate)
def set_wal_mode(sender, **kwargs):
    from django.db import connection
    if connection.vendor == 'sqlite':
        try:
            with connection.cursor() as cursor:
                cursor.execute("PRAGMA journal_mode=WAL;")
                # Optionally, print the result:
                # mode = cursor.fetchone()
                # print("SQLite WAL mode set to:", mode)
        except sqlite3.OperationalError as e:
            print("Could not set WAL mode:", e)