import requests
import requester
import sentenceAnalyzer
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/")
def com():
    return ('hallo')

@app.route('/cam', methods=['GET'])
def cam():
    object1 = request.args.get('object1')
    object2 = request.args.get('object2')
    aspect = request.args.get('aspect')
<<<<<<< HEAD:project.py
    sentences = requester.req(object1, object2)
=======
    r = requester.req(object1, object2, aspect)
>>>>>>> 5e84ec004fec4c303c02d2f537fcc2b86a01a1b2:src/main.py
    printString = ''
    for i in range (0, len(sentences) - 1):
        printString += sentences[i]
        printString += '<br/>'
    return(printString)

if __name__ == "__main__":
    app.run()