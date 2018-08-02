import requests
import sys
from requests.auth import HTTPBasicAuth
import json
from utils.url_builder import build_object_urlpart, add_marker_urlpart, build_context_url
from utils.objects import Sentence


def request_es(fast_search, obj_a, obj_b):
    '''
    Sends a request to Elastic Search and returns the result as a JSON object.

    obj_a:   String
            an object to be searched via Elastic Search

    obj_b:   String
            another object to be searched via Elastic Search
    '''
    url = build_object_urlpart(obj_a, obj_b)
    url = add_marker_urlpart(url, fast_search)
    return send_request(url)


def request_es_triple(obj_a, obj_b, aspects):
    url = build_object_urlpart(obj_a, obj_b)
    url += '%20AND%20('
    first = True
    for aspect in aspects:
        if first:
            url += '\"{}\"'.format(aspect.name)
        else:
            url += '%20OR%20\"{}\"'.format(aspect.name)
    url += ')&from=0&size=10000'
    return send_request(url)


def request_es_ML(fast_search, obj_a, obj_b):
    url = build_object_urlpart(obj_a, obj_b)

    size = 10000
    if fast_search == 'true':
        size = 500
    url += '&from=0&size={}'.format(size)
    return send_request(url)


def send_request(url):
    if(len(sys.argv) > 1):
        return requests.get(url, auth=HTTPBasicAuth(sys.argv[1], sys.argv[2]))
    else:
        return requests.get(url)


def extract_sentences(es_json):
    '''
    Extracts the sentences from an Elastic Search commoncrawl2 json result. (This is the default
    and can be changed in constants.py)

    es_json:    Dictionary
                the JSON object resulting from Elastic Search commoncrawl2
    '''
    hits = es_json.json()['hits']['hits']
    sentences = []
    for hit in hits:
        source = hit['_source']
        document_id = source['document_id'] if 'document_id' in source else ''
        sentence_id = source['sentence_id'] if 'sentence_id' in source else ''
        sentences.append(Sentence(source['text'], hit['_score'], document_id, sentence_id))
    return sentences

def request_context_sentences(document_id, sentence_id, context_size):
    url = build_context_url(document_id, sentence_id, context_size)
    return send_request(url)