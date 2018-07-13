import requests
import sys
from requests.auth import HTTPBasicAuth
import json
from utils.url_builder import build_object_urlpart, add_marker_urlpart


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
    if(len(sys.argv) > 1):
        return requests.get(url, auth=HTTPBasicAuth(sys.argv[1], sys.argv[2]))
    else: 
        return requests.get(url)

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

    payload =  {}
    if(len(sys.argv) > 1):
        return requests.get(url, params=payload, auth=HTTPBasicAuth(sys.argv[1], sys.argv[2]))
    else: 
        return requests.get(url)

def request_es_ML(fast_search, obj_a, obj_b):
    url = build_object_urlpart(obj_a, obj_b)

    size = 10000
    if fast_search == 'true':
        size = 500
    url += '&from=0&size={}'.format(size)

    payload =  {}
    if(len(sys.argv) > 1):
        return requests.get(url, params=payload, auth=HTTPBasicAuth(sys.argv[1], sys.argv[2]))
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
    sentences = {}
    for i in range(0, len(hits)):
        sentences[hits[i]['_source']['text'].lower()] = hits[i]['_score']
    return sentences



