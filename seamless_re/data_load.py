# given a ticker
# run pipeline
# load data

from seamless_re.database import Memgraph
from seamless_re import db_operations
import pandas as pd
import sys
# from pipeline import process

TICKER = "V"
count = 10

def clear(db):
    command = "MATCH (node) DETACH DELETE node"
    db.execute_query(command)

input = pd.DataFrame(
    {"head": ["Michael","Michael","Jim","Dwight"],
    "head_label":['PER','PER','PER',"PER"],
    "head_id":["1","1","2","3"],
    "relation":["Boss","Boss","Colleague","Colleague"],
    "tail":["Dwight","Jim","Dwight","Jim"],
    "tail_label":['PER','PER','PER',"PER"],
    "tail_id":["3","2","3","2"]
    }
)


def populate_database(db, input: list, file_source: str, ticker: str):

    # Make Central Company Node
    command = """MERGE (n:ORG {{ name: '{ticker}', id: 0}});""".format(ticker=ticker)
    db.execute_query(command)


    # look at head and tail and make single list of nodes
    input = input.to_dict('records')

    if len(input) > 0:
        ticker = input[0].get('ticker')
        command = """CREATE (n:file {{ id: '{path_to_file}', path: '{path_to_file}', name: '{ticker} filing'}});""".format(path_to_file=file_source,ticker=ticker)
        db.execute_query(command)

    for line in input:
        head_label = line.get('head_label')
        tail_label = line.get('tail_label')
        relation = line.get('relation')
        head = line.get('head')
        tail = line.get('tail')
        head_id = line.get('head_id')
        tail_id = line.get('tail_id')
        relation = relation.replace(" ","")
        i = 1
        # make head node
        # Update if node does not exist
        command = """MERGE (n:{entiy_type} {{ name: '{head}', type: '{head_label}', id: '{head_id}'}});""".format(entiy_type = head_label,head=head,head_id=head_id, head_label=head_label)
        db.execute_query(command)
        # Make tail node
        command = """MERGE (n:{entiy_type} {{ name: '{tail}', type: '{tail_label}', id: '{tail_id}'}});""".format(entiy_type = tail_label,tail=tail,tail_id=tail_id, tail_label=tail_label)
        db.execute_query(command)

        #### Make relations
        #  Match file to central node
        command = """MATCH (a:ORG),(b:file) WHERE a.id = 0 AND b.path = '{path_to_file}' MERGE (a)<-[r:filing_of]-(b);""".format(
            path_to_file=file_source,
        )
        db.execute_query(command)

        # Match head entity to file
        command = """MATCH (a:file),(b:{tail_label}) WHERE a.path = '{path_to_file}' AND b.id = '{tail_id}' MERGE (a)<-[r:appears_in]-(b);""".format(
            tail_label=tail_label,
            tail_id=tail_id,
            path_to_file=file_source,
        )
        db.execute_query(command)
        # Match tail entity to file
        command = """MATCH (a:file),(b:{head_label}) WHERE a.path = '{path_to_file}' AND b.id = '{head_id}' MERGE (a)<-[r:appears_in]-(b);""".format(
            head_label=head_label,
            head_id=head_id,
            path_to_file=file_source,
        )
        db.execute_query(command)

        # Match head and tail entitites to each other
        command = """MATCH (a:{head_label}),(b:{tail_label}) WHERE a.id = '{head_id}' AND b.id = '{tail_id}' CREATE (a)-[r:{relation}]->(b);""".format(
            head = head,
            tail = tail,
            head_label=head_label,
            tail_label=tail_label,
            head_id=head_id,
            tail_id=tail_id,
            relation=relation,
        )
        db.execute_query(command)

if __name__ == "__main__":
    ticker = sys.argv[1]
    count = sys.argv[2]
    """
    EASY
    """
    # path = "file://path_to_file.txt"
    # db = Memgraph()
    # db_operations.clear(db)
    # populate_database(db, input,file_source=path)

    """
    FULL
    """
    from seamless_re.pipeline import process
    from collection import get_id_and_background
    db = Memgraph()
    db_operations.clear(db)
    # text = read_file(file_path)
    filings, file_paths = get_id_and_background(ticker, count)
    if len(filings) == 0:
        print(f"No filings found for {ticker}")
    else:
        i = 0
        for text,file_path in zip(filings,file_paths):
            # print(text)
            data= process(text, ticker, index= i)
            i += 1

            # print(output)
            populate_database(db, input=data,file_source=file_path)




# filings = get_id_and_background(ticker, count)
# data = process()
# if len(filings) == 0:
#     print(f"No filings found for {ticker}")
# else:
#     for text in filings:
#         # print(text)
#         output = process(text)
#         print(output)

