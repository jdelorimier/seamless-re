import itertools
import json
import os
# import neuralcoref
import spacy
import torch
import nltk
import opennre
import pandas as pd
from dotenv import load_dotenv
from urllib import parse, request
from transformers import LukeForEntityPairClassification, LukeTokenizer

# Define some global variables
ENTITY_TYPES = ["human", "person", "company", "enterprise", "business", "geographic region",
                "human settlement", "geographic entity", "territorial entity type", "organization"]
# wikipedia key
load_dotenv()
WIKIFIER_KEY = os.getenv('WIKIFIER_KEY')

if __name__ == "__main__":
    print('main')

