########################
# Logging Module       #
########################

import logging
import os
from pathlib import Path
from typing import Optional


class Logger:
    """
    Logger class for calculator app.

    Provides centralized logging configuration and management for the calculator,
    ensuring consistent logging across all modules.
    """

    _instance: Optional['Logger'] = None
    _logger: Optional[logging.Logger] = None

    def __new__(cls) -> 'Logger':
        """
        Implement system design pattern Singleton for our Logger.

        This ensuires only one Logger instance exists throughout the application.

        Returns:
            Logger: The singleton Logger instance.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        name: str = "calculator",
        log_file: Optional[Path] = None,
        level: int = logging.INFO
    ):
        """
        We initialize the logger with specified configuration.

        Args:
            name (str, optional): Logger name (default: "calculator").
            log_file (Optional[Path], optional): Path to log file (default: None).
            level (int, optional): Logging level (default: logging.INFO).
        """
        if Logger._logger is None:
            Logger._logger = logging.getLogger(name)
            Logger._logger.setLevel(level)

            # Remove existing handlers to prevent duplicates
            Logger._logger.handlers.clear()

            # Create formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )

            # Add console handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            Logger._logger.addHandler(console_handler)

            # Add file handler if log_file is provided
            if log_file:
                log_file.parent.mkdir(parents=True, exist_ok=True)
                file_handler = logging.FileHandler(log_file)
                file_handler.setFormatter(formatter)
                Logger._logger.addHandler(file_handler)

    @classmethod
    def get_logger(cls) -> logging.Logger:
        """
        Getter: gets the logger instance.

        Returns:
            logging.Logger: The configured logger instance.
        """
        if cls._logger is None:
            cls()
        return cls._logger

    @classmethod
    def info(cls, message: str) -> None:
        """
        Log an info-level message.

        Args:
            message (str): The message to log.
        """
        cls.get_logger().info(message)

    @classmethod
    def warning(cls, message: str) -> None:
        """
        Log a warning-level message.

        Args:
            message (str): The message to log.
        """
        cls.get_logger().warning(message)

    @classmethod
    def error(cls, message: str) -> None:
        """
        Log an error-level message.

        Args:
            message (str): The message to log.
        """
        cls.get_logger().error(message)

    @classmethod
    def debug(cls, message: str) -> None:
        """
        Log a debug-level message.

        Args:
            message (str): The message to log.
        """
        cls.get_logger().debug(message)
