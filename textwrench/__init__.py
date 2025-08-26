"""textwrench package initializer."""

# This import configures logging as soon as the package is imported.
from .logger import logger
from .pathmgr import PathMgr

__all__ = ["logger", "PathMgr"]
