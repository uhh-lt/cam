import requests
import json
import elastic_searcher
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def com():
    return ('Until the UI is finished, try CAM by opening ../cam?objectA=OBJA&objectB=OBJB&aspect=ASP replacing OBJA, OBJB and ASP with your desired values.')

@app.route('/cam', methods=['GET'])
def cam():
    objectA = request.args.get('objectA')
    objectB = request.args.get('objectB')
    aspect = request.args.get('aspect')
    allSentences = elastic_searcher.req(objectA, objectB, aspect) #list of all sentences containing objectA, objectB and a marker.
    allSentences = elastic_searcher.clearSentences(allSentences)
    aPoints = 0 #counts how many times objA won a sentence.
    bPoints = 0 #counts how many times objB won a sentence.
    aSentences = [] #collects all sentences objA has won.
    bSentences = [] #collects all sentences objB has won.
    for s in allSentences:
        result = elastic_searcher.is_better_than(s, objectA, objectB)
        if result is not None: #sentence is usable
            if result: #objectA won the sentence
                aPoints += 1
                aSentences.append(s)
            elif not result: #objectB won the sentence
                bPoints += 1
                bSentences.append(s)
    result = {}
    result ['object 1'] = objectA
    result ['object 2'] = objectB
    result ['score object 1'] = aPoints
    result ['score object 2'] = bPoints
    result ['object a sentences'] = aSentences
    result ['object b sentences'] = bSentences
    return json.dumps(result)
    '''
    printString = 'Our results suggest that ' #result String to be built and to be shown on the website.
    if aPoints > bPoints: #objectA is better.
        printString += objectA
        printString += ' is better!<br/>Have a look at some reasons for this outcome:<br/><br/>'
        for i in range(0,5):
            if aSentences:
                printString += '<br/>'
                printString += aSentences[0]
                aSentences.pop(0)
            else:
                break
    elif bPoints > aPoints: #objectB is better.
        printString += objectB
        printString += ' is better!<br/>Have a look at some reasons for this outcome:<br/><br/>'
        for i in range(0,5):
            if bSentences:
                printString += '<br/>'
                printString += bSentences[0]
                bSentences.pop(0)
            else:
                break
    else: #both objects are equal.
        printString += objectA
        printString += ' and '
        printString += objectB
        printString += ' are both equal.<br/>Have a look at some reasons for this outcome:<br/><br/>'
        for i in range(0,2):
            if aSentences:
                printString += '<br/>'
                printString += aSentences[0]
                aSentences.pop(0)
            if bSentences:
                printString += '<br/>'
                printString += bSentences[0]
                bSentences.pop(0)
    return printString
    '''

if __name__ == "__main__":
    app.run()