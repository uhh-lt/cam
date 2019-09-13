import requests
import sys
from requests.auth import HTTPBasicAuth
import json


# return a list with sentenses that contain the comparison_object AND vs
def retrieve_sentences(comparison_object, vs='vs'):
    url = build_url(comparison_object, vs)
    print(url)
    if(len(sys.argv) > 1):
        es_json = requests.get(url, auth=HTTPBasicAuth(sys.argv[1], sys.argv[2]))
    else:
        es_json = requests.get(url)

    sentences = extract_sentences(es_json)
    return sentences


def build_url(comparison_object, vs):
    esHostname = 'http://ltdemos.informatik.uni-hamburg.de/depcc-index/'
    index = 'depcc'
    crawlDataRepos = '/_search?q='
    url = esHostname + index + crawlDataRepos + 'text:(\"{}\"%20AND%20\"{}\")&from=0&size=10000'.format(comparison_object, vs)
    return url


def extract_sentences(es_json):
    hits = es_json.json()['hits']['hits']
    sentences = []
    for hit in hits:
        text = hit['_source']['text']
        sentences.append(text)

    return sentences
