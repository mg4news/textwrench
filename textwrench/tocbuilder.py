"""
Filename: tocbuilder.py

Author: mg4news

Date: 2025-07-30

License: Unlicense

Description:
    Walks a markdown file, and looks for a TOC marker (various formats). It builds a table of contents
    at that point. It ignores any headers preceding the TOC marker. The table of contents is
    built using links so that it remains navigable after the conversion to HTML and PDF. Duplicate links
    are managed in the same way as github.
"""

from typing import List, Optional
from textwrench.models import TocMarker
import re
import logging

logger = logging.getLogger(__name__)
_TOC_START = "```toc"
_TOC_END = "```"
_TOC_DEPTH_RE = re.compile(r"^(min_depth|max_depth):\s*(\d+)$")


def find_toc_marker(lines: List[str]) -> Optional[TocMarker]:
    """
    Searches a list of lines for a table of contents marker. of the form
    ```toc
    min_depth: 1
    max_depth: 2
    ```

    Args:
        lines (List[str]): A list of strings, each representing a line of text.

    Returns:
        TOC dict if found and parsed, else None

    Raises:
        a value error if the TOC block is too long
    logger.info("Searching for TOC marker...")

    """
    logger.info("Searching for TOC marker...")
    toc: Optional[TocMarker] = None

    for i, line in enumerate(lines):
        line = line.strip()
        if not toc and line == _TOC_START:
            toc = {"start_line": i, "end_line": i, "min_depth": 1, "max_depth": 3}
            logger.info(f"Found TOC start marker at line {i + 1}.")
        elif toc:
            if line == _TOC_END:
                toc["end_line"] = i
                logger.info(f"Found TOC end marker at line {i + 1}.")
                if toc["end_line"] - toc["start_line"] > 5:
                    msg = f"TOC marker block is too long (lines {toc['start_line'] + 1}–{toc['end_line'] + 1})."
                    logger.error(msg)
                    raise ValueError(msg)
                return toc
            else:
                match = _TOC_DEPTH_RE.match(line)
                if match and toc:
                    key, value = match.groups()
                    toc[key] = int(value)
    return None


def build_heading_map(lines: List[str], toc: TocMarker) -> dict[int, tuple[int, str]]:
    """
    Extracts a heading "map" from a markdown file.

    logger.info(f"Building heading map, starting after line {toc['end_line'] + 1}.")
    Args:
        lines (List[str]): A list of strings, each representing a line of text.
        if line_number <= toc["end_line"]:

    Returns:
        a map (dictionary) of line number :: (depth, heading text)

    """
    logger.info(f"Building heading map, starting after line {toc['end_line'] + 1}.")
    heading_map = {}
    for line_number, line in enumerate(lines):
        if line_number <= toc["end_line"]:
            continue
        match = re.match(r"^(#+)\s*(.*?)\s*#*\s*$", line)
        if match:
            depth = len(match.group(1))
            if depth < toc["min_depth"] or depth > toc["max_depth"]:
                continue
            heading_text = match.group(2).strip()
            heading_map[line_number] = (depth, heading_text)
    logger.info(f"Found {len(heading_map)} headings matching depth criteria.")
    return heading_map


def new_toc_from_map(heading_map: dict[int, tuple[int, str]]) -> List[str]:
    logger.info(f"Generating new TOC from a map of {len(heading_map)} headings.")
    """
    Builds a new hyperlinked TOC from the heading map

    Args:
        heading_map (dict[int, tuple[int, str]]): a map (dictionary) of line number

    Returns:
        a line list of the new TOC

    """
    logger.info(f"Generating new TOC from a map of {len(heading_map)} headings.")
    new_toc_lines = ["## Table of Contents\n", "\n"]
    slug_counts = {}

    for line_number, (depth, heading_text) in heading_map.items():
        prefix = "    " * (depth - 1) + "- "

        # to lower; remove anything not alphanumeric, space, or hyphen; replace spaces with hyphens
        base_slug = heading_text.lower()
        base_slug = re.sub(r"[^\w\s-]", "", base_slug)
        base_slug = re.sub(r"\s+", "-", base_slug)

        # Handle duplicate slugs to ensure unique links, similar to GitHub
        count = slug_counts.get(base_slug, 0)
        slug_counts[base_slug] = count + 1
        if count > 0:
            slug = f"{base_slug}-{count}"
            logger.info(f"Found duplicate slug: {slug}. Appended count.")
        else:
            slug = base_slug

        line = prefix + f"[{heading_text}](#{slug})\n"
        new_toc_lines.append(line)

    logger.info(f"Generated {len(new_toc_lines)} lines for the new TOC.")
    return new_toc_lines


def build_toc(lines: List[str]) -> List[str]:
    """
    Builds a table of contents from a list of strings from a markdown file
    It replaces the Obsidian plugin YAML toc marker with a TOC that remains
    navigable after conversion to HTML

    Args:
        lines (List[str]): A list of strings, each representing a line of text.

    Returns:
        a line list. Either empty if nothing found, or updated with the TOC

    """
    logger.info("Starting TOC build process.")
    toc = find_toc_marker(lines)
    if not toc:
        logger.warning("TOC build process aborted: No TOC marker found.")
        return lines

    hm = build_heading_map(lines, toc)
    if not hm:
        logger.warning("No headings found. TOC will be empty.")

    new_toc = new_toc_from_map(hm)

    # Reconstruct the file content by taking lines before the marker,
    # inserting the new TOC, and appending lines after the marker.
    pre_toc_lines = lines[: toc["start_line"]]
    post_toc_lines = lines[toc["end_line"] + 1 :]

    logger.info("Successfully built new content with updated TOC.")
    return pre_toc_lines + new_toc + post_toc_lines
