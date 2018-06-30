import requests
import json
from es_requester import request_es, extract_sentences, request_es_ML, request_es_triple
import sentence_clearer 
from sentence_preparation_ML import prepare_sentence_DF
from classify import classify_sentences, evaluate
from object_comparer import find_winner
from flask import Flask, request, jsonify
from flask_cors import CORS
import sklearn


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
    aspects = extract_aspects(request)
    
    global status
    # json obj with all ES hits containing obj_a, obj_b and a marker.
    status = 'Request ES'
    json_compl = request_es(fast_search, obj_a, obj_b)

    # list of all sentences containing obj_a, obj_b and a marker.
    status = 'Extract sentences'
    all_sentences = extract_sentences(json_compl)

    # removing sentences that can't be properly analyzed
    status = 'Clear sentences'
    all_sentences = sentence_clearer.clear_sentences(all_sentences, obj_a, obj_b)

    # find the winner of the two objects
    status = 'Find winner'
    final_dict = find_winner(all_sentences, obj_a, obj_b, aspects)

    return jsonify(final_dict)

@app.route('/ml', methods=['GET'])
@app.route('/cam/ml', methods=['GET'])
def cam_ml():
    fast_search = request.args.get('fs')
    model = request.args.get('model')
    obj_a = Argument(request.args.get('objectA').lower().strip())
    obj_b = Argument(request.args.get('objectB').lower().strip())
    aspects = extract_aspects(request)

    global status
    status = 'Request all sentences containing the objects'
    if aspects:
        json_compl_triples = request_es_triple(obj_a, obj_b, aspects)
    json_compl = request_es_ML(fast_search, obj_a, obj_b)

    status = 'Extract sentences'
    if aspects:
        all_sentences = extract_sentences(json_compl_triples)
        all_sentences.update(extract_sentences(json_compl))
    else:
        all_sentences = extract_sentences(json_compl)

    sentence_clearer.remove_questions(all_sentences)

    status = 'Prepare sentences for classification'
    prepared_sentences = prepare_sentence_DF(all_sentences, obj_a, obj_b)

    status = 'Classify sentences'
    classification_results = classify_sentences(prepared_sentences, model)

    status = 'Evaluate classified sentences; Find winner'
    final_dict = evaluate(all_sentences, prepared_sentences, classification_results, obj_a, obj_b, aspects)

    return jsonify(final_dict)

@app.route('/status')
@app.route('/cam/status')
def getStatus():
    return jsonify(status)

def extract_aspects(request):
    aspects = []
    i = 1
    while i is not False:
        asp = 'aspect{}'.format(i)
        wght = 'weight{}'.format(i)
        inputasp = request.args.get(asp)
        inputwght = request.args.get(wght)
        if inputasp is not None and inputwght is not None:
            asp = Aspect(inputasp.lower(), int(inputwght))
            aspects.append(asp)
            i += 1
        else:
            i = False
    return aspects

class Argument:
    '''
    Argument Class for the objects to be compared
    '''

    def __init__(self, name):
        self.name = name.lower()
        self.points = {}
        self.totalPoints = 0
        self.sentences = {}

    def add_points(self, aspect, points):
        self.totalPoints = self.totalPoints + points
        if aspect in self.points:
            self.points[aspect] = self.points[aspect] + points
        else:
            self.points[aspect] = points

    def add_sentence(self, aspect, sentence):
        if aspect in self.sentences:
            self.sentences[aspect].append(sentence)
        else:
            self.sentences[aspect] = [sentence]

class Aspect:
    '''
    Aspect Class for the user entered aspects
    '''

    def __init__(self, name, weight):
        self.name = name.lower()
        self.weight = weight


if __name__ == "__main__":
    status = ''
    app.run(host="0.0.0.0", threaded=True)
