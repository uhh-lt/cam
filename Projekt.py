import requests
from flask import Flask
app = Flask(__name__)

@app.route("/")
def com():
    r = requests.get('http://localhost:9222/commoncrawl2/_search?q=text:matlab%20AND%20python%20AND%20better')
    print(r.text)
    print("\n")
    print("\n")
    print(r.json()['hits']['hits'][1]['_source']['text'])

if __name__ == "__main__":
    app.run()