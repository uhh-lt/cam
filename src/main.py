import requests
import json
import es_requester
import es_sentence_extracter
import sentence_clearer
import object_comparer
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/")
def com():
    '''
    Main route containing the UI expecting the objects and aspects (WIP).
    '''
    return ('Until the UI is finished, try CAM by opening ../cam?objectA=OBJA&objectB=OBJB&aspect=ASP replacing OBJA, OBJB and ASP with your desired values.')


@app.route('/cam', methods=['GET'])
def cam():
    '''
    to be visited after a user clicked the 'compare' button.
    '''
    objectA = Argument(request.args.get('objectA').lower())
    objectB = Argument(request.args.get('objectB').lower())
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
    all_hits = es_requester.request_es(objectA, objectB)
    # list of all sentences containing objectA, objectB and a marker.
    all_sentences = es_sentence_extracter.extract_sentences(all_hits)
    # removing sentences that can't be properly analyzed
    all_sentences = sentence_clearer.clear_sentences(all_sentences)
    # find the winner of the two objects
    final_dict = object_comparer.find_winner(
        all_sentences, objectA, objectB, aspects)
    return jsonify(final_dict)


class Argument:
    """Argument Class"""

    def __init__(self, name):
        self.name = name
        self.points = 0
        self.sentences = []

    def set_name(self, name):
        self.name = name

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

    def set_name(self, name):
        self.name = name

    def set_weight(self, weight):
        self.weight = weight


if __name__ == "__main__":
    app.run()
