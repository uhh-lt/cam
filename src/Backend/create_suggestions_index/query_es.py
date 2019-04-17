import pandas
from elasticsearch import Elasticsearch
import time
from sample_wordlist import comparison_objects
from sample_wordlist import comparison_objects_small
import requests
import json


ES_HOST = {"host" : "localhost", "port" : 9200}
INDEX_NAME = "suggestions-index"
TYPE_NAME = "suggestions"


# Create ES client, create index.
es = Elasticsearch(hosts = [ES_HOST], timeout=300)


res1 = es.get(index = INDEX_NAME, doc_type = TYPE_NAME, id = 1)
res2 = es.get(index = INDEX_NAME, doc_type = TYPE_NAME, id = 2)
res3 = es.get(index = INDEX_NAME, doc_type = TYPE_NAME, id = 3)

print(res1)
print(res2)
print(res3)

print("hallo welt!")



res = es.search(index=INDEX_NAME, body={"query": {"match": {"comparison_object": "c"}}})
print(res)

res = es.search(index=INDEX_NAME, body={"query": {"match": {"comparison_object": "gold"}}})
print(res)

res = es.search(index=INDEX_NAME, body={"query": {"match": {"suggestions": "petrol"}}})
print(res)

res = es.search(index=INDEX_NAME, body={"query": {"match": {"suggestions": "petrol"}}})
print(res)

if res["hits"]["total"] > 0:
    print(res["hits"]["hits"][0]["_source"]["suggestions"])
else:
    print("no suggestions")
