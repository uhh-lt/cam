import requests
import requester
import sentenceAnalyzer
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/")
def com():
    return ('Until the UI is finished, try CAM by opening ../cam?objectA=OBJA&objectB=OBJB&aspect=ASP replacing OBJA, OBJB and ASP with your desired values.')

@app.route('/cam', methods=['GET'])
def cam():
    objectA = request.args.get('objectA')
    objectB = request.args.get('objectB')
    aspect = request.args.get('aspect')
    allSentences = requester.req(objectA, objectB, aspect) #list of all sentences containing objectA, objectB and a marker.
    aPoints = 0 #counts how many times objA won a sentence.
    bPoints = 0 #counts how many times objB won a sentence.
    aSentences = [] #collects all sentences objA has won.
    bSentences = [] #collects all sentences objB has won.
    for s in allSentences:
        result = sentenceAnalyzer.analyze(s, objectA, objectB)
        if result == objectA: #objectA won the sentence
            aPoints += 1
            aSentences.append(s)
        elif result == objectB: #objectB won the sentence
            bPoints += 1
            bSentences.append(s)
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

if __name__ == "__main__":
    app.run()