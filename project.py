import requests
from requester import requester
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
    r = requester(object1, object2)
    printString = ''
    for i in range (0, len(r.req()) - 1):
        printString += r.req()[i]
        printString += '<br/>'
    return(printString)

if __name__ == "__main__":
    app.run()