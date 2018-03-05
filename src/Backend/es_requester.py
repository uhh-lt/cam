import requests
import json
import constants


def request_es(objA, objB):
    '''
    Sends a request to Elastic Search and returns the result as a JSON object.

    objA:   String
            an object to be searched via Elastic Search

    objB:   String
            another object to be searched via Elastic Search

    aspect: String
            a specific aspect that plays a special role while analyzing the result.
            Note that this is currently WIP and not actually implemented.
    '''
    url = build_object_urlpart(objA, objB)
    url = add_marker_urlpart(url)
    return requests.get(url)


def extract_sentences(es_json):
    '''
    Extracts the sentences from an Elastic Search commoncrawl2 json result.

    es_json:    Dictionary
                the JSON object resulting from Elastic Search commoncrawl2
    '''
    hits = es_json.json()['hits']['hits']
    sentences = {}
    for i in range(0, len(hits)):
        sentences[hits[i]['_source']
                  ['text'].lower()] = hits[i]['_score']
    return sentences


def build_object_urlpart(objA, objB):
    '''
    Builds the part of the URL containing the host name, the Elastic Search type and the objects to look for.

    objA:   String
            an object to be searched via Elastic Search

    objB:   String
            another object to be searched via Elastic Search

    aspect: String
            a specific aspect that plays a special role while analyzing the result.
            Note that this is currently WIP and not actually implemented.
    '''
    url = constants.ES_HOSTNAME  # name of the host
    url += constants.CRAWL_DATA_REPOS  # Elastic Search commoncrawl2
    url += '{}%20AND%20{}'.format(
        objA.name, objB.name)  # add the objects to look for
    return url


def add_marker_urlpart(url):
    '''
    Adds to an existing Elastic Search URL part the markers that shall compare the objects.

    url:    String
            a URL containing an Elastic Search command
    '''
    url += '%20AND%20('
    # markers are separated with OR
    for i in range(0, len(constants.MARKERS_WO_THAN)):
        url += constants.MARKERS_WO_THAN[i]
        url += '%20OR%20'
    for i in range(0, len(constants.MARKERS_THAN)):
        url += '('
        url += constants.MARKERS_THAN[i]
        url += '%20AND%20than)%20OR%20'
    for i in range(0, len(constants.MARKERS_THAN)):
        url += '(\"'
        url += constants.MARKERS_THAN[i]
        url += '%20alternative%20to\")%20OR%20'
    for i in range(0, len(constants.MARKERS_THAN) - 1):
        url += '(\"'
        url += constants.MARKERS_THAN[i]
        url += '%20then\")%20OR%20'
    url += '(\"'
    url += constants.MARKERS_THAN[len(constants.MARKERS_THAN) - 1]
    url += '%20then\"))&from=0&size=10000'
    return url
