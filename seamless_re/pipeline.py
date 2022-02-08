import nltk
import sys
import pandas as pd
from seamless_re.utils import read_file
from seamless_re.ner import spacy_ner, coreference
from seamless_re.relation import relation_extraction_spacy
from seamless_re.collection import get_id_and_background, secedgar_method

import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

try:
   nltk.data.find('tokenizers/punkt')
except LookupError:
    print("Download not found")
    nltk.download("punkt")


def process(text: str,url: str, ticker,index, ner=spacy_ner, relation=relation_extraction_spacy):
    triples = []
    # preform coreference: "Joe Biden is president. He lives in Deleware." -> "Joe Biden is president. Joe Biden lives in Deleware."
    text = coreference(text=text)

    tokenized_sentences = nltk.sent_tokenize(text)
    for sentence in tokenized_sentences:
        # Preform NER sentence by sentence.
        entities = ner(text=sentence)
        if len(entities) > 1:
            # Preform RE on each entity in the sentences.
            triples.append(relation(text=sentence, entities=entities, namespace_value=index))
        
    if triples:
        # Add entity_type for head and tail
        # Add ID for head and tail

        df = pd.concat(triples).sort_values(by="score", ascending=False).drop_duplicates(keep="first",subset=['head','tail']).reset_index(drop=True)
        df['ticker'] = ticker
        df['url'] = url
        return df
        
    return pd.DataFrame(columns=["head","head_label","head_id","relation","tail","tail_label","tail_id","ticker","score"])


if __name__ == "__main__":
    
    ticker = sys.argv[1]
    count = sys.argv[2]
    
    # text = read_file(file_path)
    urls, filings = secedgar_method(ticker, count)
    if len(filings) == 0:
        print(f"No filings found for {ticker}")
    else:
        i = 0
        for text, url in zip(filings, urls):
            # print(text)
            output= process(text, url, ticker, index= i)
            i += 1

            print(output)