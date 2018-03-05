import requests
import json
import es_requester
import sentence_clearer
import object_comparer
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
    objectA = Argument(request.args.get('objectA').lower().strip())
    objectB = Argument(request.args.get('objectB').lower().strip())
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
    # json obj with all ES hits containing objectA, objectB and a marker.
    json_compl = es_requester.request_es(objectA, objectB)
    # list of all sentences containing objectA, objectB and a marker.
    all_sentences = es_requester.extract_sentences(json_compl)
    # removing sentences that can't be properly analyzed
    all_sentences = sentence_clearer.clear_sentences(
        all_sentences, objectA, objectB)
    # find the winner of the two objects
    final_dict = object_comparer.find_winner(
        all_sentences, objectA, objectB, aspects)
    return jsonify(final_dict)


class Argument:
    '''
    Argument Class
    '''

    def __init__(self, name):
        self.name = name
        self.points = 0
        self.sentences = []

    def add_points(self, points):
        self.points += points

    def add_sentence(self, sentence):
        self.sentences.append(sentence)


class Aspect:
    '''
    Aspect Class
    '''

    def __init__(self, name, weight):
        self.name = name
        self.weight = weight


if __name__ == "__main__":
    app.run()
