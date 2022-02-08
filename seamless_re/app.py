from flask import Flask, render_template, jsonify, make_response, request
from html2text import element_style
from seamless_re.database import Memgraph
from seamless_re import db_operations
from seamless_re import collection
from seamless_re import data_load

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
#     db = Memgraph()
#     db_operations.clear(db)
#     db_operations.populate_database(db, "seamless_re/resources/data_big.txt")
    return render_template('index.html')

@app.route('/', methods=['POST'])
def submit_query():
    ticker = request.form['text']
    # processed_ticker = ticker.upper()

    db = Memgraph()
    db_operations.clear(db)
    # filings, file_paths = collection.get_id_and_background(processed_ticker, 20)
    import asyncio
    asyncio.set_event_loop(asyncio.new_event_loop())
    urls, filings = collection.secedgar_method(ticker, count=10)
    if len(filings) == 0:
        pass
    else:
        from seamless_re.pipeline import process
        i = 0
        for text, url in zip(filings, urls):
            data= process(text,url, ticker, index= i)
            i += 1
            data_load.populate_database(db, input=data, ticker=ticker)
    return render_template('index.html')

@app.route('/query')
def query():
    return render_template('query.html')

@app.route("/get-graph", methods=["POST"])
def get_graph():
    db = Memgraph()
    response = make_response(
        jsonify(db_operations.get_graph(db)), 200)
    return response

@app.route('/get-orgs', methods=["POST"])
def get_users():
    db = Memgraph()
    response = make_response(
        jsonify(db_operations.get_orgs(db)), 200)
    return response

@app.route('/get-relationships', methods=["POST"])
def get_relationships():
    db = Memgraph()
    response = make_response(
        jsonify(db_operations.get_relationships(db)), 200)
    return response
