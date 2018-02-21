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
    url += ')&from=0&size=1000'
    print(url)
    return url

betterMarkers = ['better', 'easier', 'faster', 'nicer', 'wiser', 'cooler', 'decent', 'safer', 'superior', 'solid', 'terrific']
worseMarkers = ['worse', 'harder', 'slower', 'poorly', 'uglier', 'poorer', 'lousy', 'nastier', 'inferior', 'mediocre']

def is_better_than(sentence, objA, objB):
    '''
    Analyzes a sentence that contains two given objects. Returns objA, if the sentence
    suggests that objA is "better" than objB, objB if it suggests the opposite and
    False if the sentence doesn't suggest a clear answer.

    sentence:   String
                the sentence to is_better_than. Has to contain objA and objB.
    objA:       String
                the first object to be compared to the second.
    objB:       String
                the second object to be compared to the first.
    '''
    aPos = sentence.find(objA) #position of objectA in sentence
    bPos = sentence.find(objB) #position of objectB in sentence
    if aPos < bPos:
        n = sentence.find('not', aPos, bPos) #looks for a 'not' between A and B
    else:
        n = sentence.find('not', bPos, aPos) #looks for a 'not' between B and A
    for s in betterMarkers: #look for a betterMarker
        pos = sentence.find(s)
        if pos != -1: #found a betterMarker in sentence
            if (pos < aPos and pos > bPos): #betterMarker is between B and A
                if n != -1: #a 'not' exists between the objects
                    return True
                else:
                    return False
            elif (pos > aPos and pos < bPos): #betterMarker is between A and B
                if n != -1: #a 'not' exists between the objects
                    return False
                else:
                    return True
    for s in worseMarkers: #look for a worseMarker
        pos = sentence.find(s)
        if pos != -1: #found a worseMarker in sentence
            if (pos < aPos and pos > bPos): #worseMarker is between B and A
                if n != -1: #a 'not' exists between the objects
                    return False
                else:
                    return True
            elif (pos > aPos and pos < bPos): #worseMarker is between A and B
                if n != -1: #a 'not' exists between the objects
                    return True
                else:
                    return False
    return None #no better or worse marker was found between both objects

negRemovers = ['didn\'t', 'couldn\'t', 'wasn\'t', 'haven\'t', 'wouldn\'t', 
'did not', 'could not', 'was not', 'have not', 'would not', 
'didnt', 'couldnt', 'wasnt', 'havent', 'wouldnt']

def clearSentences(sentences):
    for s in sentences:
        if '?' in s:
            sentences.remove(s)
        else:
            for neg in negRemovers:
                if neg in s:
                    sentences.remove(s)
                    break
    return sentences