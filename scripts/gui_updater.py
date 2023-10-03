import logging
import os
import sys
from datetime import datetime
from multiprocessing import Queue
from logging.handlers import RotatingFileHandler

class MultiProcessLogHandler(logging.Handler):

    def __init__(self, message_queue: Queue) -> None:
        logging.Handler.__init__(self)
        self.message_queue = message_queue

    def emit(self, record: logging.LogRecord) -> None:
        """Adds log to message queue"""
        msg = self.format(record)
        self.message_queue.put(msg)

    def set_logs(self):
        log_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep + os.pardir), 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        filename = os.path.join(log_dir, datetime.now().strftime('%d%m%Y_%H%M_log.log'))
        formatter = logging.Formatter(fmt='[%(asctime)s] [%(levelname)-7s] [%(funcName)-21s] %(message)s', datefmt='%d %b %Y %H:%M:%S')
        logging.getLogger().setLevel(logging.DEBUG)

        fh = RotatingFileHandler(filename=filename, maxBytes=500000, backupCount=1)
        fh.setFormatter(formatter)
        fh.setLevel(logging.DEBUG)
        logging.getLogger().addHandler(fh)

        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(formatter)
        ch.setLevel(logging.INFO)
        logging.getLogger().addHandler(ch)

        self.setFormatter(logging.Formatter(fmt='[%(asctime)s] [%(levelname)-7s] %(message)s', datefmt='%H:%M:%S'))
        self.setLevel(logging.INFO)
        logging.getLogger().addHandler(self)