"""CLI for resumaker, a tool for producing resumes from DOCX templates and resume information in
YAML files."""
from pathlib import Path
from typing import Dict, Any
import os
import subprocess

import yaml
from docxcompose.composer import Composer
import docx
import docx.document
import docxtpl

from resumaker import resumaker

RESUMAKER_MODULE_DIR = Path(os.path.dirname(__file__))
RESUMAKER_MODULE_ROOT_DIR = RESUMAKER_MODULE_DIR.parents[1]

WORKING_DIR = Path.cwd().resolve()
OUTPUT_DIR = WORKING_DIR / "output"
print("Output directory:", OUTPUT_DIR)
OUTPUT_DIR.mkdir(exist_ok=True)


class JobArguments:

    def __init__(self, job_path: Path):
        self._job_path = job_path
        self._job_dict = self._load_yaml(self._job_path)
        self.output_root_name: str = self._job_dict["output_root_name"]
        self._resume_body_path: Path = Path(self._job_dict["resume_body"])
        self.resume_body = self._load_yaml(self._resume_body_path.resolve())
        self.sections: list[Path] = [Path(p).resolve() for p in self._job_dict["sections"]]

    def _load_yaml(self, path: Path) -> Dict[str, Any]:
        with path.open("r") as f:
            return yaml.safe_load(f)


def remove_last_paragraph(doc: docx.document.Document):
    """Removes the last paragraph in a docx document
    
    NOTE: Should add a check to ensure that the paragraph is empty before removing it. 
    """
    last_p = None
    for el in reversed(doc.element.body):
        if el.tag.endswith("p"):
            last_p = el
            break
    if last_p is None:
        raise RuntimeError("No paragraph found in document")
    last_p.getparent().remove(last_p)


def load_doc_for_composition(doc_path: Path):
    """Loads a docx document and preps it for composition with other docs
    
    By, "preps it for composition," I mean that it removes the last paragraph from the document,
    preventing unnecessary whitespace between sections.
    """
    doc = docx.Document(doc_path)
    remove_last_paragraph(doc)
    return doc


def main(job_args: JobArguments, no_display_pdf: bool = False, convert_to_txt: bool = False):
    output_root: Path = OUTPUT_DIR / job_args.output_root_name
    output_docx = output_root.with_suffix(".docx")

    # Always inheret the style from the first doc in the sections list.
    parent_doc = load_doc_for_composition(job_args.sections[0])

    composer = Composer(parent_doc)

    for section_path in job_args.sections[1:]:
        doc = load_doc_for_composition(section_path)
        composer.append(doc)

    # Since `docxtpl` doesn't support creating a `DocxTemplate` from an existing `Document`, we need
    # to save the composed document to a temporary file and then load it back in.
    # TODO: Potentially switch to using the `tempfile` library for the intermediate file.
    temp_path = OUTPUT_DIR / "temp.docx"
    composer.save(temp_path.as_posix())
    doc = docxtpl.DocxTemplate(temp_path.as_posix())

    resumaker.populate_resume_template(doc, job_args.resume_body, output_docx)

    output_pdf = output_docx.with_suffix(".pdf")
    resumaker.convert_to_pdf(output_docx, output_pdf)

    # Open the PDF *in the background* if conversion was successful.
    no_display_pdf = False
    if not no_display_pdf:
        print("Displaying PDF in the background.")
        subprocess.Popen(["evince", output_pdf])

    # Convert to TXT if desired.
    if convert_to_txt:
        resumaker.convert_to_txt(output_docx, output_root.with_suffix(".txt"))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description=("CLI for resumaker, a tool for producing resumes from DOCX templates and "
                     "resume information contained in YAML files."))

    parser.add_argument("job_path", type=Path, help="The YAML file describing the resume job.")
    parser.add_argument("--no-display-pdf", default=False, action="store_true")
    parser.add_argument("--convert-to-txt", "-c", default=False, action="store_true")

    args = parser.parse_args()

    args.job_path = args.job_path.resolve()
    job_args = JobArguments(args.job_path)

    main(job_args, args.no_display_pdf, args.convert_to_txt)
