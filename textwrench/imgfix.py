"""
Filename: imgfix.py

Author: mg4news

Date: 2025-08-26

License: Unlicense

Description:
    Parses out image links and replaces them with absollute links. This allows pandoc to find them without
    needing to run the program from the directory the markdown is in
"""

import re
from pathlib import Path
import logging
from typing import List

logger = logging.getLogger(__name__)

_IMG_LINK = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")


def _resolve_image_link(link: str, md_dir: str) -> str:
    """
    Resolves a single parsed out image link

    Args:
        link (str): the matched link
        md_dir: the directory of the current markdown document

    Return:
        an absolute link to the image file, if found

    Raises:
        an error if the image file cannot be found
    """
    if Path(link).is_file():
        resolved = str(Path(link))
    elif Path(Path(md_dir) / link).is_file():
        resolved = str(Path(md_dir) / link)
    else:
        logger.error(f"Image file not found: {link}")
        resolved = f"ERROR: Image file not found: {link}"
    return resolved


def resolve_image_links(lines: List[str], md_dir: str) -> List[str]:
    """
    Finds markdown image links in lines, searches for the file under md_dir,
    and replaces the reference with the fully qualified path if found.

    Args:
        lines: list of markdown lines (strings).
        md_dir: root directory to search for image files.

    Returns:
        list of processed lines with updated image paths.
    """
    logger.info(f"Resolving image links using doc path: {md_dir}")
    new_lines = []
    for line in lines:
        match = _IMG_LINK.search(line)
        if match:
            title, link = match.groups()
            if link:
                logger.info(f"Resolving image link: [{title}]({link})")
                line = line.replace(link, _resolve_image_link(link, md_dir))
        new_lines.append(line)

    return new_lines
