import constants
import re


def extract_main_links(sentencesA, sentencesB, objA, objB):
    '''
    Extracts the most common words from a list of strings.

    sentences:  List
                list of strings
    '''
    # stores all words for object A as keys and the number of times they've been found as values
    worddictA = {}
    # stores all words for object B as keys and the number of times they've been found as values
    worddictB = {}
    for s in sentencesA:
        # find all words in the sentence
        wordlist = re.compile('[A-Za-z]+').findall(s)
        for w in wordlist:
            w = w.lower()
            # check if w is "useful" as a links
            if w not in constants.STOPWORDS and w not in constants.POSITIVE_MARKERS and w not in \
                    constants.NEGATIVE_MARKERS and w != objA and w != objB and w not in \
                    constants.NON_LINKS and w not in constants.NUMBER_STRINGS:
                if w in worddictA:
                    worddictA[w] += 1
                else:
                    worddictA[w] = 1
    result = {}
    resultA = {}
    resultB = {}
    resultBoth = {}
    resultBothTemp = {}
    # return the top 10 links for A, B and both
    while (len(resultA.keys()) < 10 and len(resultB.keys()) < 10):
        if worddictA:
            maxA = max(worddictA, key=worddictA.get)
            resultA[maxA] = worddictA[maxA]
            worddictA.pop(maxA)
        if worddictB:
            maxB = max(worddictB, key=worddictB.get)
            resultB[maxB] = worddictB[maxB]
            worddictB.pop(maxB)
        for key in worddictA:
            if key in worddictB.keys():
                resultBothTemp[key] = resultA[key] + resultB[key]
                resultA.pop(key)
                resultB.pop(key)
    result['A'] = resultA
    result['B'] = resultB
    for _i in range(0, 10):
        maxBoth = max(resultBothTemp, key=resultBothTemp.get)
        resultBoth[maxBoth] = resultBothTemp[maxBoth]
        resultBothTemp.pop(maxBoth)
    return result
