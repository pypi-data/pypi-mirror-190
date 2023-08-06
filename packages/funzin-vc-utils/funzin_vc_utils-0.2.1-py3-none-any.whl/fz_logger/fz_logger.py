import logging
import os
import sys
from logging import handlers

import colorlog


class Logger:
    def __init__(self, className, lvl, filePath=None):
        if filePath is None:
            self.filePath = "./log"
        else:
            self.filePath = filePath
        os.makedirs(self.filePath, exist_ok=True)

        self.settings = {
            "LEVEL": self.logger_LUT(lvl),
            "FILENAME": className,
            "MAYBYTES": 15 * 1024 * 1024,
            "BACKUPCOUNT": 100,
            "FORMAT": "%(log_color)s[%(levelname)-8s]%(reset)s <%(name)s>: %(module)s:%(lineno)d:  %(message)s",
        }

    def logger_LUT(self, idx):
        logger_Level = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }

        return logger_Level.get(idx, "INFO")

    def initLogger(self):
        __logger = logging.getLogger(self.settings["FILENAME"])
        if len(__logger.handlers) > 0:
            return __logger
        streamFormatter = colorlog.ColoredFormatter(
            "%(log_color)s[%(levelname)-8s]%(reset)s <%(name)s>: %(module)s:%(lineno)d:  %(message)s"
        )
        fileFormatter = logging.Formatter(
            "%(asctime)s [%(levelname)-8s] <%(name)s>: %(module)s:%(lineno)d: %(message)s"
        )

        streamHandler = colorlog.StreamHandler(sys.stdout)

        fileHandler = handlers.TimedRotatingFileHandler(
            os.path.abspath("{}/{}.log".format(self.filePath, self.settings["FILENAME"])),
            when="midnight",
            interval=1,
            backupCount=self.settings["BACKUPCOUNT"],
            encoding="utf-8",
        )
        streamHandler.setFormatter(streamFormatter)
        fileHandler.setFormatter(fileFormatter)

        __logger.addHandler(streamHandler)
        __logger.addHandler(fileHandler)

        __logger.setLevel(self.settings["LEVEL"])

        return __logger
