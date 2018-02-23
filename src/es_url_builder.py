import constants


def build_object_urlpart(objA, objB, aspect):
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
    url = constants.HOSTNAME  # name of the host
    url += constants.ESCC2  # Elastic Search commoncrawl2
    url += '{}%20AND%20{}'.format(
        objA, objB)  # add the objects to look for
    return url


def add_marker_urlpart(url):
    '''
    Adds to an existing Elastic Search URL part the markers that shall compare the objects.

    url:    String
            a URL containing an Elastic Search command
    '''
    url += '%20AND%20('
    # markers are separated with OR
    for i in range(0, len(constants.MARKERS) - 1):
        url += constants.MARKERS[i]
        url += '%20OR%20'
    url += constants.MARKERS[len(constants.MARKERS) - 1]
    url += ')&from=0&size=1000'
    return url
