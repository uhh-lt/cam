import os
import sys

import requests
from requests.auth import HTTPBasicAuth

from utils.objects import Sentence
from utils.url_builder import build_object_urlpart, add_marker_urlpart, build_context_url, build_document_getter_url, \
    get_query_range, build_keyword_search_url


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
    url += ')' + get_query_range(10000)
    return send_request(url)


def request_es_ML(fast_search, obj_a, obj_b):
    url = build_object_urlpart(obj_a, obj_b)

    size = 10000
    if fast_search == 'true':
        size = 500
    url += get_query_range(size)
    return send_request(url)


def request_keyword_query(query, size):
    url = build_keyword_search_url(query, size)
    return send_request(url)


def send_request(url, method="GET"):
    if len(sys.argv) >= 2:
        return requests.request(method, url, auth=HTTPBasicAuth(sys.argv[1], sys.argv[2]))
    elif os.getenv("ES_USERNAME") and os.getenv("ES_PASSWORD"):
        return requests.request(method, url, auth=HTTPBasicAuth(os.getenv("ES_USERNAME"), os.getenv("ES_PASSWORD")))
    else:
        return requests.request(method, url)


def extract_sentences(es_json, aggregate_duplicates=True):
    '''
    Extracts the sentences from an Elastic Search commoncrawl2 json result. (This is the default
    and can be changed in constants.py)

    es_json:    Dictionary
                the JSON object resulting from Elastic Search commoncrawl2
    '''
    try:
        hits = es_json.json()['hits']['hits']
    except KeyError:
        return []
    sentences = []
    seen_sentences = set()
    for hit in hits:
        source = hit['_source']
        text = source['text']
        document_id = source['document_id'] if 'document_id' in source else ''
        sentence_id = source['sentence_id'] if 'sentence_id' in source else ''

        if prepare_sentence_comparison(text) in seen_sentences:
            if aggregate_duplicates:
                for x in sentences:
                    if prepare_sentence_comparison(x.text) == prepare_sentence_comparison(text):
                        if document_id not in x.id_pair:
                            x.add_id_pair(document_id, sentence_id)
                        elif document_id in x.id_pair and x.id_pair[document_id] > sentence_id:
                            x.id_pair[document_id] = sentence_id
                        break
        else:
            seen_sentences.add(prepare_sentence_comparison(text))
            sentences.append(
                Sentence(text, hit['_score'], document_id, sentence_id))

    return sentences


def prepare_sentence_comparison(sentence):
    return sentence.lower()
    # return re.sub('[^A-Za-z0-9]+', '', sentence).lower()
    # return ''.join(e for e in sentence if e.isalnum()).lower()


def request_context_sentences(document_id, sentence_id, context_size):
    url = build_context_url(document_id, sentence_id,
                            context_size) + get_query_range(10000)
    return send_request(url)


def request_document_by_id(document_id):
    url = build_document_getter_url(document_id) + get_query_range(10000)
    return send_request(url)
