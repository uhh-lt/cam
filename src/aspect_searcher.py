import re
import constants


def extract_main_aspects(sentences, objA, objB):
    '''
    Extracts the most common words from a list of strings.

    sentences:  List
                list of strings
    '''
    worddict = {}  # stores all words as keys and the number of times they've been found as values
    for s in sentences:
        # find all words in the sentence
        wordlist = re.compile('[A-Za-z]+').findall(s)
        for w in wordlist:
            # check if w is "useful" as an aspect
            if w not in constants.STOPWORDS and w not in constants.MARKERS and w != objA and \
                    w != objB and w not in constants.NON_ASPECTS and w not in constants.NUMBER_STRINGS:
                if w in worddict:
                    worddict[w] += 1
                else:
                    worddict[w] = 1
    result = {}
    for _i in range(0, 10):  # return the top 10 aspects
        k = max(worddict, key=worddict.get)
        result[k] = worddict[k]
        worddict.pop(k)
    return result


def find_aspects(sentence, aspects):
    '''
    Searches for one of the aspects the user entered within a given sentence.

    sentence:   String
                the sentence which shall be scanned for aspects

    aspects:    List
                list of Aspect objects
    '''
    wordlist = re.compile(
        '[A-Za-z]+').findall(sentence)  # find all words in the sentence
    ret_aspects = []
    for aspect in aspects:
        if aspect.name in wordlist:
            ret_aspects.append(aspect)
    return ret_aspects
