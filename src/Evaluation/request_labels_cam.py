import requests
import csv
import operator
import time
import threading


class myThread (threading.Thread):
    def __init__(self, threadID, name, comparations):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.comparations = comparations
        self.resultList = []

    def run(self):
        print("Starting " + self.name)
        self.resultList = self.executeComparision(self.comparations, self.name)
        print("Finished " + self.name)

    def requestLabels(self, url, id):
        try:
            jsonResult = requests.get(url).json()
            scoreA = jsonResult['score object 1']
            scoreB = jsonResult['score object 2']

            return [scoreA, scoreB]
        except requests.exceptions.RequestException:
            print('Pair with id {}, raised an exception'.format(id))
            return self.requestLabels(url, id)

    def executeComparision(self, comparations, threadName):
        urls = generateURLS(comparations)
        resultList = []
        for i in range(0, len(urls), 1):
            id = comparations[i][0]
            result = comparations[i][:4]
            result.extend(self.requestLabels(urls[i], id))
            resultList.append(result)
            print(result[0] + ' ' + result[1] + ' ' + result[2] + ' ' +
                  result[3] + ' ' + str(result[4]) + ' ' + str(result[5]))
            # print(url)

        return resultList


def buildURL(objA, objB, aspectMap, model, fastSearch):
    hostname = ''
    if model == 'default':
        hostname = 'http://ltdemos.informatik.uni-hamburg.de/cam-api'
    elif model == 'machine_learning':
        hostname = 'http://ltdemos.informatik.uni-hamburg.de/cam-api'
    URL = hostname + '?fs=' + fastSearch + '&objectA=' + objA + '&objectB=' + objB
    URL += addAspectURL(aspectMap)
    return URL


def addAspectURL(aspectMap):
    url_part = ''
    i = 1
    for k, v in aspectMap.items():
        url_part += '&aspect' + str(i) + '=' + k + \
            '&weight' + str(i) + '=' + str(v)
        i += 1
    return url_part


def generateURLS(comparations):
    urls = []
    for objects in comparations:
        aspects = [x for x in objects[5].split(', ')]
        aspectDict = {}
        for aspect in aspects:
            aspectDict[aspect] = 5
        urls.append(buildURL(objects[1], objects[2],
                             aspectDict, 'default', 'false'))
    return urls


def main():
    comparations = []
    urlParam = 'NN+JJ'
    with open('./csv/({})_preprocessed_dataset.csv'.format(urlParam), newline='', encoding='utf-8') as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvReader:
            comparations.append(row)
    comparations.pop(0)

    requested = [['id', 'object_a', 'object_b',
                  'gold_label', 'score_a', 'score_b']]

    # *****Threads here*****
    # Create new threads
    threads = []

    i = 10
    thread1 = myThread(1, "Thread-1", comparations[0:i])
    thread2 = myThread(2, "Thread-2", comparations[i:2*i])
    thread3 = myThread(3, "Thread-3", comparations[2*i:3*i])
    thread4 = myThread(4, "Thread-4", comparations[3*i:4*i])
    thread5 = myThread(5, "Thread-5", comparations[4*i:5*i])
    thread6 = myThread(6, "Thread-6", comparations[5*i:6*i])
    thread7 = myThread(7, "Thread-7", comparations[6*i:7*i])
    thread8 = myThread(8, "Thread-8", comparations[7*i:8*i])
    thread9 = myThread(9, "Thread-9", comparations[8*i:9*i])
    thread10 = myThread(10, "Thread-10", comparations[9*i:10*i])
    thread11 = myThread(11, "Thread-11", comparations[10*i:11*i])
    thread12 = myThread(12, "Thread-12", comparations[11*i:12*i])
    thread13 = myThread(13, "Thread-13", comparations[12*i:13*i])
    thread14 = myThread(14, "Thread-14", comparations[13*i:14*i])
    thread15 = myThread(15, "Thread-15", comparations[14*i:15*i])
    thread16 = myThread(16, "Thread-16", comparations[15*i:16*i])
    thread17 = myThread(17, "Thread-17", comparations[16*i:17*i])
    thread18 = myThread(18, "Thread-18", comparations[17*i:18*i])
    thread19 = myThread(19, "Thread-19", comparations[18*i:19*i])
    thread20 = myThread(20, "Thread-20", comparations[19*i:20*i])

    # Start new Threads
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()
    thread6.start()
    thread7.start()
    thread8.start()
    thread9.start()
    thread10.start()
    thread11.start()
    thread12.start()
    thread13.start()
    thread14.start()
    thread15.start()
    thread16.start()
    thread17.start()
    thread18.start()
    thread19.start()
    thread20.start()

    # Add threads to thread list
    threads.append(thread1)
    threads.append(thread2)
    threads.append(thread3)
    threads.append(thread4)
    threads.append(thread5)
    threads.append(thread6)
    threads.append(thread7)
    threads.append(thread8)
    threads.append(thread9)
    threads.append(thread10)
    threads.append(thread11)
    threads.append(thread12)
    threads.append(thread13)
    threads.append(thread14)
    threads.append(thread15)
    threads.append(thread16)
    threads.append(thread17)
    threads.append(thread18)
    threads.append(thread19)
    threads.append(thread20)

    print('Processing...')
    # Wait for all threads to complete
    while(thread1.isAlive() or thread2.isAlive() or thread3.isAlive() or thread4.isAlive()
          or thread5.isAlive() or thread6.isAlive() or thread7.isAlive() or thread8.isAlive()
          or thread9.isAlive() or thread10.isAlive() or thread11.isAlive() or thread12.isAlive()
          or thread13.isAlive() or thread14.isAlive() or thread15.isAlive() or thread16.isAlive()
          or thread17.isAlive() or thread18.isAlive() or thread19.isAlive() or thread20.isAlive()):
        pass

    for t in threads:
        print('Wait')
        t.join()
        requested.extend(t.resultList)

    print("Exiting Main Thread")
    print(str(len(requested)) + ' results.')
    # **********************

    with open('./csv/({})_requested_labels.csv'.format(urlParam), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(requested)


start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))
