# TeachingTools
--

## Overview

WORDS

## An Intro to TeachingTools

Watch an introductory video to see what TeacingTools is and how to use it ADD LINK TO VIDEO WHEN PUBLISHED

## Documentation

[link to documentation](TeachingTools)

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

Depenedencies can be installed individually or by creating a conda environment using the command below:

**With makefile:**  

	make init

**Manually:**  

	conda env create --prefix ./envs --file environment.yml

--