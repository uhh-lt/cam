import requests

class Requester:
    #
    def __init__(self, A, B):
        self.objA = A
        self.objB = B

    def req(self):
        url = self.buildString()
        r = requests.get(url)
        print(r.text)

    def buildString(self):
        url = 'http://localhost:9222/commoncrawl2/_search?q=text:'
        url += self.objA
        url += '%20AND%20'
        url += self.objB
        url += '%20AND%20better'
        return url

r = Requester('Python', 'MATLAB')
r.req()