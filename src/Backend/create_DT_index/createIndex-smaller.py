import pandas
from elasticsearch import Elasticsearch
import time
import csv
from evaluation_triples import triples





FILE_PATH = "../data/"
ES_HOST = {"host" : "localhost", "port" : 9200}
INDEX_NAME = 'dt-index'
TYPE_NAME = 'triple'
ID_FIELD = 'tripleid'

first_triples = [triple[1] for triple in triples]
print(first_triples)
first_triples_regex = '|'.join(first_triples)
print(first_triples_regex)

header = ['first', 'second', 'similarity']

# create ES client, create index
es = Elasticsearch(hosts = [ES_HOST], timeout=300)
if es.indices.exists(INDEX_NAME):
    print("deleting '%s' index..." % (INDEX_NAME))
    res = es.indices.delete(index = INDEX_NAME)
    print(" response: '%s'" % (res))
# since we are running locally, use one shard and no replicas
request_body = {
    "settings" : {
        "number_of_shards": 1,
        "number_of_replicas": 0
    }
}
print("creating '%s' index..." % (INDEX_NAME))
res = es.indices.create(index = INDEX_NAME, body = request_body)
print(" response: '%s'" % (res))

total_time_start = time.time()

# Go through the 1000 documents

for k in range(0,1,1):
    index = 0
    # build document index part (x)
    document_name = 'part-{}.txt'.format(str('%05d' % k))
    print('Indexing file', document_name, '.......')

    # load file
    triple_df = pandas.read_csv(FILE_PATH + document_name, sep='\t', header=None, names=header, dtype={'first': str, 'second': str}, encoding='utf-8', quoting=csv.QUOTE_NONE)
    triple_df = triple_df.dropna()
    triple_df = triple_df[triple_df['first'].str.contains(first_triples_regex)]
    
    document_length = len(triple_df.index)
    print('File loaded....(', document_length, ')')

    bulk_data = []
    bulk_counter = 0
    # formate data to bulk load into elasticsearch
    start = time.time()
    for row_index, row in triple_df.iterrows():
        data_dict = {}
        # data_dict[ID_FIELD] = index
        index += 1
        for i in range(len(row)):
            data_dict[header[i]] = row[i]
        op_dict = {
            "index": {
                "_index": INDEX_NAME, 
                "_type": TYPE_NAME, 
                # "_id": data_dict[ID_FIELD]
            }
        }
        bulk_data.append(op_dict)
        bulk_data.append(data_dict)
        bulk_counter += 1

        # bulk load into elasticsearch after every 5000 lines
        if bulk_counter > 1000:
            end = time.time()
            print('Data preparation process took:', end - start, 's')
            print("Bulk data prepared, bulk indexing ({})...".format(index/document_length))
            res = es.bulk(index = INDEX_NAME, body = bulk_data, refresh = True)
            start = time.time()
            print('Bulking took:', start - end, 's', 'Actual total time used:', time.time() - total_time_start, 's')
            bulk_counter = 0
            bulk_data = []
    end = time.time()
    print('Data preparation process took:', end - start, 's')
    print("Bulk data prepared, bulk indexing ({})...".format(index/document_length))
    res = es.bulk(index = INDEX_NAME, body = bulk_data, refresh = True)
    start = time.time()
    print('Bulking took:', start - end, 's', 'Actual total time used:', time.time() - total_time_start, 's')
    bulk_counter = 0
    bulk_data = []




# sanity check
res = es.search(index = INDEX_NAME, size=10000, body={"query": {"match": {"first": "python"}}})
print(" response: '%s'" % (len(res)))

for hit in res['hits']['hits']:
    print(hit["_source"])