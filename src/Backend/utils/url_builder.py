from marker_approach.constants import MARKERS_WO_THAN, MARKERS_THAN

# ES_HOSTNAME = 'http://localhost:9200/'  # if you want to connect to a locally hosted ES
ES_HOSTNAME = 'http://ltdemos.informatik.uni-hamburg.de/depcc-index/'
# Elastic Search commoncrawl2 search request
CRAWL_DATA_REPOS = 'depcc/_search?q=text:'


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
    url = ES_HOSTNAME  # name of the host
    url += CRAWL_DATA_REPOS  # Elastic Search request type
    # add the objects to look for
    url += '\"{}\"%20AND%20\"{}\"'.format(obj_a.name, obj_b.name)
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
        url += '%20then\"))&from=0&size=10000'
    else:
        url += '%20then\"))&from=0&size=500'
    return url