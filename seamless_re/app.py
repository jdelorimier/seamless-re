from flask import Flask, render_template, jsonify, make_response
from seamless_re.database import Memgraph
from seamless_re import db_operations

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    db = Memgraph()
    db_operations.clear(db)
    db_operations.populate_database(db, "seamless_re/resources/data_big.txt")
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

@app.route('/get-users', methods=["POST"])
def get_users():
    db = Memgraph()
    response = make_response(
        jsonify(db_operations.get_users(db)), 200)
    return response

@app.route('/get-relationships', methods=["POST"])
def get_relationships():
    db = Memgraph()
    response = make_response(
        jsonify(db_operations.get_relationships(db)), 200)
    return response
