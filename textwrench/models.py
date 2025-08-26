"""
Filename: models.py

Author: mg4news

Date: 2025-07-30

License: Unlicense

Description:
    Contains TypedDict definitions for complex dictionaries used in TextWrench
    Prefer this to pydantic to limit dependencies and for a bit more efficiency.
"""

from typing import List, Optional, TypedDict


class TocMarker(TypedDict):
    start_line: int
    end_line: int
    min_depth: int
    max_depth: int
