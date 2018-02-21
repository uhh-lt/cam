import requests

markers = ['better', 'easier', 'faster', 'nicer', 'wiser', 'cooler', 'decent', 'safer', 'superior', 'solid', 'terrific', 'worse', 'harder', 'slower', 'poorly', 'uglier', 'poorer', 'lousy', 'nastier', 'inferior', 'mediocre']

def req(objA, objB):
    url = buildString(objA, objB)
    r = requests.get(url)
    hits = r.json()['hits']['hits']
    sentences = []
    for i in range(0, len(hits) - 1):
        sentences.append(hits[i]['_source']['text'])
    return sentences

def buildString(objA, objB):
    url = 'http://localhost:9222/commoncrawl2/_search?q=text:'
    url += objA
    url += '%20AND%20'
    url += objB
    url += '%20AND%20('
    for i in range(0, len(markers) - 2):
        url += markers[i]
        url += '%20OR%20'
    url += markers[len(markers) - 1]
    url += ')&from=0&size=10'
    return url