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
    Route to be visited after a user clicked the 'compare' button.
    '''
    objectA = request.args.get('objectA').lower()
    objectB = request.args.get('objectB').lower()
    aspect = request.args.get('aspect').lower()
    # json obj with all ES hits containing objectA, objectB and a marker.
    all_hits = es_requester.request_es(objectA, objectB, aspect)
    # list of all sentences containing objectA, objectB and a marker.
    all_sentences = es_sentence_extracter.extract_sentences(all_hits)
    # removing sentences that can't be properly analyzed
    all_sentences = sentence_clearer.clear_sentences(all_sentences)
    # find the winner of the two objects
    result = object_comparer.find_winner(all_sentences, objectA, objectB)
    return json.dumps(result)


if __name__ == "__main__":
    app.run()
