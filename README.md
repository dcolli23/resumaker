# Resumaker

Tool to produce resumes in both DOCX and PDF file formats from DOCX templates and YAML files containing the resume contents.

## Installation

The easiest method to install this package is to clone this repository and execute:

```
pip install -e .
```

I use my personal favorite virtual environment manager, `pipenv` for this. To install the environment for running Resumaker, run `python3 -m pip install pipenv`, then `pipenv install -e .` in the root directory of this repository.

## Usage

This library is setup such that the module is executable via the command line. To populate a DOCX template with the resume information in a YAML file, do the following:

1. Activate your Python environment if you installed `resumaker` in one.
2. Execute the following:
    ```
    python -m resumaker <yaml_file> <docx_template_file>
    ```
    
This populates the DOCX template with your information in the YAML file, convert that DOCX file to PDF, then use `evince` to display the PDF.

## Planned Development

I would very much like to make the resume sections modular so that one can pick and choose which sections to include. There's no promise that I'll get to this, but keep an eye on the [issues page](https://github.com/dcolli23/resumaker/issues) and star the repository if you'd like updates!