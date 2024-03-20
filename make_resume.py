from pathlib import Path
import os
import subprocess

ROOT_DIR = Path(os.path.dirname(__file__))
OUTPUT_DIR = ROOT_DIR / "output"


def populate_resume_template(yaml_file: Path, docx_template: Path, output_root: str):
    """Populates the resume template by calling `resumaker.py`

    Assumes working directory is this repository's root directory.
    """
    # NOTE: Constructing this seperately from the subprocess function call in case I want to add
    # optional commands, such as the option to remove markdown-style hyperlinks.
    cmd = [
        "pipenv", "run", "python", "resumaker.py",
        yaml_file.as_posix(),
        docx_template.as_posix(), "-o", output_root
    ]
    print("Populating resume template with resume body.")
    subprocess.run(cmd, check=True)


def do_docx_to_pdf_conversion(docx_file: Path):
    print("Now using doc2pdf to convert to PDF")
    subprocess.run(["doc2pdf", docx_file], check=True)


def main(yaml_file: Path,
         docx_template: Path,
         output_name: str,
         no_display_pdf: bool = False,
         convert_to_txt: bool = False):
    # Have to change the working directory to this repo for pipenv environment activation.
    os.chdir(ROOT_DIR.as_posix())
    output_root = OUTPUT_DIR / output_name

    populate_resume_template(yaml_file, docx_template, output_name)
    output_docx = output_root.with_suffix(".docx")

    do_docx_to_pdf_conversion(output_docx)

    # Open the PDF *in the background* if conversion was successful.
    if not no_display_pdf:
        print("Displaying PDF in the background.")
        subprocess.Popen(["evince", output_root.with_suffix(".pdf")])

    # Convert to TXT if desired.
    if convert_to_txt:
        print("Converting output DOCX to TXT to check automated resume parsing compatibility.")
        subprocess.run(
            ["docx2txt", output_docx.as_posix(),
             output_root.with_suffix(".txt")], check=True)


if __name__ == "__main__":
    import argparse
    import datetime

    parser = argparse.ArgumentParser(
        description=("CLI for resumaker, a tool for producing resumes from DOCX templates and "
                     "resume information contained in YAML files."))

    parser.add_argument("--yaml_file",
                        "-y",
                        default=None,
                        type=Path,
                        help="The YAML file containing your resume info.")
    parser.add_argument("--docx_template",
                        "-d",
                        default=None,
                        type=Path,
                        help="File path to the resume structural template")

    # Zero-padded date format such that `ls` maintains chronological order.
    date_str = datetime.date.today().strftime("%Y%m%d")
    parser.add_argument("--output-name",
                        "-o",
                        type=str,
                        help="The root name of the output resume file *without* file extension.",
                        default=f"dylan_colli_resume_{date_str}")

    parser.add_argument("--no-display-pdf", default=False, action="store_true")
    parser.add_argument("--convert-to-txt", "-c", default=False, action="store_true")

    args = parser.parse_args()

    if args.yaml_file is None:
        args.yaml_file = ROOT_DIR / "resume_bodies" / "resume_grad_robotics.yml"

    if args.docx_template is None:
        args.docx_template = ROOT_DIR / "templates" / "skills_and_research_highlight.docx"

    main(**vars(args))
