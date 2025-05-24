"""
Structured logging configuration for the Audio Generation Library.
"""

import logging
import sys
import json
from datetime import datetime
from typing import Dict, Any, Optional
from audio_api.config import get_config


class StructuredFormatter(logging.Formatter):
    """Custom formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as structured JSON."""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        # Add extra fields from record
        for key, value in record.__dict__.items():
            if key not in {
                "name",
                "msg",
                "args",
                "levelname",
                "levelno",
                "pathname",
                "filename",
                "module",
                "lineno",
                "funcName",
                "created",
                "msecs",
                "relativeCreated",
                "thread",
                "threadName",
                "processName",
                "process",
                "getMessage",
                "exc_info",
                "exc_text",
                "stack_info",
            }:
                log_entry[key] = value

        return json.dumps(log_entry, default=str)


class StandardFormatter(logging.Formatter):
    """Standard formatter for human-readable logs."""

    def __init__(self):
        super().__init__(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )


def setup_logging(config: Optional[Any] = None) -> None:
    """
    Setup logging configuration based on config settings.

    Args:
        config: Configuration instance (uses global config if None)
    """
    if config is None:
        config = get_config()

    # Get log level
    log_level = getattr(logging, config.log_level.upper(), logging.INFO)

    # Create root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)

    # Choose formatter based on config
    if config.enable_structured_logging:
        formatter = StructuredFormatter()
    else:
        formatter = StandardFormatter()

    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Set specific logger levels
    logging.getLogger("audio_api").setLevel(log_level)
    logging.getLogger("redis").setLevel(logging.WARNING)  # Reduce Redis noise
    logging.getLogger("urllib3").setLevel(logging.WARNING)  # Reduce HTTP noise

    # Log configuration
    logger = logging.getLogger(__name__)
    logger.info(
        f"Logging configured: level={config.log_level}, "
        f"structured={config.enable_structured_logging}"
    )


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.

    Args:
        name: Logger name

    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)


def log_performance(
    logger: logging.Logger, operation: str, duration: float, **kwargs
) -> None:
    """
    Log performance metrics in a structured way.

    Args:
        logger: Logger instance
        operation: Operation name
        duration: Duration in seconds
        **kwargs: Additional metrics
    """
    metrics = {
        "operation": operation,
        "duration_seconds": round(duration, 3),
        "performance_metric": True,
        **kwargs,
    }

    logger.info(f"Performance: {operation} completed in {duration:.3f}s", extra=metrics)


def log_error_with_context(
    logger: logging.Logger, error: Exception, context: Dict[str, Any]
) -> None:
    """
    Log error with additional context.

    Args:
        logger: Logger instance
        error: Exception that occurred
        context: Additional context information
    """
    error_info = {
        "error_type": type(error).__name__,
        "error_message": str(error),
        "error_context": context,
        "error_occurred": True,
    }

    logger.error(f"Error occurred: {str(error)}", extra=error_info, exc_info=True)


# Initialize logging on module import
try:
    setup_logging()
except Exception as e:
    # Fallback to basic logging if setup fails
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logging.getLogger(__name__).warning(f"Failed to setup structured logging: {e}")
