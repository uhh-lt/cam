import pandas
from elasticsearch import Elasticsearch
import time
from sample_wordlist import comparison_objects
from sample_wordlist import comparison_objects_small
import requests
import json
from multiprocessing import Pool

ES_HOST = {"host" : "localhost", "port" : 9200}
INDEX_NAME = "suggestions-index"
TYPE_NAME = "suggestions"
ID_FIELD = "suggestionsid"
CCR_BASE_URL = "http://127.0.0.1:5000/ccr/"


# Create ES client, create index.
es = Elasticsearch(hosts = [ES_HOST], timeout=300)
if es.indices.exists(INDEX_NAME):
    print("deleting '%s' index..." % (INDEX_NAME))
    res = es.indices.delete(index = INDEX_NAME)
    print(" response: '%s'" % (res))
# Since we are running locally, use one shard and no replicas.
request_body = {
    "settings" : {
        "number_of_shards": 1,
        "number_of_replicas": 0
    }
}
print("creating '%s' index..." % (INDEX_NAME))
res = es.indices.create(index = INDEX_NAME, body = request_body)
print(" response: '%s'" % (res))


# New version, parallel on server:




# Old version, one by one, locally:
#total_time_start = time.time()

#index = 0
#start = time.time()
# do something with each word in the sample_wordlist
#for comparison_object in comparison_objects:
#    index += 1
#    ccr_suggestions = requests.get(CCR_BASE_URL + '{}'.format(comparison_object)).json()
#
#    data = {}
#    data = {
#        "comparison_object": comparison_object,
#        "suggestions": ccr_suggestions
#        }
#
#
#    es.index(index = INDEX_NAME, doc_type = TYPE_NAME, id = index, body = data)


res1 = es.get(index = INDEX_NAME, doc_type = TYPE_NAME, id = 1)
res2 = es.get(index = INDEX_NAME, doc_type = TYPE_NAME, id = 2)
res3 = es.get(index = INDEX_NAME, doc_type = TYPE_NAME, id = 3)

print(res1)
print(res2)
print(res3)

print("hallo welt!")



res = es.search(index=INDEX_NAME, body={"query": {"match": {"comparison_object": "c"}}})
print(res)

res = es.search(index=INDEX_NAME, body={"query": {"match": {"comparison_object": "petrol"}}})
print(res)

res = es.search(index=INDEX_NAME, body={"query": {"match": {"suggestions": "gold"}}})
print(res)

if res["hits"]["total"] > 0:
    print(res["hits"]["hits"][0]["_source"]["suggestions"])
else:
    print("no suggestions")
