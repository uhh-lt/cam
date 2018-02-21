import requests
import json
import requester
import sentenceAnalyzer
import sentenceClearer
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
    return ('Test')

if __name__ == "__main__":
    app.run()