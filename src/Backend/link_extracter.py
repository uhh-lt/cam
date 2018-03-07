import constants
import re
import nltk
from nltk import word_tokenize


def extract_main_links(sentencesA, sentencesB, objA, objB):
    '''
    Extracts the most common nouns for two lists of strings.

    sentencesA: List
                list of strings containing the sentences for object A

    sentencesB: List
                list of strings containing the sentences for object B

    objA:       Argument
                the first object to be compared

    objB:       Argument
                the second object to be compared
    '''
    # stores all words for object A as keys and the number of times they've been found as values
    worddictA = {}
    # stores all words for object B as keys and the number of times they've been found as values
    worddictB = {}
    for s in sentencesA:
        taglist = tag_sentence(s)
        for tag in taglist:
            if tag[1].startswith('NN'):  # is the word a noun?
                w = tag[0].lower()
                # check if w is "useful" as a linked word
                if w not in constants.STOPWORDS and w not in constants.POSITIVE_MARKERS and w not in \
                        constants.NEGATIVE_MARKERS and w != objA and w != objB and w not in \
                        constants.NON_LINKS and w not in constants.NUMBER_STRINGS:
                    if w in worddictA:
                        worddictA[w] += 1
                    else:
                        worddictA[w] = 1
    for s in sentencesB:
        taglist = tag_sentence(s)
        for tag in taglist:
            if tag[1].startswith('NN'):  # is the word a noun?
                w = tag[0].lower()
                # check if w is "useful" as a linked word
                if w not in constants.STOPWORDS and w not in constants.POSITIVE_MARKERS and w not in \
                        constants.NEGATIVE_MARKERS and w != objA and w != objB and w not in \
                        constants.NON_LINKS and w not in constants.NUMBER_STRINGS:
                    if w in worddictB:
                        worddictB[w] += 1
                    else:
                        worddictB[w] = 1
    result = {}
    resultA = []
    resultB = []
    # add ratios (frequency of the word in sentences of A divided by frequency in B)
    for word in worddictA:
        if word in worddictB:
            worddictA[word] = worddictA[word] / worddictB[word]
            worddictB[word] = worddictB[word] / worddictA[word]
    # return the top 10 links for A and B
    while (len(resultA) < 10 and len(resultB) < 10 and (worddictA or worddictB)):
        if worddictA:
            maxA = max(worddictA, key=worddictA.get)
            resultA.append(maxA)
            worddictA.pop(maxA)
        if worddictB:
            maxB = max(worddictB, key=worddictB.get)
            resultB.append(maxB)
            worddictB.pop(maxB)
    result['A'] = resultA
    result['B'] = resultB
    return result


def tag_sentence(sentence):
    # remove special characters
    s_rem = re.sub('[^a-zA-Z0-9 ]', ' ', sentence)
    # find all words in the sentence
    wordlist = word_tokenize(s_rem)
    taglist = nltk.pos_tag(wordlist)
    return taglist
