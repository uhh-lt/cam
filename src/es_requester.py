import requests
import es_url_builder


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
    url = es_url_builder.build_object_urlpart(objA, objB)
    url = es_url_builder.add_marker_urlpart(url)
    return requests.get(url)
