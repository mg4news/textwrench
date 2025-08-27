"""
Filename: img.py

Author: mg4news

Date: 2025-08-27

License: Unlicense

Description:
    Example / test to exercise and debug the imgfix module
"""

from textwrench.pathmgr import PathMgr
import textwrench.imgfix as imgfix


def imgfix_test():
    # The logger inside TextFile is now active and will print to the console.
    fmgr = PathMgr(relative_dir="./data")
    lines = fmgr.read_lines("document-main.md")
    lines = imgfix.resolve_image_links(lines, str(fmgr.get_resolved_path()))
    fmgr.write_lines("document-main_imgfix.md", lines)


if __name__ == "__main__":
    imgfix_test()
