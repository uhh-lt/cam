import re
import nltk
from nltk import word_tokenize
from constants import STOPWORDS, POSITIVE_MARKERS, NEGATIVE_MARKERS, NON_LINKS, NUMBER_STRINGS


def extract_main_links(sentencesA, sentencesB, obj_a, obj_b):
    '''
    Extracts the most common nouns for two lists of strings.

    sentencesA: List
                list of strings containing the sentences for object A

    sentencesB: List
                list of strings containing the sentences for object B

    obj_a:       Argument
                the first object to be compared

    obj_b:       Argument
                the second object to be compared
    '''
    # stores all words for object A as keys and the number of times they've been found as values
    worddict_a = {}
    # stores all words for object B as keys and the number of times they've been found as values
    worddict_b = {}
    for s in sentencesA:
        taglist = tag_sentence(s)
        for tag in taglist:
            if tag[1].startswith('NN'):  # is the word a noun?
                w = tag[0].lower()
                if is_useful(w, obj_a, obj_b):
                    if w in worddict_a:
                        worddict_a[w] += 1
                    else:
                        worddict_a[w] = 1
    for s in sentencesB:
        taglist = tag_sentence(s)
        for tag in taglist:
            if tag[1].startswith('NN'):  # is the word a noun?
                w = tag[0].lower()
                if is_useful(w, obj_a, obj_b):
                    if w in worddict_b:
                        worddict_b[w] += 1
                    else:
                        worddict_b[w] = 1
    result = {}
    result_a = []
    result_b = []
    # add ratios (frequency of the word in sentences of A divided by frequency in B)
    for word in worddict_a:
        if word in worddict_b:
            worddict_a[word] = worddict_a[word] / worddict_b[word]
            worddict_b[word] = worddict_b[word] / worddict_a[word]
    # return the top 10 links for A and B
    while (len(result_a) < 10 and len(result_b) < 10 and (worddict_a or worddict_b)):
        if worddict_a:
            maxA = max(worddict_a, key=worddict_a.get)
            result_a.append(maxA)
            worddict_a.pop(maxA)
        if worddict_b:
            maxB = max(worddict_b, key=worddict_b.get)
            result_b.append(maxB)
            worddict_b.pop(maxB)
    result['A'] = result_a
    result['B'] = result_b
    return result


def is_useful(word, obj_a, obj_b):
    '''
    Checks if the word is useful; that is, it's not one of the stopwords, markers, number strings
    or non links or one of the objects.

    word:   String
            the word to check

    obj_a:  String
            one of the two objects

    obj_b:  String
            the second object
    '''
    return word not in STOPWORDS and word not in POSITIVE_MARKERS and word not in NEGATIVE_MARKERS \
        and word != obj_a and word != obj_b and word not in NON_LINKS and word not in NUMBER_STRINGS


def tag_sentence(sentence):
    '''
    Returns a list of tags for each word of the sentence. A tag is a combination of the word and
    its part of speech coded as an NLTK tag, for example ('apple', 'NN').
    '''
    # remove special characters
    s_rem = re.sub('[^a-zA-Z0-9 ]', ' ', sentence)
    # find all words in the sentence
    wordlist = word_tokenize(s_rem)
    taglist = nltk.pos_tag(wordlist)
    return taglist
