"""
Filename: mdbuilder.py

Author: mg4news

Date: 2025-08-20

License: Unlicense

Description:
    Walks a markdown file, and inserts any linked markdown documents.
    Results in a single assembled markdown file
"""

import re
from typing import List
from textwrench.pathmgr import PathMgr
import logging

logger = logging.getLogger(__name__)

# Explanation of regex:
# 	^ → start of line
# 	\s* → allow optional whitespace before the link
# 	(!)? → Optional embed character i.e. !
# 	\[\[ ... \]\] → the wiki link itself
# 	\s* → allow trailing spaces
# 	$ → end of line
_DOC_LINK_RE = re.compile(r"^\s*(!)?\[\[([^\]|]+)(?:\|([^\]]+))?\]\]\s*$")
_MAX_PASSES = 3


def strip_yaml_comment_blocks(lines: List[str]) -> List[str]:
    """
    Removes YAML-style blocks wrapped in <!-- ... --> from a list of markdown lines.

    Args:
        lines (List[str]): Markdown content as a list of lines.

    Returns:
        List[str]: Lines with YAML blocks removed.
    """
    stripped = []
    inside_block = False

    for line in lines:
        # Check for block start
        if not inside_block and line.strip().startswith("<!--"):
            inside_block = True
            continue
        # Check for block end
        if inside_block and line.strip().endswith("-->"):
            inside_block = False
            continue
        # Only keep lines outside blocks
        if not inside_block:
            stripped.append(line)

    return stripped


def _one_pass(lines: List[str], fmgr: PathMgr) -> List[str]:
    """
    Perform a single assembly pass.

    Args:
        lines (List[str]): A list of strings, each representing a line of text from the root document
        fmgr (PathMgr): A File/Path Manager instance to handle fetching documents

    Returns:
        a list of lines representing the assembled linked document
    """
    logger.info("Document assemply pass starting...")
    new_lines = []
    for line in lines:
        match = _DOC_LINK_RE.match(line)
        doc = None
        if match:
            is_embed, doc, alias = match.groups()
            logger.info(f"Found doc link: {doc}")
        if doc and fmgr.file_exists(f"{doc}.md"):
            logger.info(f"Inserted document: {doc}")
            n = fmgr.read_lines(f"{doc}.md")
            new_lines.extend(strip_yaml_comment_blocks(n))
        else:
            new_lines.append(line)
    logger.info("Document assembly pass done...")
    return new_lines


def assemble(lines: List[str], fmgr: PathMgr, passes: int = 1) -> List[str]:
    """
    Assembles a single markdown file from linked markdown documents. Runs up
    to three passes. Inlines in any markdown document referenced by an Obsidian or
    Wikipedia style doc link. Each pass (default = 1) fetches the next level of documents.

    Args:
        lines (List[str]): A list of strings, each representing a line of text from the root document
        fmgr (PathMgr): A File/Path Manager instance to handle fetching documents
        passes (int): the maximum number of passes to make. Defaults to 1.

    Returns:
        a list of lines representing the assembled linked document

    Raises:
        a value error if the maximum number of passes is exceeded

    """
    if passes > _MAX_PASSES:
        msg = f"Maximum number of passes ({_MAX_PASSES}) exceeded. Aborting."
        logger.error(msg)
        raise ValueError(msg)

    asm_lines = lines
    for p in range(passes):
        logger.info(f"Document assembly pass: {p + 1} / {passes}")
        asm_lines = _one_pass(asm_lines, fmgr)
    return asm_lines
