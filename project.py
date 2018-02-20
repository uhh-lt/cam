import requests
from requester import requester
from flask import Flask
app = Flask(__name__)

@app.route("/")
def com():
    r = requester('Python', 'MATLAB')
    printString = ''
    for i in range (0, len(r.req()) - 1):
        printString += r.req()[i]
        printString += '<br/>'
    return(printString)

@app.route("/test")
def test():
    return('test')

if __name__ == "__main__":
    app.run()