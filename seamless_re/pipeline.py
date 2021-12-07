import nltk
import sys
import pandas as pd
from seamless_re.utils import read_file
from utils import read_file
from ner import spacy_ner, coreference
from relation import relation_extraction_spacy

import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

nltk.download("punkt")

def process(text: str, ner=spacy_ner, relation=relation_extraction_spacy):
    triples = []
    text = coreference(text=text)

    tokenized_sentences = nltk.sent_tokenize(text)
    for sentence in tokenized_sentences:
        entities = ner(text=sentence)
        if len(entities) > 1:
            triples.append(relation(text=sentence, entities=entities))
        
    if triples:
        return (
            pd.concat(triples)
            .sort_values(by="score", ascending=False)
            .drop_duplicates(keep="first",subset=['head','tail'])
            .reset_index(drop=True)
        )
    return pd.DataFrame(columns=["head", "relation", "tail", "score"])


if __name__ == "__main__":
    file_path = sys.argv[1]
    text = read_file(file_path)
    process = process(text)
    print(process)