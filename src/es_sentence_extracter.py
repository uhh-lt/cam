import json


def extract_sentences(es_json):
    '''
    Extracts the sentences from an Elastic Search commoncrawl2 json result.

    es_json:    Dictionary
                the JSON object resulting from Elastic Search commoncrawl2
    '''
    hits = es_json.json()['hits']['hits']
    sentences = []
    for i in range(0, len(hits)):
        sentences.append(hits[i]['_source']['text'].lower())
    return sentences