# Resumaker
Tool to produce resumes from template YAML files

## Installation

### Python Dependencies

I used my personal favorite virtual environment manager, `pipenv` for this. To install the environment for running Resumaker, run `python3 -m pip install pipenv`, then `pipenv install` in the root directory of this repository.

### Additional Dependencies

If you'd like to automatically convert the resume to a PDF after generating it, `sudo apt install doc2pdf`.

Additionally, if you'd like to convert the PDF to plain-text (to get a better idea of how an [ATS](https://www.jobscan.co/blog/8-things-you-need-to-know-about-applicant-tracking-systems/) might parse your resume), install `docx2txt` via `sudo apt install docx2txt`.
- This is optional and isn't run by the [Script For Rapid Resume Template Population](#script-for-rapid-resume-template-population) by default.

## How To Run

### Script For Rapid Resume Template Population

You'll see below that you can run this tool directly via the command line, but this means you have to run the other steps (like PDF conversion) separately, which is a tad annoying. Instead, you can use the script in `scripts/make_resume.sh` to do all of this for you and to avoid typing out commands over and over again.

To run this, edit the script, filling in the variables with your resume body (YAML file) and desired template(DOCX file). Then:
```bash
cd <REPOSITORY_ROOT_DIRECTORY>
./scripts/make_resume.sh
```

### Direct Python Interface

1. Activate the `pipenv` virtual environment by executing:
    ```bash
    pipenv shell
    ```
2. Run `resumaker.py` by executing:
    ```bash
    python resumaker.py <resume.yml file> <docx structural template>
    ```
    This saves your constructed resume in `temp.docx` in the `output` directory.
3. If you'd like to convert the resume to PDF, you can install and run `doc2pdf` and convert with `doc2pdf output/temp.docx`.

Currently, there are two choices for templates: a basic template and a template that highlights the skills you learned from specific positions and projects. I've included my two `resume.yml` files to see how they're structured.
