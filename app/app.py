#!/home/admin/venv_flask3/bin/python3

from celery import Celery
from configs import celeryconfig
from configs.config import Configuration as Conf
from flask import Flask

app = Flask(__name__)
app.config.from_object(Conf)

# celery_app = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery_app = Celery(app.name)
celery_app.config_from_object(celeryconfig)
celery_app.set_default()
