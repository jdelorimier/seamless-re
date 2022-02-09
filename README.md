# Disclosed: AI-Powered Network Discovery

## About

This application connects to the US SEC archives EDGAR, and parses beneficial ownership information into a graph database. In this app, we leverage two layers of machine learning text enrichment models: 
1. NER (Named Entity Recognition)
2. NRE (Nural Relationship Extraction)

The final product is mapped into a graph database.


## Installation

## Quick start

#### Docker Compose

Start up app with:
```
docker-compose build
docker-compose up
```

#### Run Locally
See below on Poetry dependency manager installation

```
poetry shell
bash start.sh
```

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

### Dependincies issues

Currently we have to peg huggingface's `transformers` library at 3.5.1 due to conflicts with the modeles in `OpenNRE`

To utilize newer transformers like `LUKE` we will need to update to 4.0 library
