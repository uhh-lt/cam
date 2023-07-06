import urllib.parse
import os

from flask import Flask, jsonify, request
from flask_cors import CORS
# from flask_wtf.csrf import CSRFProtect

import extract_candidates
import filter_candidates_wordnet
import query_sentences
from marker_approach.object_comparer import find_winner
from ml_approach.classify import (classify_sentences, evaluate)
from ml_approach.sentence_preparation_ML import prepare_sentence_DF
from utils.es_requester import (extract_sentences, request_es,
                                request_es_ML, request_es_triple,
                                request_keyword_query, send_request)
from utils.objects import Argument, Aspect
from utils.sentence_clearer import clear_sentences, remove_questions
from utils.sentence_context_getter import get_sentence_context
from utils.url_builder import build_url_suggestions

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
CORS(app)
# csrf = CSRFProtect(app)

# @app.before_request
# def csrf_protect():
#     if request.method == 'POST':
#         csrf.protect()

# @app.route('/cam/csrf-token', method=['GET'])
# def get_csrf_tpken():
#     token = csrf.generate_scrf()
#     response = jsonify({'csrf_token': token})
#     return response

# @app.after_request
# def after_request(response):
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#     response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
#     return response

@app.route("/")
def home():
    return cam()

@app.route("/suggestions", methods = ['POST', 'GET'])
def suggestions_proxy():
    """
    Proxy suggestions requests to Elasticsearch and authenticate.
    This proxy should be used by the frontend to query suggestions,
    as it should not store Elasticsearch credentials itself.
    """
    return send_request(build_url_suggestions() + "?" + request.query_string, method=request.method)


@app.route("/ccrr/<object_a>")
def hello_ccr_world(object_a):
    return "Hello, ccr!" + object_a


@app.route('/ccr/<object_a>', methods=['GET'])
def ccr(object_a):
    """
    To bi visited after the keyUp event in first-object-input-field.
    """
    comparison_object = object_a.lower().strip()
    # sentences is a list with sentenses that contain the comparison_object AND vs

    sentences = query_sentences.retrieve_sentences(comparison_object)
    # candidates are sentences that match the pattern 'comparison_object vs <nounphrase>' or the other way around
    candidates = extract_candidates.extract_candidates(comparison_object, sentences)

    wordnet_filtered_candidates = filter_candidates_wordnet.filter_candidates(comparison_object, candidates)

    # append comparison object and 'vs' to suggestions to get the same format as suggestions from the keyword tool
    ccr_suggestions_all = []

    print(ccr_suggestions_all)

    for candidate in wordnet_filtered_candidates:
        ccr_suggestions_all.append(comparison_object + ' vs ' + candidate)
    # top seven results from ccr
    ccr_suggestions_top = ccr_suggestions_all[0:7]
    # remove the comparison_object and ' vs ' from suggestions
    ccr_suggestions_top = [suggestion[(len(comparison_object) + 4):] for suggestion in ccr_suggestions_top]

    print('Done with ', comparison_object, '!')
    return jsonify(ccr_suggestions_top)

# @app.route("/")
@app.route('/cam', methods=['GET'])
def cam():
    """
    to be visited after a user clicked the 'compare' button.
    """
    fast_search = request.args.get('fs')
    obj_a = Argument(request.args.get('objectA').lower().strip())
    obj_b = Argument(request.args.get('objectB').lower().strip())
    aspects = extract_aspects(request)
    model = request.args.get('model')
    statusID = request.args.get('statusID')

    if model == 'default' or model is None:
        # json obj with all ES hits containing obj_a, obj_b and a marker.
        set_status(statusID, 'Request ES')
        json_compl = request_es(fast_search, obj_a, obj_b)

        # list of all sentences containing obj_a, obj_b and a marker.
        set_status(statusID, 'Extract sentences')
        all_sentences = extract_sentences(json_compl)

        # removing sentences that can't be properly analyzed
        set_status(statusID, 'Clear sentences')
        all_sentences = clear_sentences(all_sentences, obj_a, obj_b)

        # find the winner of the two objects
        set_status(statusID, 'Find winner')
        return jsonify(find_winner(all_sentences, obj_a, obj_b, aspects))

    else:
        set_status(statusID, 'Request all sentences containing the objects')
        if aspects:
            json_compl_triples = request_es_triple(obj_a, obj_b, aspects)
        else:
            json_compl_triples = []
        json_compl = request_es_ML(fast_search, obj_a, obj_b)

        set_status(statusID, 'Extract sentences')
        if aspects:
            all_sentences = extract_sentences(json_compl_triples)
            all_sentences.extend([sentence for sentence in extract_sentences(
                json_compl) if sentence.text not in [sentence.text for sentence in all_sentences]])
        else:
            all_sentences = extract_sentences(json_compl)

        if len(all_sentences) == 0:
            return jsonify(find_winner(all_sentences, obj_a, obj_b, aspects))

        remove_questions(all_sentences)

        set_status(statusID, 'Prepare sentences for classification')
        prepared_sentences = prepare_sentence_DF(all_sentences, obj_a, obj_b)

        set_status(statusID, 'Classify sentences')
        classification_results = classify_sentences(prepared_sentences, model)

        set_status(statusID, 'Evaluate classified sentences; Find winner')
        final_dict = evaluate(all_sentences, prepared_sentences,
                              classification_results, obj_a, obj_b, aspects)

        return jsonify(final_dict)


@app.route('/status', methods=['GET'])
@app.route('/cam/status', methods=['GET'])
def get_status():
    statusID = request.args.get('statusID')
    return jsonify(status[statusID])


@app.route('/remove/status', methods=['DELETE'])
@app.route('/cam/remove/status', methods=['DELETE'])
def remove_status():
    statusID = request.args.get('statusID')
    print('Remove registered:', statusID)
    del status[statusID]
    return jsonify(True)


@app.route('/register', methods=['GET'])
@app.route('/cam/register', methods=['GET'])
def register():
    statusID = str(len(status))
    set_status(statusID, '')
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


def set_status(status_id, status_text):
    if status_id is not None:
        status[status_id] = status_text


def extract_aspects(req):
    aspects = []
    i = 1
    while i is not False:
        asp = 'aspect{}'.format(i)
        wght = 'weight{}'.format(i)
        inputasp = req.args.get(asp)
        inputwght = req.args.get(wght)
        if inputasp is not None and inputwght is not None:
            asp = Aspect(inputasp.lower(), int(inputwght))
            aspects.append(asp)
            i += 1
        else:
            i = False
    return aspects


if __name__ == "__main__":
    status = {}
    app.run(host="0.0.0.0", port=5000, threaded=True)
