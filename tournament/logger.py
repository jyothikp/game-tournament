import json
import logging

import datetime

# Logs are send to standard output in this logger
from threading import Lock


class Logger(object):
    lock = Lock()

    def __init__(self, domain='game'):
        self.domain = domain
        self.logger = self._setup_logger()

    def _setup_logger(self):
        logger = logging.getLogger(self.domain)
        if not len(logger.handlers):
            with self.lock:
                if not len(logger.handlers):
                    logger.setLevel(logging.INFO)
                    handler = logging.StreamHandler()
                    formatter = logging.Formatter('%(message)s')
                    handler.setFormatter(formatter)
                    logger.addHandler(handler)
        return logger

    def _format_logs(self, log_tag, **kwargs):
        for each in kwargs:
            kwargs[each] = str(kwargs[each])
        kwargs['log_tag'] = log_tag
        kwargs['asctime'] = str(datetime.datetime.utcnow())
        kwargs['domain'] = self.domain
        return json.dumps(kwargs)

    def info(self, log_tag, **kwargs):
        self.logger.info(msg=self._format_logs(log_tag, **kwargs))

    def warning(self, log_tag, **kwargs):
        self.logger.warning(msg=self._format_logs(log_tag, **kwargs))

    def exception(self, log_tag, **kwargs):
        self.logger.exception(msg=self._format_logs(log_tag, **kwargs))

    def error(self, log_tag, **kwargs):
        self.logger.error(msg=self._format_logs(log_tag, **kwargs))