import constants
import re


def extract_main_links(sentences, objA, objB):
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
            w = w.lower()
            # check if w is "useful" as a links
            if w not in constants.STOPWORDS and w not in constants.POSITIVE_MARKERS and w not in \
                    constants.NEGATIVE_MARKERS and w != objA and w != objB and w not in \
                    constants.NON_LINKS and w not in constants.NUMBER_STRINGS:
                if w in worddict:
                    worddict[w] += 1
                else:
                    worddict[w] = 1
    result = {}
    for _i in range(0, 10):  # return the top 10 links
        if worddict:
            k = max(worddict, key=worddict.get)
            result[k] = worddict[k]
            worddict.pop(k)
    return result
