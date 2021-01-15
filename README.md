# TeachingTools

## Overview

When teaching any course, it is important to have up to date and accurate summaries of what is going on in the class. While learning management systems often enable instructors to summarize some useful information, there often is no flexibility and grades can be calculated differently than intended. The TeachingTools package allows for a more detailed course summary based on instructor specific needs. The package summarizes grades at the course level, section level, assignment level, and student level. It also provides lists of missing or ungraded assignments at the section, assignment, and student level as well. If a student has ever walked into your office asking "Wait... what's my grade again?????", this is the python package for you!

## An Intro to TeachingTools

Watch an introductory video to see what TeachingTools is and how to use it
[Link to video](https://youtu.be/NcUCpbYCDAc)

## Documentation

[link to documentation](./docs/index.html)

---

## Dependencies
* python 3.7
  * [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
  * [jupyter](https://jupyter.readthedocs.io/en/latest/install.html)
* [autopep8](https://pypi.org/project/autopep8/)
* [pylint](http://pylint.pycqa.org/en/latest/user_guide/installation.html)
* [pytest](https://docs.pytest.org/en/stable/getting-started.html)
* [pdoc3](https://pypi.org/project/pdoc3/)
* [pandas](https://pandas.pydata.org/getting_started.html)

Dependencies can be installed individually or by creating a conda environment using the command below:

**With makefile:**  

	make init

**Manually:**  

	conda env create --prefix ./envs --file environment.yml

---
