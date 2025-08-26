"""
Filename: logger.py

Author: mg4news

Date: 2025-07-30

License: Unlicense

Description:
    Configures logging for the textwrench package.
"""

import logging
import sys

# Get a logger for the 'textwrench' package. This will be the parent logger.
logger = logging.getLogger("textwrench")

# Set the lowest-severity log message a logger will handle.
logger.setLevel(logging.INFO)

# Create a handler to send log records to the console (stdout).
console_handler = logging.StreamHandler(sys.stdout)

# Create a formatter to define the log message layout and add it to the handler.
formatter = logging.Formatter("[%(asctime)s] [%(name)s] [%(levelname)s] - %(message)s")
console_handler.setFormatter(formatter)

# Add the handler to the logger, but only if no handlers are already configured.
if not logger.handlers:
    logger.addHandler(console_handler)
