# resumaker
Tool to produce resumes from template YAML files

## How To Run

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
