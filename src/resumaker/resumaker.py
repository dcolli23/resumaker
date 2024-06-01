from typing import Dict
from pathlib import Path

import yaml
import docxtpl
import doc2pdf
import docx2txt

ROOT_DIR = Path(__file__).parent
OUTPUT_DIR = ROOT_DIR / "output"
HYPERLINK_COLOR = "#000080"


def build_rt_hlink_obj(hlink_dict: Dict, doc: docxtpl.DocxTemplate):
    """Builds the docxtpl.RichText object for the supplied link

    Parameters
    ----------
    hlink_dict : dict
        Dictionary for the hyperlink that has `"display"` and `"url"` members for hyperlink.
    doc : docxtpl.DocxTemplate
        The template you're working with.
    """
    rt = docxtpl.RichText()
    rt.add(hlink_dict["display"],
           url_id=doc.build_url_id(hlink_dict["url"]),
           underline=True,
           color=HYPERLINK_COLOR,
           style="InternetLink")
    return rt


def populate_resume_template(doc: docxtpl.DocxTemplate, yaml_dict: Dict, output_path: Path):
    # Replace all of the links with rich text objects to dynamically hyperlink in the resume.
    yaml_dict["github"] = build_rt_hlink_obj(yaml_dict["github"], doc)
    yaml_dict["linkedin"] = build_rt_hlink_obj(yaml_dict["linkedin"], doc)
    yaml_dict["email"] = build_rt_hlink_obj(yaml_dict["email"], doc)
    for project in yaml_dict["Projects"]:
        if project["repo"]:
            project["repo"] = build_rt_hlink_obj(project["repo"], doc)
        if project["publication_href"]:
            project["publication_href"] = build_rt_hlink_obj(project["publication_href"], doc)

    doc.render(yaml_dict)
    doc.save(output_path.as_posix())
    print("Saved resume to:", output_path.as_posix())


def make_resume_docx(yaml_file: Path, docx_template: Path, output_path: Path):
    """Populates the resume template and writes to the output file"""
    with yaml_file.open('r') as f:
        yaml_dict = yaml.safe_load(f)

    doc = docxtpl.DocxTemplate(docx_template.as_posix())

    populate_resume_template(doc, yaml_dict, output_path)


def convert_to_pdf(doc_output_file: Path, pdf_output_file: Path):
    print("Now using doc2pdf to convert to PDF")
    doc2pdf.convert(doc_output_file, pdf_output_file)
    print("Done converting to PDF!")


def convert_to_txt(doc_output_file: Path, txt_output_file: Path):
    print("Now converting DOCX to TXT")
    text = docx2txt.process(doc_output_file)
    with txt_output_file.open('w') as f:
        f.write(text)
    print("Done converting to TXT!")


def verify_files(yaml_file: Path, docx_template: Path):
    """Verifies that the YAML and DOCX files exist"""
    if not yaml_file.is_file():
        raise FileNotFoundError(f"YAML file not found: {yaml_file}")
    if not docx_template.is_file():
        raise FileNotFoundError(f"DOCX template file not found: {docx_template}")


def main(yaml_file: Path,
         docx_template: Path,
         output_root_name: str,
         output_dir: Path = OUTPUT_DIR):
    """Generates the resume from the YAML and template files"""
    verify_files(yaml_file, docx_template)

    # TODO: Potentially check for and/or create the output directory.

    output_path_template = output_dir / output_root_name
    doc_output_file = output_path_template.with_suffix(".docx")

    make_resume_docx(yaml_file, docx_template, output_path_template)

    pdf_output_file = output_path_template.with_suffix(".pdf")
    convert_to_pdf(doc_output_file, pdf_output_file)
    print("Done making resume!")
