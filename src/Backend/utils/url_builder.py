from marker_approach.constants import MARKERS_WO_THAN, MARKERS_THAN
import re

# ES_HOSTNAME = 'http://localhost:9200/'  # if you want to connect to a locally hosted ES
ES_HOSTNAME = 'http://ltdemos.informatik.uni-hamburg.de/depcc-index/'
# Elastic Search commoncrawl2 search request
INDEX = 'commoncrawl2'
CRAWL_DATA_REPOS = '/_search?q='
lucene_special_characters = ["+", "-", "=", "&&", "||", ">", "<", "!", "(", ")", "{", "}", "[", "]", "^", '"', "~", "*", "?", ":", "\\", "/"]


def escape_query_part(query_part):
    for special in lucene_special_characters:
       query_part = re.sub(re.escape(special),"\\" + special, query_part)
    return query_part

def build_url_base():
    return ES_HOSTNAME + INDEX + CRAWL_DATA_REPOS

def build_context_url(document_id, sentence_id, context_size):
    return build_document_getter_url(document_id) + ' AND sentence_id:[{} TO {}]'.format(sentence_id - context_size, sentence_id + context_size)

def build_document_getter_url(document_id):
    return build_url_base() + 'document_id:\"{}\"'.format(escape_query_part(document_id))

def get_query_range(maximum):
    return '&from=0&size={}'.format(maximum)

def build_keyword_search_url(query, size):
    return build_url_base() + 'text:({})&from=0&size={}'.format(query, size)


def build_object_urlpart(obj_a, obj_b):
    '''
    Builds the part of the URL containing the host name, the Elastic Search type and the objects to look for.

    obj_a:   String
            an object to be searched via Elastic Search

    obj_b:   String
            another object to be searched via Elastic Search
    '''
    if(obj_a.name == '' or obj_b.name == ''):
        raise ValueError('Please enter both objects!')
    url=build_url_base() + 'text:\"{}\"%20AND%20\"{}\"'.format(obj_a.name, obj_b.name)
    return url


def add_marker_urlpart(url, fast_search):
    '''
    Adds to an existing Elastic Search URL part the markers that shall compare the objects.

    url:    String
            a URL containing an Elastic Search command
    '''
    url += '%20AND%20('
    # markers are separated with OR
    for i in range(0, len(MARKERS_WO_THAN)):
        url += MARKERS_WO_THAN[i]
        url += '%20OR%20'
    for i in range(0, len(MARKERS_THAN)):
        url += '(\"'
        url += MARKERS_THAN[i]
        url += '\"%20AND%20than)%20OR%20'
    for i in range(0, len(MARKERS_THAN)):
        url += '(\"'
        url += MARKERS_THAN[i]
        url += '%20alternative%20to\")%20OR%20'
    for i in range(0, len(MARKERS_THAN) - 1):
        url += '(\"'
        url += MARKERS_THAN[i]
        url += '%20then\")%20OR%20'
    url += '(\"'
    url += MARKERS_THAN[len(MARKERS_THAN) - 1]
    if fast_search == 'false':
        url += '%20then\"))' + get_query_range(10000)
    else:
        url += '%20then\"))' + get_query_range(500)
    return url


def set_index(index):
    global INDEX
    INDEX=index
