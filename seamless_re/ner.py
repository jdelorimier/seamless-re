import json
import os
import spacy
import neuralcoref
from dotenv import load_dotenv
from urllib import parse, request

ENTITY_TYPES = ["human", "person", "company", "enterprise", "business", "geographic region",
                "human settlement", "geographic entity", "territorial entity type", "organization"]
# wikipedia key
load_dotenv()
WIKIFIER_KEY = os.getenv('WIKIFIER_KEY')
# download NLTK encoder to split paragraphs 


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


######## SPACY NER #########

nlp = spacy.load('en_core_web_sm')
neuralcoref.add_to_pipe(nlp)

def coreference(text: str):
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


def show_ents(doc): 
    if doc.ents: 
        for ent in doc.ents: 
            print(ent.text+' - ' +str(ent.start_char) +' - '+ str(ent.end_char) +' - '+ent.label_+ ' - '+str(spacy.explain(ent.label_))) 
        else: print('No named entities found.')

def spacy_ner(text):
    """
    takes full text blob returns list of dictionaries with 
    ent: entity text
    position: tuple( start, end)
    label: entity type
    """
    doc = nlp(text)
    output = []
    entities = doc.ents
    if entities:
        for ent in entities:
            start_char = ent.start_char
            end_char = ent.end_char
            label = ent.label_
            output.append(
                {
                    "ent": ent.text,
                    "positions":
                        (start_char, end_char),
                    "label":label
                } 
            )

    return output