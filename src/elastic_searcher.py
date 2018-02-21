import requests
import json

markers = ['better', 'easier', 'faster', 'nicer', 'wiser', 'cooler', 'decent', 'safer', 'superior', 'solid', 
'terrific', 'worse', 'harder', 'slower', 'poorly', 'uglier', 'poorer', 'lousy', 'nastier', 'inferior', 'mediocre']

def req(objA, objB, aspect):
    url = buildString(objA, objB, aspect)
    r = requests.get(url)
    print(r.text)
    hits = r.json()['hits']['hits']
    sentences = []
    for i in range(0, len(hits)):
        sentences.append(hits[i]['_source']['text'])
    return sentences

def buildString(objA, objB, aspect):
    url = 'http://localhost:9222/commoncrawl2/_search?q=text:{}%20AND%20{}%20AND%20('.format(objA, objB)
    for i in range(0, len(markers) - 1):
        url += markers[i]
        url += '%20OR%20'
    url += markers[len(markers) - 1]
    url += ')&from=0&size=100'
    print(url)
    return url