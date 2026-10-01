import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mini_store.settings")

app = Celery("mini_store")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
