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
    python -m resumaker <job_yaml_file>
    ```
    Where `<job_yaml_file>` is the YAML file containing the path to the YAML file with all of your resume body information, the paths to sections that you want to compose for your resume, among other arguments.
    
This populates the DOCX templates with your information in the YAML file, converts the output DOCX file to PDF, then uses `evince` to display the PDF.

For more information on how to format the input files, see `resume_bodies/blank_resume_body.yaml` and `jobs/example_resume_job.yaml`.
