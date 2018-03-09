import requests
import json
from es_requester import request_es, extract_sentences
from sentence_clearer import clear_sentences
from object_comparer import find_winner
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
@app.route('/cam', methods=['GET'])
def cam():
    '''
    to be visited after a user clicked the 'compare' button.
    '''
    fast_search = request.args.get('fs')
    obj_a = Argument(request.args.get('objectA').lower().strip())
    obj_b = Argument(request.args.get('objectB').lower().strip())
    aspects = []
    i = 1
    while i is not False:
        asp = 'aspect'
        asp += str(i)
        wght = 'weight'
        wght += str(i)
        inputasp = request.args.get(asp)
        inputwght = request.args.get(wght)
        if inputasp is not None and inputwght is not None:
            asp = Aspect(inputasp.lower(), int(inputwght))
            aspects.append(asp)
            i += 1
        else:
            i = False
    # json obj with all ES hits containing obj_a, obj_b and a marker.
    json_compl = request_es(fast_search, obj_a, obj_b)
    # list of all sentences containing obj_a, obj_b and a marker.
    all_sentences = extract_sentences(json_compl)
    # removing sentences that can't be properly analyzed
    all_sentences = clear_sentences(all_sentences, obj_a, obj_b)
    # find the winner of the two objects
    final_dict = find_winner(all_sentences, obj_a, obj_b, aspects)
    return jsonify(final_dict)


class Argument:
    '''
    Argument Class for the objects to be compared
    '''

    def __init__(self, name):
        self.name = name.lower()
        self.points = 0
        self.sentences = []

    def add_points(self, points):
        self.points += points

    def add_sentence(self, sentence):
        self.sentences.append(sentence)


class Aspect:
    '''
    Aspect Class for the user entered aspects
    '''

    def __init__(self, name, weight):
        self.name = name.lower()
        self.weight = weight


if __name__ == "__main__":
    app.run(host="0.0.0.0")
