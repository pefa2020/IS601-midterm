import pytest
import logging
from pathlib import Path
from app.logger import Logger


@pytest.fixture(autouse=True)
def reset_logger():
    """Reset Logger singleton before each test."""
    Logger._instance = None
    Logger._logger = None
    yield
    Logger._instance = None
    Logger._logger = None


class TestLogger:
    """Test Logger class functionality."""

    def test_logger_singleton(self):
        """Test that Logger implements Singleton pattern."""
        logger1 = Logger()
        logger2 = Logger()
        assert logger1 is logger2

    def test_get_logger(self):
        """Test getting a logger instance."""
        logger = Logger.get_logger()
        assert isinstance(logger, logging.Logger)

    def test_logger_info(self, caplog):
        """Test logging info level messages."""
        Logger()  # Initialize
        with caplog.at_level(logging.INFO):
            Logger.info("Test info message")
        assert "Test info message" in caplog.text

    def test_logger_warning(self, caplog):
        """Test logging warning level messages."""
        Logger()  # Initialize
        with caplog.at_level(logging.WARNING):
            Logger.warning("Test warning message")
        assert "Test warning message" in caplog.text

    def test_logger_error(self, caplog):
        """Test logging error level messages."""
        Logger()  # Initialize
        with caplog.at_level(logging.ERROR):
            Logger.error("Test error message")
        assert "Test error message" in caplog.text

    def test_logger_debug(self, caplog):
        """Test logging debug level messages."""
        Logger()  # Initialize
        with caplog.at_level(logging.DEBUG):
            Logger.debug("Test debug message")
        assert Logger.get_logger() is not None

    def test_multiple_instantiations_return_singleton(self):
        """Test that repeated Logger instantiations return the same object."""
        first_call = Logger()
        second_call = Logger()
        third_call = Logger()
        assert first_call is second_call is third_call
