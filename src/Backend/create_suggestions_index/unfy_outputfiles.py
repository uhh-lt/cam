import json
from elasticsearch import Elasticsearch

ES_HOST = {"host" : "localhost", "port" : 9200}
INDEX_NAME = "suggestions-index"
TYPE_NAME = "suggestions"
ID_FIELD = "suggestionsid"


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



#data = []
counter = 0

for i in range(0,741,1):
    document_name = 'outfile-{}.json'.format(str('%05d' % i))
    print(document_name)

    with open(document_name) as json_file:
        data = json.load(json_file)
        for obj in data:
            print(obj)
            es.index(index = INDEX_NAME, doc_type = TYPE_NAME, id = counter, body = obj)
            counter += 1


