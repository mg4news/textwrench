"""
Filename: pdfbuilder.py

Author: mg4news

Date: 2025-08-25

License: Unlicense

Description:
    Pandoc builder class. Handles the conversion from MD -> HTML -> PDF
"""

import subprocess
from textwrench.pathmgr import PathMgr
import logging

logger = logging.getLogger(__name__)


class PdfBuilder:

    def __init__(self, fmgr: PathMgr) -> None:
        """
        Initializes the PdfBuilder with a PathMgr instance.

        Args:
            fmgr (PathMgr): An instance of PathMgr to handle file operations.
        """
        self.fmgr = fmgr
        logger.info("PdfBuilder initialized.")

    def convert_to_pdf(
        self,
        input_md_file: str,
        output_pdf_file: str,
        css_file: str,
        html_template_file: str,
    ):
        """
        Converts a markdown file to a PDF using pandoc.

        Args:
            input_md_file (str): The name of the input markdown file.
            output_pdf_file (str): The name of the output PDF file.
            css_file (str): The path to the CSS file to use for styling.
        """
        input_path = self.fmgr.directory / input_md_file
        output_path = self.fmgr.directory / output_pdf_file
        css_opt = f"--css={css_file}"
        html_opt = f"--template={html_template_file}"

        command = [
            "pandoc",
            str(input_path),
            "-f",
            "gfm",
            "-t",
            "html5",
            css_opt,
            html_opt,
            "--pdf-engine=weasyprint",
            "-s",
            "-o",
            str(output_path),
        ]

        logger.info(f"Executing pandoc command: {' '.join(command)}")
        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
            logger.info(
                f"Successfully converted '{input_md_file}' to '{output_pdf_file}'."
            )
        except subprocess.CalledProcessError as e:
            logger.error(f"Pandoc conversion failed for '{input_md_file}':")
            logger.error(f"Stdout: {e.stdout}")
            logger.error(f"Stderr: {e.stderr}")
            raise
        except FileNotFoundError:
            logger.error(
                "Pandoc or weasyprint not found. Please ensure they are installed and in your PATH."
            )
            raise
