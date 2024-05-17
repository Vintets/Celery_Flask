import random
import time

from app import app as flask_app, celery_app
from celery import shared_task
from utils.mailer import Mailer


@shared_task(ignore_result=False)
def background_task_email(email: str) -> None:
    send_email()


def send_email() -> None:
    with flask_app.app_context():
        subject = 'Тест отправки e-mail'
        html = 'Тест Тест Тест'
        mailer = Mailer(
                        path_config='configs',
                        email_sender='email_robot_teplonet',
                        toaddr='',
                        msg_print=True
                        )
        mailer.read_toaddr_email_file('_email_send_admin.txt')
        status = mailer.send(subject, html, test=False)
        if not status:
            mailer.errors('noSend')


@celery_app.task
def update_products_task(discount_obj) -> None:
    with flask_app.app_context():
        discount_obj.update_products()


@celery_app.task(bind=True, serializer='json')
def long_task(self):
    """Background task that runs a long function with progress reports."""

    verb = ['Запуск', 'Загрузка', 'Восстановление', 'Проверка']
    adjective = ['главный', 'излучающий', 'тихий', 'гармоничный', 'быстрый']
    noun = ['солнечная батарея', 'преобразователь частиц', 'космические лучи', 'орбитальный аппарат', 'бит']
    # verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking']
    # adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast']
    # noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit']
    message = ''
    total = random.randint(20, 30)
    for i in range(total):
        if not message or random.random() < 0.25:
            message = '{0} {1} {2}...'.format(random.choice(verb),
                                              random.choice(adjective),
                                              random.choice(noun))
        self.update_state(state='PROGRESS',
                          meta={'current': i, 'total': total, 'status': message})
        time.sleep(0.3)
    return {'current': 100, 'total': 100, 'status': 'Task completed!', 'result': total}
