import json
import numbers
import sys
import urllib
import query_sentences
import extract_candidates
import filter_candidates_wordnet
import query_sentences
import sklearn
from flask import Flask, jsonify, request
from flask_cors import CORS
from requests.auth import HTTPBasicAuth

from marker_approach.object_comparer import find_winner
from ml_approach.classify import (classify_sentences, evaluate,
                                  set_use_heuristics)
from ml_approach.sentence_preparation_ML import prepare_sentence_DF
from utils.es_requester import (extract_sentences, request_context_sentences,
                                request_document_by_id, request_es,
                                request_es_ML, request_es_triple,
                                request_keyword_query)
from utils.objects import Argument, Aspect
from utils.sentence_clearer import clear_sentences, remove_questions
from utils.sentence_context_getter import get_sentence_context
from utils.url_builder import set_index

app = Flask(__name__)
CORS(app)


@app.route("/")
def helloWorld():
  return "Hello, cross-origin-world!"

@app.route("/ccrr/<objectA>")
def helloCcrWorld(objectA):
  return "Hello, ccr!" + objectA

@app.route('/ccr/<objectA>', methods=['GET'])
def ccr(objectA):
    '''
    To bi visited after the keyUp event in first-object-input-field.
    '''
    comparison_object = objectA.lower().strip()
    # sentences is a list with sentenses that contain the comparison_object AND vs
    
    sentences = query_sentences.retrieve_sentences(comparison_object)
    # candidates are sentences that match the pattern 'comparison_object vs <nounphrase>' or the other way around
    candidates = extract_candidates.extract_candidates(comparison_object, sentences)

    wordnet_filtered_candidates = filter_candidates_wordnet.filter(comparison_object, candidates)
    
    # append comparison object and 'vs' to suggestions to get the same format as suggestions from the keyword tool
    ccr_suggestions_all = []
    
    print(ccr_suggestions_all)

    for candidate in wordnet_filtered_candidates:
        ccr_suggestions_all.append(comparison_object + ' vs ' + candidate)
    # top ten results from ccr
    ccr_suggestions_top = ccr_suggestions_all[0:7]
    # remove the comparison_object and ' vs ' from suggestions
    ccr_suggestions_top = [suggestion[(len(comparison_object) + 4):] for suggestion in ccr_suggestions_top]

    print('Done with ', comparison_object, '!')
    return jsonify(ccr_suggestions_top)

@app.route('/cam', methods=['GET'])
def cam():
    '''
    to be visited after a user clicked the 'compare' button.
    '''
    load_config()

    fast_search = request.args.get('fs')
    obj_a = Argument(request.args.get('objectA').lower().strip())
    obj_b = Argument(request.args.get('objectB').lower().strip())
    aspects = extract_aspects(request)
    model = request.args.get('model')
    statusID = request.args.get('statusID')

    if model == 'default' or model is None:
        # json obj with all ES hits containing obj_a, obj_b and a marker.
        setStatus(statusID, 'Request ES')
        json_compl = request_es(fast_search, obj_a, obj_b)

        # list of all sentences containing obj_a, obj_b and a marker.
        setStatus(statusID, 'Extract sentences')
        all_sentences = extract_sentences(json_compl)

        # removing sentences that can't be properly analyzed
        setStatus(statusID, 'Clear sentences')
        all_sentences = clear_sentences(all_sentences, obj_a, obj_b)

        # find the winner of the two objects
        setStatus(statusID, 'Find winner')
        return jsonify(find_winner(all_sentences, obj_a, obj_b, aspects))

    else:
        setStatus(statusID, 'Request all sentences containing the objects')
        if aspects:
            json_compl_triples = request_es_triple(obj_a, obj_b, aspects)
        json_compl = request_es_ML(fast_search, obj_a, obj_b)

        setStatus(statusID, 'Extract sentences')
        if aspects:
            all_sentences = extract_sentences(json_compl_triples)
            all_sentences.extend([sentence for sentence in extract_sentences(
                json_compl) if sentence.text not in [sentence.text for sentence in all_sentences]])
        else:
            all_sentences = extract_sentences(json_compl)

        if len(all_sentences) == 0:
            return jsonify(find_winner(all_sentences, obj_a, obj_b, aspects))

        remove_questions(all_sentences)

        setStatus(statusID, 'Prepare sentences for classification')
        prepared_sentences = prepare_sentence_DF(all_sentences, obj_a, obj_b)

        setStatus(statusID, 'Classify sentences')
        classification_results = classify_sentences(prepared_sentences, model)

        setStatus(statusID, 'Evaluate classified sentences; Find winner')
        final_dict = evaluate(all_sentences, prepared_sentences,
                              classification_results, obj_a, obj_b, aspects)

        return jsonify(final_dict)


@app.route('/status', methods=['GET'])
@app.route('/cam/status', methods=['GET'])
def getStatus():
    statusID = request.args.get('statusID')
    return jsonify(status[statusID])


@app.route('/remove/status', methods=['DELETE'])
@app.route('/cam/remove/status', methods=['DELETE'])
def removeStatus():
    statusID = request.args.get('statusID')
    print('Remove registered:', statusID)
    del status[statusID]
    return jsonify(True)


@app.route('/register', methods=['GET'])
@app.route('/cam/register', methods=['GET'])
def register():
    statusID = str(len(status))
    setStatus(statusID, '')
    print('Register:', statusID)
    return jsonify(statusID)


@app.route('/context', methods=['GET'])
@app.route('/cam/context', methods=['GET'])
def get_context():
    document_id = urllib.parse.quote(request.args.get('documentID'))
    sentence_id = request.args.get('sentenceID')
    context_size = request.args.get('contextSize')
    return jsonify(get_sentence_context(document_id, sentence_id, context_size))

@app.route('/search')
@app.route('/cam/search', methods=['GET'])
def search():
    query = request.args.get('query')
    es_json = request_keyword_query(query, 500)
    sentences = extract_sentences(es_json)
    return jsonify([sentence.__dict__ for sentence in sentences])


def setStatus(statusID, statusText):
    if statusID != None:
        status[statusID] = statusText


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


def load_config():
    with open('config.json') as json_data_file:
        config = json.load(json_data_file)
    set_index(config['index']['name'])
    set_use_heuristics(config['use_heuristics'] == 'True')


if __name__ == "__main__":
    status = {}
    load_config()
    app.run()
    #app.run(host="0.0.0.0", threaded=True)
