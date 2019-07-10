from elasticsearch import Elasticsearch
import re

ES_HOST = {"host" : "localhost", "port" : 9200}
INDEX_NAME = 'dt-index'

es = Elasticsearch(hosts = [ES_HOST], timeout=300)








def get_all_similarities(comparison_object):
    # print(comparison_object)
    res = es.search(index = INDEX_NAME, size=10000, body={"query": {"match": {"first": comparison_object}}})

    return list(set([hit['_source']['second'].lower() for hit in res['hits']['hits']]))