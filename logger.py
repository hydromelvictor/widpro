#!/usr/bin/env python3
"""
Logging module to manage loggers for applications.
"""
import logging
import os


class Logger:
    """
    A class for managing logging configurations with both
    file and console output.
    """

    def __init__(self, name: str, level: int = logging.INFO):
        """
        Initialize the Logger with a name and logging level.

        :param name: The name of the logger, used to identify logs.
        :param level: The logging level (default is INFO).
        :raises ValueError: If name is not a string or level is not an integer.
        """
        if not isinstance(name, str):
            raise ValueError('name must be str')
        self.name = name

        if not isinstance(level, int):
            raise ValueError('level must be int')
        self.level = level

        self.logger = logging.getLogger(self.name)
        if not self.logger.handlers:
            self.logger.setLevel(self.level)

            self.formatter = logging.Formatter(
                "%(asctime)s :: %(name)s :: %(levelname)s ::\
                    file %(filename)s :: %(funcName)s ::\
                        line %(lineno)d :: %(message)s"
            )

            log_dir = os.environ.get('LOG_DIR', os.getcwd())
            log_file_path = os.path.join(log_dir, f'{self.name}.log')

            self.file_handler = logging.FileHandler(log_file_path, mode='a')
            self.file_handler.setLevel(self.level)
            self.file_handler.setFormatter(self.formatter)
            self.logger.addHandler(self.file_handler)

            self.stream_handler = logging.StreamHandler()
            self.stream_handler.setLevel(self.level)
            self.stream_handler.setFormatter(self.formatter)
            self.logger.addHandler(self.stream_handler)

    def log_info(self, message: str):
        """
        Log an info message.

        :param message: The message to log.
        :raises ValueError: If message is not a string.
        """
        if not isinstance(message, str):
            raise ValueError('message must be str')
        self.logger.info(message)

    def log_debug(self, message: str):
        """
        Log a debug message.

        :param message: The message to log.
        :raises ValueError: If message is not a string.
        """
        if not isinstance(message, str):
            raise ValueError('message must be str')
        self.logger.debug(message)

    def log_warning(self, message: str):
        """
        Log a warning message.

        :param message: The message to log.
        :raises ValueError: If message is not a string.
        """
        if not isinstance(message, str):
            raise ValueError('message must be str')
        self.logger.warning(message)

    def log_error(self, message: str):
        """
        Log an error message.

        :param message: The message to log.
        :raises ValueError: If message is not a string.
        """
        if not isinstance(message, str):
            raise ValueError('message must be str')
        self.logger.error(message)

    def log_critical(self, message: str):
        """
        Log a critical message.

        :param message: The message to log.
        :raises ValueError: If message is not a string.
        """
        if not isinstance(message, str):
            raise ValueError('message must be str')
        self.logger.critical(message)

    def close(self):
        """Close all handlers associated with this logger."""
        for handler in self.logger.handlers[:]:
            handler.close()
            self.logger.removeHandler(handler)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
