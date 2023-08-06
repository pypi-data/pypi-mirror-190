# UEQ Plus Data Analyzer

[![PyPI](https://img.shields.io/pypi/v/ueqplusanalyze.svg?style=plastic)](https://pypi.org/project/ueqplusanalyze/)
[![Tests](https://img.shields.io/github/actions/workflow/status/B3J4y/ueq-plus-data-analyze/test_code.yml?style=plastic)](https://github.com/B3J4y/ueq-plus-data-analyze/actions/workflows/test_code.yml)

This repository is data analyzer for UEQ+ data in Python. The calculations are copied from the 
data analysis tool of the [oficial UEQ+ website](https://ueqplus.ueq-research.org/).

## Project structure

```
ueq-plus-data-analyze
| .github               # used for github files
  | workflows           # used for github actions
| data                  # example data which shows the needed data structure
| src
  | ueq-plus-anazye
| .gitignore
| definitions.py        # defines global variables
| LICENSE               
| README.md
| requirements.in       # every new package should be written in here
```