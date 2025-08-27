"""
Filename: pathmgr.py

Author: mg4news

Date: 2025-07-30

License: Unlicense

Description:
    A persistance class for managing text files in a given path. Opens, closes, writes, etc. Extraxts text data in
    the various formats required by the textwrench library. Created for convenience
    and reuse
"""

import logging
from pathlib import Path
from typing import List


class PathMgr:

    def __init__(self, relative_dir: str | Path) -> None:
        """
        Initialize a PathMgr object. Creates the directory if it doesn't exist.
        Logs actions performed by the instance.

        Args:
            relative_dir (str or Path object): The relative directory where data will be stored and loaded.
        """
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.directory = Path(relative_dir).resolve()

        # Create directory only if it does not exist
        if not self.directory.exists():
            self.directory.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Created directory: {self.directory}")

    def file_exists(self, filename: str) -> bool:
        """
        Check if a file exists.
        Logs the check.

        Args:
            filename (str): The name of the file to check.

        Returns:
            bool: True if the file exists, False otherwise.
        """
        exists = (self.directory / filename).exists()
        self.logger.info(
            f"Checked if '{filename}' exists in '{self.directory}': {exists}"
        )
        return exists

    def delete_file(self, filename: str):
        """
        Delete a file.
        Logs the deletion.

        Args:
            filename (str): The name of the file to delete.

        Returns:
            None
        """
        filepath = self.directory / filename
        if filepath.exists():
            filepath.unlink()
            self.logger.info(f"Deleted file: {filepath}")
        else:
            self.logger.info(f"Attempted to delete non-existent file: {filepath}")

    def read_lines(self, filename: str) -> List[str]:
        """
        Reads a text file and returns its contents as a list of lines.

        Args:
            filename (str): The name of the text file to read.

        Returns:
            List[str]: A list of strings, each representing a line from the file.
        """
        filepath = self.directory / filename
        with open(filepath, "r") as f:
            lines = f.readlines()
            self.logger.info(f"Read text file: {filepath}")
            return lines

    def write_lines(self, filename: str, lines: List[str]):
        """
        Writes a list of lines to a text file.

        Args:
            filename (str): The name of the text file to write.
            lines (List[str]): A list of strings to write to the file.

        Returns:
            None
        """
        filepath = self.directory / filename
        with open(filepath, "w") as f:
            f.writelines(lines)
            self.logger.info(f"Wrote text file: {filepath}")

    def get_resolved_path(self, filename: str | None = None) -> Path:
        """
        Returns the resolved path for a given filename.

        Args:
            filename (str): The name of the file.

        Returns:
            Path: The resolved path for the file.
        """
        if filename is None:
            return self.directory
        else:
            return self.directory / filename
