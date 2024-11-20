# Risk Score Extraction

Tool for extracting risk scores from thermography exam reports.

## Prerequisites

  1. The dependencies for this package are managed using [`poetry`](https://python-poetry.org/), and at the moment using poetry is the easiest way to install this package and it's dependencies. Details on installing poetry can be found [here](https://python-poetry.org/docs/). However, the easiest way to get started is to run the following command (which vendorizes poetry's dependencies, isolating poetry from the rest of your system):

      ```bash
      curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
      ```

      Assuming the above command didn't produce any errors, and assuming you see some help text upon running the command `poetry`, then you should be good to go.

      One can also setup poetry with command completion. [See the documentation](https://python-poetry.org/docs/#enable-tab-completion-for-bash-fish-or-zsh).

  1. There are various types of virtual env management tools (`conda`, `virtualenv`, etc.), `poetry` should play nice with environments created with those tools, however this shouldn't be necessary as poetry should avoid installing packages into your system's version of python when no such environment is detected by setting up it's own virtual envs as needed. Dealer's choice.

## Installation

```bash
git clone git@github.com:jmostovoy/medical_ai.git
cd medical_ai/score-extraction/
poetry install
```

The last command above should have installed a CLI called `thermo_scores` and all of the dependent packages. To test the installation run:

```bash
thermo_scores -h
```

Which should display the following help

```bash
usage: thermo_scores [-h] [-o json_file] [--raise-exceptions] pdf_file

Tools for extracting risk scores from thermography exam reports.

positional arguments:
  pdf_file            The PDF file from which to extract risk scores.

optional arguments:
  -h, --help          show this help message and exit
  -o json_file        The JSON file to write scores to. If not specified the
                      filename is determined from the PDF filename.
  --raise-exceptions  Raise an exception if scores are not found.
```

## Examples

To extract scores using the CLI just pass the path to a breast examination report (PDF) to the `thermo_scores` command:

```bash
thermo_scores /path/to/breast_exam_report.pdf
```

This should result in the creation of a JSON file with the same basename placed along side the PDF, in this case a file named:

```bash
/path/to/breast_exam_report.json
```

Whose contents should look something like:

```json
{
    "left_breast": {
        "level_string": "TH-3",
        "level": "3",
        "score": "75",
        "impressions": [
            "Curvilinear Thermovascular Pattern Upper Breast",
            "Vascular Hyperthermia \u2206T \u2265 2.0 \u00b0C (Contra Lateral)",
            "Asymmetrical Thermal Pattern",
            "Thermovascular Network"
        ]
    },
    "right_breast": {
        "level_string": "TH-2",
        "level": "2",
        "score": "65",
        "impressions": [
            "Curvilinear Thermovascular Pattern Upper Breast",
            "Regional Hyperthermia \u2206T \u2265 2.5 \u00b0C (Ipsi Lateral)",
            "Asymmetrical Thermal Pattern"
        ]
    }
}
```

It's also possible to script the extraction of scores from within python. Specifically, this would look like:

```python
import thermo_scores
report = '/path/to/breast_exam_report.pdf'
json_file = thermo_scores.pdf_to_json_scores(report)
print(json_file)  # prints: '/path/to/breast_exam_report.json'
```

which again would result in the same file that was produced by the CLI (above).
