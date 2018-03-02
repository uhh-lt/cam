import re


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
