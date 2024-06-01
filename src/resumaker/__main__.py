"""CLI for resumaker, a tool for producing resumes from DOCX templates and resume information in
YAML files."""
from pathlib import Path
import os
import subprocess

from resumaker import resumaker

RESUMAKER_MODULE_DIR = Path(os.path.dirname(__file__))
RESUMAKER_MODULE_ROOT_DIR = RESUMAKER_MODULE_DIR.parents[1]

WORKING_DIR = Path.cwd().resolve()
OUTPUT_DIR = WORKING_DIR / "output"


def main(yaml_file: Path,
         docx_template: Path,
         output_name: str,
         no_display_pdf: bool = False,
         convert_to_txt: bool = False,
         output_dir: Path = OUTPUT_DIR):
    # Placing this in the main function to avoid creating the directory until necessary.
    output_dir.mkdir(exist_ok=True)

    resumaker.verify_files(yaml_file, docx_template)

    output_root = output_dir / output_name
    output_docx = output_root.with_suffix(".docx")
    output_pdf = output_root.with_suffix(".pdf")

    resumaker.make_resume_docx(yaml_file, docx_template, output_docx)
    resumaker.convert_to_pdf(output_docx, output_pdf)

    # Open the PDF *in the background* if conversion was successful.
    if not no_display_pdf:
        print("Displaying PDF in the background.")
        subprocess.Popen(["evince", output_pdf])

    # Convert to TXT if desired.
    if convert_to_txt:
        resumaker.convert_to_txt(output_docx, output_root.with_suffix(".txt"))


if __name__ == "__main__":
    import argparse
    import datetime

    parser = argparse.ArgumentParser(
        description=("CLI for resumaker, a tool for producing resumes from DOCX templates and "
                     "resume information contained in YAML files."))

    parser.add_argument("--yaml_file",
                        "-y",
                        required=True,
                        type=Path,
                        help="The YAML file containing your resume info.")
    parser.add_argument("--docx_template",
                        "-d",
                        required=True,
                        type=Path,
                        help="File path to the resume structural template")

    # Zero-padded date format such that `ls` maintains chronological order.
    date_str = datetime.date.today().strftime("%Y%m%d")
    parser.add_argument("--output-name",
                        "-o",
                        type=str,
                        help="The root name of the output resume file *without* file extension.",
                        default=f"resume_{date_str}")

    parser.add_argument("--no-display-pdf", default=False, action="store_true")
    parser.add_argument("--convert-to-txt", "-c", default=False, action="store_true")

    args = parser.parse_args()

    args.yaml_file = args.yaml_file.resolve()
    args.docx_template = args.docx_template.resolve()

    main(**vars(args))
