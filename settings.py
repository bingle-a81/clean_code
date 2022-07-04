# -*- coding: utf-8 -*-
import logging
from logging import StreamHandler, Formatter, LogRecord
import smtplib
import telebot
from configparser import ConfigParser
import os

base_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(base_path, "set.ini")
# проверка наличия файла настоек
if os.path.exists(config_path):
    cfg = ConfigParser()
    cfg.read(config_path, encoding='utf-8')
else:
    print("Конфигурация не найдена!")

SERVER = cfg.get("smtp", "server")
PORT = cfg.get("smtp", "port")
EMAIL = cfg.get("smtp", "email")
PASSWD = cfg.get("smtp", "passwd")

CHAT_ID = cfg.get("telega", "chat_id")
TOKEN = cfg.get("telega", "token")


class TelegramBotHandler(logging.Handler):
    def __init__(self, token: str, chat_id: str):
        super().__init__()
        self.token = token
        self.chat_id = chat_id

    def emit(self, record: LogRecord):
        message = self.format(record)
        bot = telebot.TeleBot(self.token)
        try:
            bot.send_message(self.chat_id, message)
        except:
            pass


class MegaHandler(logging.Handler):
    def __init__(self, filename):
        logging.Handler.__init__(self)
        self.filename = filename

    def emit(self, record):
        message = self.format(record)
        with open(self.filename, 'a') as file:
            file.write(message + '\n')


class MegaEmail(logging.Handler):
    def __init__(self, server, port, email, passwd):
        logging.Handler.__init__(self)
        self.server = server
        self.port = port
        self.email = email
        self.passwd = passwd

    def emit(self, record: LogRecord):
        message = self.format(record)
        charset = f'Content-Type: text/plain; charset=utf-8'
        mime = 'MIME-Version: 1.0'
        body = "\r\n".join((f"From: {self.email}", f"To: {self.email}",
                            f"Subject: File log debug.log ", mime, charset, "", message))
        # формируем тело письма
        try:
            # подключаемся к почтовому сервису
            smtp = smtplib.SMTP(self.server, self.port)
            smtp.starttls()
            smtp.ehlo()
            # логинимся на почтовом сервере
            smtp.login(self.email, self.passwd)
            # пробуем послать письмо
            smtp.sendmail(self.email, self.email, body.encode('utf-8'))
        except smtplib.SMTPException as err:
            print('Что - то пошло не так...')
            raise err
        finally:
            smtp.quit()


logger_config = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'std_format': {
            'format': '{asctime} - {levelname} - {name} - {message}',
            'style': '{'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'std_format',
            # 'filters': ['new_filter'],
        },
        'file': {
            '()': MegaHandler,
            'level': 'INFO',
            'filename': 'debug.log',
            'formatter': 'std_format',
        },
        'email': {
            '()': MegaEmail,
            'level': 'ERROR',
            'server': SERVER,
            'port': PORT,
            'email': EMAIL,
            'passwd': PASSWD,
            'formatter': 'std_format',
        },
        'telegram_handler': {
            '()': TelegramBotHandler,
            'level': 'WARNING',
            'chat_id': CHAT_ID,
            'token': TOKEN,
            'formatter': 'std_format',
        }

    },
    'loggers': {
        'app_logger': {
            'level': 'DEBUG',
            'handlers': ['console', 'file', 'telegram_handler','email'],
            # 'propagate': False
        },
        'telega_logger': {
            'level': 'DEBUG',
            # 'handlers': ['telegram_handler'],
        },
        'email_logger': {
            'level': 'DEBUG',
            # 'handlers': ['email'],
        }

    },
}
