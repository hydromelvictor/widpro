#!/usr/bin/env python3
"""
logging module
"""
import logging
import os


class Logger:
    """
    logging class
    """

    def __init__(self, name: str, level: int = logging.INFO):
        """
        init
        """
        assert type(name) is str, 'name must be str'
        self.name = name

        assert type(level) is int, 'level must be int'
        self.level = level

        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(self.level)

        self.formatter = logging.Formatter(
            "%(asctime)s :: %(name)s :: %(levelname)s :: file %(filename)s\
                :: %(funcName)s :: line %(lineno)d :: %(message)s"
        )

        # file handler

        log_file_path = os.path.join(os.getcwd(), '{}.log'.format(self.name))

        self.file_handler = logging.FileHandler(log_file_path, mode='a')
        self.file_handler.setLevel(self.level)
        self.file_handler.setFormatter(self.formatter)

        self.logger.addHandler(self.file_handler)

        # stream handler
        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setLevel(self.level)
        self.stream_handler.setFormatter(self.formatter)

        self.logger.addHandler(self.stream_handler)

    def info(self, message: str):
        """
        info
        """
        assert type(message) is str, 'message must be str'
        self.logger.info(message)

    def debug(self, message: str):
        """
        debug
        """
        assert type(message) is str, 'message must be str'
        self.logger.debug(message)

    def warning(self, message: str):
        """
        warning
        """
        assert type(message) is str, 'message must be str'
        self.logger.warning(message)

    def error(self, message: str):
        """
        error
        """
        assert type(message) is str, 'message must be str'
        self.logger.error(message)

    def critical(self, message: str):
        """
        critical
        """
        assert type(message) is str, 'message must be str'
        self.logger.critical(message)

    def close(self):
        """Close file and stream handlers"""
        for handler in self.logger.handlers:
            handler.close()
