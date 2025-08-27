"""
Filename: __main__.py

Author: mg4news

Date: 2025-07-30

License: Unlicense

Description:
    Main entry point for the text wrench program.
"""

import argparse
import logging
import sys
from pathlib import Path
from textwrench.pathmgr import PathMgr
from textwrench.mdbuilder import assemble
from textwrench.pdfbuilder import PdfBuilder
from textwrench.tocbuilder import build_toc
from textwrench.imgfix import resolve_image_links

logger = logging.getLogger(__name__)


DESCRIPTION = """TextWrench is a set of tools for markdown files. It can:
  - assemble a single markdown file from linked documents
  - replace markdown TOC marker with HTML and PDF compatible TOC
  - convert markdown (via HTML) to PDF
  - apply different CSS to the HTML -> PDF conversion

Note: The intermediate and output files are written to the same directory as the input file
and use the input file name provided. If the input file name is (say) bob.md, then:
  - the assembled markdown is bob_assembled.md
  - the PDF is bob.pdf
"""

_CSS_PROFFESSIONAL = "templates/professional.css"
_CSS_STANDARD = "templates/standard.css"
_HTML_TEMPLATE = "templates/default.html5"


def sanity_check():
    fm = PathMgr(Path.cwd())
    if fm.file_exists(_CSS_PROFFESSIONAL):
        logger.info(f"Sanity check: found {_CSS_PROFFESSIONAL}")
    else:
        logger.warning(f"Sanity check: {_CSS_PROFFESSIONAL} not found")
    if fm.file_exists(_CSS_STANDARD):
        logger.info(f"Sanity check: found {_CSS_STANDARD}")
    else:
        logger.warning(f"Sanity check: {_CSS_STANDARD} not found")
    if fm.file_exists(_HTML_TEMPLATE):
        logger.info(f"Sanity check: found {_HTML_TEMPLATE}")
    else:
        logger.warning(f"Sanity check: {_HTML_TEMPLATE} not found")


def wrench(args):
    # sanity_check()
    logger.info(f"Processing {args.inp} with arguments: {args}")
    filepath = Path(args.inp)
    filestem = str(filepath.stem)
    fmgr = PathMgr(filepath.parent)
    toc = args.toc == "y"
    asm = args.asm == "y"
    css = (
        str(Path.cwd() / _CSS_PROFFESSIONAL)
        if args.css == "p"
        else str(Path.cwd() / _CSS_STANDARD)
    )

    # Read the file, then:
    # - if needed, assemble the file
    # - if needed, build the TOC
    # - store as a working file (replace existing)
    # - convert to PDF
    lines = fmgr.read_lines(filepath.name)
    if asm:
        logger.info("Assembling document...")
        lines = assemble(lines, fmgr)
    if toc:
        logger.info("Building table of contents...")
        lines = build_toc(lines)
    lines = resolve_image_links(lines, str(fmgr.get_resolved_path()))

    fmgr.write_lines(f"{filestem}_work.md", lines)
    pdf = PdfBuilder(fmgr)
    pdf.convert_to_pdf(
        input_md_file=f"{filestem}_work.md",
        output_pdf_file=f"{filestem}.pdf",
        css_file=css,
        html_template_file=str(Path.cwd() / _HTML_TEMPLATE),
    )


def main():
    parser = argparse.ArgumentParser(
        prog="textwrench",
        description=DESCRIPTION,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--inp", "-i", type=str, required=True, help="input file path")

    parser.add_argument(
        "-a",
        "--asm",
        type=str,
        choices=["y", "n"],  # limits input to 'y' or 'n'
        required=False,
        help="Assemble markdown from linked documents, 'y' or 'n' (default 'n')",
    )
    parser.add_argument(
        "-t",
        "--toc",
        type=str,
        choices=["y", "n"],  # limits input to 'y' or 'n'
        required=False,
        help="Parse out TOC marker, insert HTML/PDF compliant TOC, 'y' or 'n' (default 'n')",
    )
    parser.add_argument(
        "-c",
        "--css",
        type=str,
        choices=["s", "p"],
        required=False,
        help="Which CSS template to use, 's' = standard or 'p' = profesional (default 's')",
    )

    # No arguments, show the help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    # Parse the arguments
    try:
        args = parser.parse_args()
        wrench(args)
    except SystemExit:
        # argparse prints help automatically on error, we just exit
        sys.exit(1)

    logger.info("Processing complete.")


if __name__ == "__main__":
    main()
