import requests

class requester:
    #
    def __init__(self, A, B):
        self.objA = A
        self.objB = B
        self.markers = ['better', 'easier', 'faster', 'nicer', 'wiser', 'cooler', 'decent', 'safer', 'superior', 'solid', 'terrific', 'worse', 'harder', 'slower', 'poorly', 'uglier', 'poorer', 'lousy', 'nastier', 'inferior', 'mediocre']

    def req(self):
        url = self.buildString()
        r = requests.get(url)
        hits = r.json()['hits']['hits']
        sentences = []
        for i in range(0, len(hits) - 1):
            sentences.append(hits[i]['_source']['text'])
        return sentences

    def buildString(self):
        url = 'http://localhost:9222/commoncrawl2/_search?q=text:'
        url += self.objA
        url += '%20AND%20'
        url += self.objB
        url += '%20AND%20('
        for i in range(0, len(self.markers) - 2):
            url += self.markers[i]
            url += '%20OR%20'
        url += self.markers[len(self.markers) - 1]
        url += ')&from=0&size=10000'
        return url