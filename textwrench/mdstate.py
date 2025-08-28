"""
Filename: mdstate.py

Author: mg4news

Date: 2025-08-28

License: Unlicense

Description:
    Simple doc state utility. Gets fed each line of text and can determine state, etc.
"""

import logging
import re

_CODE_BLOCK_TYPE = re.compile(r"^```(\w+)?")


class MdState:

    def _reset_states(self):
        self.in_code_block = False
        self.code_block_type = None
        self.in_yaml_block = False
        self.in_html_block = False
        self.in_comment_block = False
        self._last_line = False

    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self._reset_states()
        self.line_count = 0

    def process_line(self, line: str):
        stripped_line = line.strip()
        self.line_count += 1

        # Changes state AFTER the end of each block
        if self._last_line:
            self._reset_states()

        # Check for code blocks (fenced code blocks)
        if stripped_line.startswith("```"):
            if not self.in_code_block:
                self.logger.info(f"Code block starts at line {self.line_count}.")
                self.in_code_block = True
                match = _CODE_BLOCK_TYPE.match(stripped_line)
                if match:
                    self.code_block_type = match.group(1)
                    self.logger.info(
                        f"Code block type: {self.code_block_type} at line {self.line_count}."
                    )
            else:
                self.logger.info(f"Code block ends at line {self.line_count}.")
                self._last_line = True
            return

        # Check for HTML comment blocks
        if not self.in_comment_block and stripped_line.startswith("<!--"):
            self.in_comment_block = True
            self.logger.info(f"HTML comment block starts at line {self.line_count}.")
        elif self.in_comment_block and stripped_line.endswith("-->"):
            self._last_line = True
            self.logger.info(f"HTML comment block ends at line {self.line_count}.")
            return  # The line ending the comment block is part of the block

        # Check for YAML front matter (typically at the very beginning of the file)
        # This is a simplified check and might need refinement for complex YAML
        if self.line_count == 1 and not self.in_yaml_block and stripped_line == "---":
            # Only start YAML block if it's the first '---' or after content
            if (
                not self.in_code_block
                and not self.in_html_block
                and not self.in_comment_block
            ):
                self.in_yaml_block = True
                self.logger.info(f"YAML block starts at line {self.line_count}.")
        elif self.in_yaml_block and stripped_line == "---":
            self._last_line = True
            self.logger.info(f"YAML block ends at line {self.line_count}.")
            return  # The line ending the YAML block is part of the block

        # Check for raw HTML blocks (simplified: lines starting with < and ending with >)
        # This is a very basic check and might not cover all HTML cases
        if (
            not self.in_html_block
            and stripped_line.startswith("<")
            and stripped_line.endswith(">")
        ):
            self.in_html_block = True
            self.logger.info(f"HTML block starts at line {self.line_count}.")
        elif self.in_html_block and stripped_line.startswith("</"):
            self._last_line = True
            self.logger.info(f"HTML block ends at line {self.line_count}.")
            return  # The line ending the HTML block is part of the block
