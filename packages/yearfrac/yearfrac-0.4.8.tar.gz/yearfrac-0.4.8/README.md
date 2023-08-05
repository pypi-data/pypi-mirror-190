[![PyPI version](https://badge.fury.io/py/yearfrac.svg)](https://badge.fury.io/py/yearfrac)
[![yearfrac](https://snyk.io/advisor/python/yearfrac/badge.svg)](https://snyk.io/advisor/python/yearfrac)


# yearfrac

## Installation
The `yearfrac` [git repo](http://github.com/kmedian/yearfrac) is available as [PyPi package](https://pypi.org/project/yearfrac)

```
pip install yearfrac
```


## Usage
Check the [examples](https://github.com/kmedian/yearfrac/tree/master/examples) folder for notebooks.

Functions

* `isaleapyear` -- Check if a year is leap year
* `eastersunday` -- Determine day and month of an Easter Sunday for a given year
* `jd_to_date` and `date_to_jd` -- Julian Day number conversion
* `act_afb` -- Actual/Actual AFB
* `act_isda` -- Actual/Actual ISDA
* `d30360e` -- 30E/360 ISDA daycount method
* `d30365` -- 30/365 daycount method
* `yearfrac` -- Wrapper for all daycount methods


## Appendix

### Install a virtual environment

```
python3.7 -m venv .venv
source .venv/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt
pip3 install -r requirements-dev.txt
pip3 install -r requirements-demo.txt
```

(If your git repo is stored in a folder with whitespaces, then don't use the subfolder `.venv`. Use an absolute path without whitespaces.)

### Python Commands
* Check syntax: `flake8 --ignore=F401 --exclude=$(grep -v '^#' .gitignore | xargs | sed -e 's/ /,/g')`
* Run Unit Tests: `python -W ignore -m unittest discover`
* Remove `.pyc` files: `find . -type f -name "*.pyc" | xargs rm`
* Remove `__pycache__` folders: `find . -type d -name "__pycache__" | xargs rm -rf`

Publish

```sh
# pandoc README.md --from markdown --to rst -s -o README.rst  # RST file is too much trouble
python setup.py sdist 
twine upload -r pypi dist/*
```

### Support
Please [open an issue](https://github.com/kmedian/yearfrac/issues/new) for support.


### Contributors
* Adam Groszer [@agroszer](https://github.com/agroszer)
* Emilio Basualdo [@emiliobasualdo](https://github.com/emiliobasualdo)
* Ivan Nesic [@fatkaratekid](https://github.com/fatkaratekid)
* Vinay Gupta [@vinschess](https://github.com/vinschess)
* Ulf Hamster [@ulf1](https://github.com/ulf1)

Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/kmedian/yearfrac/compare/).
