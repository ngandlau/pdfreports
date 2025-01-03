# PDF Report Generation 

A tool to generate professionally looking PDFs (see `output/report.pdf` for an example) with footers and headers like:

![](output/pdf-report-example.jpg)

## Setup

Setup virtual environment:

```
poetry shell
poetry install
```

* Check out the `development.ipynb` notebook, in which we generate an example report
* The html template must be named `template.html`
* All images (e.g. logo) to be rendered in the PDF must be in the `templates` folder


