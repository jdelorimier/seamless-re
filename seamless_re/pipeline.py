import nltk
import sys
import pandas as pd
from seamless_re.utils import read_file
from utils import read_file
from ner import spacy_ner, coreference
from relation import relation_extraction_spacy
from collection import get_id_and_background

import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

nltk.download("punkt")

def process(text: str, ner=spacy_ner, relation=relation_extraction_spacy):
    triples = []
    # preform coreference: "Joe Biden is president. He lives in Deleware." -> "Joe Biden is president. Joe Biden lives in Deleware."
    text = coreference(text=text)

    tokenized_sentences = nltk.sent_tokenize(text)
    for sentence in tokenized_sentences:
        # Preform NER sentence by sentence.
        entities = ner(text=sentence)
        if len(entities) > 1:
            # Preform RE on each entity in the sentences.
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
    
    ticker = sys.argv[1]
    count = sys.argv[2]
    
    # text = read_file(file_path)
    filings = get_id_and_background(ticker, count)
    if len(filings) == 0:
        print(f"No filings found for {ticker}")
    else:
        for text in filings:
            # print(text)
            output = process(text)
            print(output)