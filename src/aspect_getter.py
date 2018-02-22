import re
import constants


def extract_main_aspects(stringlist, objA, objB):
    '''
    Extracts the most common words from a list of strings.

    stringlist: List
                list of strings
    '''
    worddict = {}
    for s in stringlist:
        wordlist = re.compile('[A-Za-z]+').findall(s)
        for w in wordlist:
            if w not in constants.STOPWORDS and w not in constants.MARKERS and w != objA and w != objB and w not in constants.NON_ASPECTS and w not in constants.NUMBER_STRINGS:
                if w in worddict:
                    worddict[w] += 1
                else:
                    worddict[w] = 1
    result = {}
    for _i in range(0, 10):
        k = max(worddict, key=worddict.get)
        result[k] = worddict[k]
        worddict.pop(k)
    return result
