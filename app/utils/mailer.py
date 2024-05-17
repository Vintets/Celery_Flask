#!/home/admin/venv_flask3/bin/python3

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# from email.mime.base import MIMEBase
# from email.utils import formatdate
# from email import encoders as Encoders
import json  # noqa: F401
import logging
import os
from pathlib import Path
import smtplib
import sys

from accessory import authorship, clear_console, cprint
import my_logger  # noqa: F401
from utils.ini import Ini


err_logger = logging.getLogger('error_logger')


class MyErrorsMailer():
    def errors(self, _type: str, arg: str = '') -> None:
        if _type == 'noOpen':
            err = f'13Ошибка открытия файла: {arg}'
            errlg = f'13Ошибка открытия файла: ^15_{arg}'
        elif _type == 'noSender_Name':
            err = errlg = '13Не задан отправитель'
        elif _type == 'noLoginPass':
            err = errlg = '13Не задан логин-пароль отправителя'
        elif _type == 'noToaddrFile':
            err = errlg = '13Не задано имя файла с адресатами'
        elif _type == 'noSend':
            err = errlg = '13Ошибка отправки e-mail'
        cprint(errlg)
        cprint('14-------------   ^12_ERROR   ^14_---------------')
        err_logger.error(err[2:])
        self.error = True


class Mailer(MyErrorsMailer):
    def __init__(self,
                 path_config: str = '',
                 email_sender: str = None,
                 toaddr: str = '',
                 msg_print: bool = False) -> None:
        self.path_config = Path(path_config)
        self.msg_print = msg_print
        self.email_sender = email_sender
        self.username = None
        self.password = None
        self.error = False
        self.get_login_pass()
        self.fromaddr = f'Time - teplonet.ru <{self.username}>'
        self.toaddr = self.str2list(toaddr)
        self.toaddr_test = ['kvv <kvv@domtepla.ru>']  # , 'vintets <vintets@mail.ru>']

    def get_login_pass(self) -> None:
        if self.email_sender is None:
            self.errors('noSender_Name')
            return
        ini = Ini(self.path_config / 'auth_code.ini')
        if ini.set_name_section(self.email_sender):
            self.username = ini.get_param('login')
            self.password = ini.get_param('pass')
            if self.username and self.password:
                return
        self.errors('noLoginPass')

    def str2list(self, _s: str) -> list:
        return list(map(lambda x: x.strip(), _s.split(';')))

    def read_toaddr_email_file(self, toaddr_file: str) -> bool:
        if not toaddr_file:
            self.errors('noToaddrFile')
            return False
        filename = self.path_config / toaddr_file
        self.check_read_file(filename)
        if self.error:
            return False
        with open(filename, 'r', encoding='utf-8') as fr:
            text = fr.read()
        self.toaddr = self.str2list(text)
        return True

    def check_read_file(self, __file: Path) -> None:
        if not __file.is_file():
            self.errors('noOpen', __file)

    def send_email(self, subject: str, msg_txt: str, test: bool = False) -> (list[str] | list):
        toaddr = self.toaddr
        if test:
            toaddr = self.toaddr_test

        # Заголовок         subject
        # Текст сообщения   msg_txt

        # Compose attachment
        # basename = self.filename_out.name
        # part = MIMEBase('application', 'octet-stream')
        # part.set_payload(open(self.filename_out, 'rb').read())
        # Encoders.encode_base64(part)
        # part.add_header('Content-Disposition', f'attachment; filename="{basename}"')

        # Compose message
        if self.msg_print:
            # print(json.dumps(toaddr, indent=4, ensure_ascii=False))
            toaddr_all = ',\n\t'.join(toaddr)
            print(f'\t{toaddr_all}')  # noqa: T201

        msg = MIMEMultipart()
        msg['From'] = self.fromaddr
        msg['To'] = ','.join(toaddr)
        # msg['CC'] = ', '.join(cc_emails)
        # msg['BCC'] = ', '.join(bcc_emails)
        msg['Subject'] = subject
        # msg['charset'] = 'utf-8'
        msg.attach(MIMEText(msg_txt, 'html', 'utf-8'))  # plain/html
        # msg.attach(part)

        # Send mail
        smtp = smtplib.SMTP_SSL(host='smtp.yandex.ru', port=465)
        # smtp.connect('smtp.yandex.ru', 465)
        # smtp.set_debuglevel(1);  # Выводим на консоль лог работы с сервером
        smtp.login(self.username, self.password)
        smtp.sendmail(self.fromaddr, toaddr, msg.as_string())
        smtp.quit()
        return toaddr

    def send(self, subject: str, msg_txt: str, test: bool = False) -> bool:
        if self.error:
            return False
        if self.msg_print:
            cprint('1Отправляем e-mail')
        try:
            self.send_email(subject, msg_txt, test=test)  # sended_address =
            self.__signal_send_success()
        except Exception:
            self.errors('noSend')
            return False
        return True

    def __signal_send_success(self) -> None:
        if self.msg_print:
            cprint('2Письмо успешно отправлено')


if __name__ == '__main__':
    _width = 100
    _hight = 50
    if sys.platform == 'win32':
        os.system('color 71')
        os.system(f'mode con cols={_width} lines={_hight}')
    PATH_APP = Path(__file__).parent.parent
    if str(PATH_APP) not in sys.path:  # sys.platform == 'win32'
        sys.path.insert(0, str(PATH_APP))
    os.chdir(PATH_APP)
    clear_console()

    __author__ = 'master by Vint'
    __title__ = '--- mailer ---'
    __version__ = '2.0.1'
    __copyright__ = 'Copyright 2019 (c)  bitbucket.org/Vintets'
    authorship(__author__, __title__, __version__, __copyright__, width=_width)

    email_sender    = 'email_robot_teplonet'  # noqa: E221
    # toaddr_file     = '_email_send_list_montag.txt'  # noqa: E221
    subject         = 'Тест отправки e-mail'  # noqa: E221
    html            = 'Тест Тест Тест'  # noqa: E221

    mailer = Mailer(
            path_config='configs',
            email_sender=email_sender,
            toaddr='',
            msg_print=True
            )
    # mailer.read_toaddr_email_file(toaddr_file)
    print(f'{mailer.username} {mailer.password} {mailer.toaddr}')  # noqa: T201
    status = mailer.send(subject, html, test=True)
    if not status:
        mailer.errors('noSend')

    # input('\n---------------   END   ---------------')
    print('\n---------------   END   ---------------')  # noqa: T201
