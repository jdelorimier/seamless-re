import itertools
import pandas as pd
import opennre
import hashlib



import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

### RE MODEL ###
model = opennre.get_model('wiki80_bert_softmax')

def relation_extraction_wiki(text: str, entities: list):
    """
    WARNING: Currently this only works in conjunction with the wikifier NER method.
    #TODO: standardize RE funtions

    Input:
    text (str): Free text
    entities (list): List of dictionary output from wikifier extraction function. Example:
    >>> entities = [{'title': 'Elon Musk',  'wikiId': 'Q317521',  'label': 'Person',  'characters': [(0, 8), (5, 8)]}, {'title': 'SpaceX',  'wikiId': 'Q193701',  'label': 'Organization',  'characters': [(58, 63)]}]
    """
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
                        "relation": data[0],
                        "tail": permutation[1]["title"],
                        "score": data[1],
                    }
                )
    return pd.DataFrame(triples)

def relation_extraction_spacy(text: str, entities: list, namespace_value):
    """
    WARNING: This only works in conjuncture with spacy NER method
    Input: 
    text (str): Free text
    entities (list): List of dictionaries from Spacy NER output. Example:
    >>> entities = [{'ent': 'James Bond', 'positions': (5, 6), 'label': 'PER'}]

    RETURN pd.DATAFRAME: [{"head":'James Bond', "head_label":"PER", "relation": "Employee", "tail":"MI6", "tail_label":"ORG"}]
    """
    triples = []
    for permutation in itertools.permutations(entities, 2):
        source = permutation[0]['positions']
        target = permutation[1]['positions']

        data = model.infer(
            {'text': text,
             'h': {'pos': [source[0], source[1] + 1]},
             't': {'pos': [target[0], target[1] + 1]}
             }
        )
        if data[0] == "no_relation":
            continue
        triples.append(
                    {
                        "head": permutation[0]["ent"],
                        "head_label":permutation[0]['label'],
                        "head_id": hashlib.sha256("{entity}{namespace_value}".format(entity=permutation[0]["ent"],namespace_value=str(namespace_value)).encode('utf-8')).hexdigest(),
                        "relation": data[0],
                        "tail": permutation[1]["ent"],
                        "tail_label":permutation[1]['label'],
                        "tail_id": hashlib.sha256("{entity}{namespace_value}".format(entity=permutation[1]["ent"],namespace_value=str(namespace_value)).encode('utf-8')).hexdigest(),
                        "score": data[1],
                    }
                )
        return pd.DataFrame(triples)