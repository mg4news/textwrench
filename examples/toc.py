# In a script that uses your library, e.g., process_markdown.py

from textwrench.pathmgr import PathMgr
import textwrench.tocbuilder as tb


def toc_test():
    # The logger inside TextFile is now active and will print to the console.
    file_manager = PathMgr(relative_dir="./data")
    lines = file_manager.read_lines("baked.md")
    toc = tb.find_toc_marker(lines)
    print(toc)
    if toc:
        hm = tb.build_heading_map(lines, toc)
        if hm:
            new_toc = tb.new_toc_from_map(hm)
            for line in new_toc:
                print(line)

    ## Full test
    annotated = tb.build_toc(lines)
    file_manager.write_lines("baked_annotated.md", annotated)


if __name__ == "__main__":
    toc_test()
