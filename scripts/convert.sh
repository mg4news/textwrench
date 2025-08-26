#!/bin/bash

#====================================================================================
# See the main repository README.md for instructions on how to set up the environment
# The script should work in any environment (Windows, Linux, MacOs) that has the correct
# prerequisites
# Script takes twp parameters:
# -inp : a fully qualified path to the input markdown file 
# -out : the filename of the output pdf. Will be generated in the same directory as 
#        the input file
#====================================================================================

#====================================================================================
# Definitions, defaults
#====================================================================================

# Directories
THIS_DIR=$(pwd)

# Templates and CSS
TEMPLATE_HTML=$(pwd)/templates/default.html5
#CSS=$(pwd)/custom.css
CSS=$(pwd)/professional.css


#====================================================================================
# pandoc options wrapped up in one place
# pandoc path/doc.md -f gfm -t pdf --pdf-engine weasyprint -s -o ../pdf/doc.pdf
# Where:
#   "-f gfm"        indicates the "from" file is github flavoured markdown
#   "-t pdf"        indicates the "to" file is pdf
#   "--pdf-engine"  replace default with weasyprint
#   "-s"            ensures the output is standalone, not a doc fragment
#   "-o file.pdf"   sets the output file name to "file.pdf"
#
#====================================================================================
PANDOC_PDF_OPT="-f gfm -t html5 --css ${CSS} --template=${TEMPLATE_HTML} --pdf-engine weasyprint -s"
#PANDOC_PDF_OPT="-f gfm -t html5 --css ${CSS} --template=${TEMPLATE_HTML} --pdf-engine weasyprint -s --toc --toc-depth=3"
#PANDOC_HTML_OPT="-f gfm -t html5 --css ${CSS} --template=${TEMPLATE_HTML} -s --toc --toc-depth=3"
PANDOC_HTML_OPT="-f gfm -t html5 --css ${CSS} --template=${TEMPLATE_HTML} -s"

#====================================================================================
# generates a PDF file
# only does the operation if the .pdf does not exist, or if the .pdf is older than the .md
# - parameter 1 = the directory containing the markdown
# - parameter 2 = the markdown filename
# - parameter 3 = the output filename
#
# The function first changes to the directory, and runs pandoc locally.
# This is because PDF files are generated from intermediate HTML. If the intermediate (temporary) output
# is not in the same directory as the original MD, then relative links (images, etc) are broken
#====================================================================================
generate_pdf() {
  cd "${1}"
  local PDF="${3}"
  local MD="${2}"
  # Regenerate if PDF doesn't exist, or if the Markdown file is newer than the PDF
  if [ ! -e "${PDF}" ] || [ "${MD}" -nt "${PDF}" ]; then
    echo "Generating PDF: ${PDF}"
    pandoc "${MD}" ${PANDOC_PDF_OPT} -o "${PDF}"
  else
    echo "PDF is up to date - ${PDF}"
  fi
  cd "${THIS_DIR}"
}

#====================================================================================
# generates an HTML file
# only does the operation if the .pdf does not exist, or if the .pdf is older than the .md
# - parameter 1 = the directory containing the markdown
# - parameter 2 = the markdown filename
# - parameter 3 = the output filename
#
# The function first changes to the directory, and runs pandoc locally.
# This is because PDF files are generated from intermediate HTML. If the intermediate (temporary) output
# is not in the same directory as the original MD, then relative links (images, etc) are broken
#====================================================================================
generate_html() {
  cd "${1}"
  local HTML="${3}"
  local MD="${2}"
  # Regenerate if HTML doesn't exist, or if the Markdown file is newer than the HTML
  if [ ! -e "${HTML}" ] || [ "${MD}" -nt "${HTML}" ]; then
    echo "Generating HTML: ${HTML}"
    pandoc "${MD}" ${PANDOC_HTML_OPT} -o "${HTML}"
  else
    echo "HTML is up to date - ${HTML}"
  fi
  cd "${THIS_DIR}"
}

#====================================================================================
# Script logic for inputs. Parse named arguments
#====================================================================================

# Initialize variables
INPUT_FILE=""
OUTPUT_FILE=""

# Parse parameters
while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    -inp)
      INPUT_FILE="$2"
      shift 2
      ;;
    -out)
      OUTPUT_FILE="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Validate required parameters
if [[ -z "$INPUT_FILE" ]] || [[ -z "$OUTPUT_FILE" ]]; then
  echo "Usage: $0 -inp <fully_qualified_path_to_input_file> -out <output_file>"
  echo "The output file is written to the same directory as the input file" 
  exit 1
fi

# Split the input file into directory and filename components
INPUT_DIR="$(dirname "$INPUT_FILE")"
INPUT_FILENAME="$(basename "$INPUT_FILE")"

# call the generation function based on the extension
EXT="${OUTPUT_FILE##*.}"
case "$EXT" in
  pdf)
    generate_pdf "$INPUT_DIR" "$INPUT_FILENAME" "$OUTPUT_FILE"
    ;;
  html)
    generate_html "$INPUT_DIR" "$INPUT_FILENAME" "$OUTPUT_FILE"
    ;;
  *)
    echo "Error: Unsupported file extension .$EXT. Only .pdf and .html are allowed."
    exit 1
    ;;
esac
