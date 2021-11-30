# Seamless Relation Extraction

## About

The goal of this project is to extract entities of interest and link their relationships.


## Installation

### Poetry dependency manager

[Poetry](https://python-poetry.org/docs/) is a dependency managmnet tool for python. For setup, follow the setup on the main project repo. It is a bit of a hassle to set up, but the benefits are large for projects like this that depend on so many inter-dependent tools with multiple development and testing enviorments.

Once installed all dependencies can be installed with
```
poetry install
```
To enter into the virtual enviorment run
```
poetry shell
```

## Quick start

#### Development notebooks

View shell pipeline in `./notebooks/dev-nb.ipynb`

#### Development pipeline

Primary pipeline development will occur in `./seamless_re/pipeline.py`
