from typing import Dict
import argparse
import os
import pprint

import yaml
import docxtpl

ROOT = os.path.dirname(__file__)
HYPERLINK_COLOR = "#000080"
OUTPUT_DIR = os.path.join(ROOT, "output")


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


def make_resume(doc: docxtpl.DocxTemplate, yaml_dict: Dict, output_file: str):
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
    doc.save(output_file)
    print("Saved resume to:", output_file)


def convert_to_pdf(doc_output_file, pdf_output_file):
    try:
        os.system(f"doc2pdf {doc_output_file} {pdf_output_file}")
        print("Saved resume to:", pdf_output_file)
    except Exception as e:
        print("Failed to convert to PDF due to error:", e)


def main(yaml_file: str, docx_template: str, output_root: str):
    """Generates the resume from the YAML and template files.

    Parameters
    ----------
    args : argparse.ArgumentParser
        The parsed arguments.
    """
    # Read in the YAML file.
    with open(yaml_file, 'r') as f:
        yaml_dict = yaml.safe_load(f)

    # Open the structural template.
    template_full_path = os.path.join(docx_template)
    doc = docxtpl.DocxTemplate(template_full_path)

    doc_output_file = os.path.join(OUTPUT_DIR, output_root + ".docx")
    pdf_output_file = os.path.join(OUTPUT_DIR, output_root + ".pdf")
    make_resume(doc, yaml_dict, doc_output_file)
    # This doesn't play well with pipenv so temporarily using doc2pdf via bash script.
    # convert_to_pdf(doc_output_file, pdf_output_file)
    print("Done making resume!")


if __name__ == "__main__":
    # Set up the argument parser.
    description = "Tool to produce resumes from template YAML files."
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("yaml_file",
                        type=str,
                        help="The YAML file containing your resume information.")
    parser.add_argument("docx_template",
                        type=str,
                        help="File path to the resume structural template.")
    parser.add_argument("--output_root",
                        "-o",
                        type=str,
                        help="The root name of the output resume file.",
                        default="tmp")

    args = parser.parse_args()

    # Call the function.
    main(args.yaml_file, args.docx_template, args.output_root)
