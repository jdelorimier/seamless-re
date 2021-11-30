import itertools
import json
import os
import neuralcoref
import spacy
import torch
import nltk
import opennre
import pandas as pd
from dotenv import load_dotenv
from urllib import parse, request
from seamless_re.utils import read_file

import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

# from transformers import LukeForEntityPairClassification, LukeTokenizer


# Define some global variables
ENTITY_TYPES = ["human", "person", "company", "enterprise", "business", "geographic region",
                "human settlement", "geographic entity", "territorial entity type", "organization"]
# wikipedia key
load_dotenv()
WIKIFIER_KEY = os.getenv('WIKIFIER_KEY')
# download NLTK encoder to split paragraphs 
nltk.download("punkt")
# define model
model = opennre.get_model('wiki80_bert_softmax')

def coreference(text: str):
    nlp = spacy.load("en")
    neuralcoref.add_to_pipe(nlp)
    doc = nlp(text)
    tokens = [token.text_with_ws for token in doc]
    for cluster in doc._.coref_clusters:
        cluster_main_words = set(cluster.main.text.split(" "))
        for coref in cluster:
            if coref != cluster.main:
                if coref.text != cluster.main.text and not set(
                    coref.text.split(" ")
                ).intersection(cluster_main_words):
                    tokens[coref.start] = cluster.main.text + doc[coref.end - 1].whitespace_
                    for i in range(coref.start + 1, coref.end):
                        tokens[i] = ""
    output = "".join(tokens)
    return output

def wikipedia_el(text: str, pageRankSqThreshold = 0.8):
    data = parse.urlencode(
        [
            ("text",text),
            ("lang","en"),
            ("userKey",WIKIFIER_KEY),
            ("pageRankSqThreshold",f"{pageRankSqThreshold}"),
            ("applyPageRankSqThreshold", "true"),
            ("wikiDataClasses", "true"),
            ("wikiDataClassIds", "false"),
            ("support", "true"),
            ("ranges", "false"),
            ("nTopDfValuesToIgnore", "100"),
            ("nWordsToIgnoreFromList", "100"),
            # ("minLinkFrequency", "1"),
            ("minLinkFrequency", "2"),
            ("includeCosines", "false"),
            # ("maxMentionEntropy", "1"),
            ("maxMentionEntropy", "3"),
        ]
    )

    response = request.Request(
        "http://www.wikifier.org/annotate-article", data=data.encode("utf8"), method="POST"
    )
    with request.urlopen(response, timeout=60) as f:
        response = f.read()
        response = json.loads(response.decode("utf8"))
    
    entities = []
    if "annotations" in response:
        for entity in response['annotations']:
            if ENTITY_TYPES:
                if not entity['wikiDataClasses']:
                    continue
                if not any([t["enLabel"] in ENTITY_TYPES for t in entity["wikiDataClasses"]]):
                    continue
            entities.append(
                {
                    "title": entity['secTitle'],
                    "url": entity['secUrl'],
                    "id": entity['wikiDataItemId'],
                    "types": entity["dbPediaTypes"],
                    "positions": [
                        (position['chFrom'], position['chTo'])
                        for position in entity['support']
                    ],
                }
            )
    return entities

def relation_extraction(text: str, entities: list):
    triples = []
    for permutation in itertools.permutations(entities, 2):
        for source in permutation[0]["positions"]:
            for target in permutation[1]["positions"]:
                data = model.infer(
                    {
                        "text": text,
                        "h": {"pos": [source[0], source[1] + 1]},
                        "t": {"pos": [target[0], target[1] + 1]}
                    }
                )
                if data[0] == "no_relation":
                    continue
                triples.append(
                    {
                        "head": permutation[0]["title"],
                        "relation": permutation[1]["title"],
                        "score": data[1],
                    }
                )

    return pd.DataFrame(triples)

def process(text: str):
    triples = []
    text = coreference(text=text)

    tokenized_sentences = nltk.sent_tokenize(text)
    for sentence in tokenized_sentences:
        entities = wikipedia_el(text=sentence)
        if len(entities) > 1:
            triples.append(relation_extraction(text=sentence, entities=entities))
        
        if triples:
            df = (
                pd.concat(triples)
                .sort_values(by="score", ascending=False)
                .drop_duplicates(keep="first",subset=['head','tail'])
                .reset_index(drop=True)
            )
            return df
        else:
            return pd.DataFrame(columns=["head", "relation", "tail", "score"])


if __name__ == "__main__":
    print('main')

