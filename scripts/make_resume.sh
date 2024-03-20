#!/bin/bash

TEMPLATE="templates/skills_and_research_highlight.docx"

YML_FILE="resume_bodies/blank_resume_body.yml"

# It would be great if I could add automatic date-tagging here. Probably appreciated by the
# recruiters too.
OUTPUT_NAME="my_resume"
OUTPUT_ROOT="output/${OUTPUT_NAME}"
OUTPUT_DOCX="${OUTPUT_ROOT}.docx"
OUTPUT_PDF="${OUTPUT_ROOT}.pdf"
OUTPUT_TXT="${OUTPUT_ROOT}.txt"

## Populate .docx template.
## ------------------------
pipenv run python resumaker.py "${YML_FILE}" \
                               "${TEMPLATE}" \
                               -o "${OUTPUT_NAME}"

## Convert .docx to PDF and open.
## ------------------------------
echo "Now using doc2pdf to convert to pdf"
doc2pdf "${OUTPUT_DOCX}"

# The cryptic `$?` checks the integer exit code of the last executed command. If it's not equal to
# 0, we know it failed.
if [ $? -ne 0 ]; then
    echo "ERROR: PDF conversion failed"
    exit 1
else
    echo "PDF conversion succeeded"
    evince "${OUTPUT_PDF}" &
fi

## Convert .docx to txt and print.
## -------------------------------
# This is good to get an idea of how resume parsers will see the resume.

# This jumbled up everything but is supposedly a way to do this without install something.
# unzip -p output/temp.docx word/document.xml | sed -e 's/<[^>]\{1,\}>//g; s/[^[:print:]]\{1,\}//g'

# docx2txt was incredibly good.
# docx2txt "${OUTPUT_DOCX}" "${OUTPUT_TXT}"
# echo
# echo "TXT-converted resume:"
# cat "${OUTPUT_TXT}"


