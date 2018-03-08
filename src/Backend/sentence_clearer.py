from constants import POSITIVE_MARKERS, NEGATIVE_MARKERS
from marker_searcher import has_marker
import re


def clear_sentences(sentences, obj_a, obj_b):
    '''
    Removes sentences which (currently) cannot be properly analyzed from a dictionary of sentences.

    sentences:  dictionary
                a dictionary of sentences

    obj_a:      Argument
                the first object to be compared

    obj_b:      Argument
                the second object to be compared
    '''
    sentences = remove_questions(sentences)
    sentences = remove_wrong_structures(sentences, obj_a, obj_b)
    return sentences


def remove_questions(sentences):
    '''
    Removes questions from a dictionary of sentences.

    sentences:  dictionary
                a dictionary of sentences
    '''
    sentences_to_delete = []
    for s in sentences:
        if '?' in s:
            sentences_to_delete.append(s)
    for s in sentences_to_delete:
        sentences.pop(s)
    return sentences


def remove_wrong_structures(sentences, obj_a, obj_b):
    '''
    Removes sentences 1: in which no marker is between the objects
                      2: in which there are both positive and negative markers between the objects

    sentences:  dictionary
                a dictionary of sentences

    obj_a:      Argument
                the first object to be compared

    obj_b:      Argument
                the second object to be compared
    '''
    sentences_to_delete = []
    for s in sentences:
        wordlist = re.compile('[A-Za-z]+').findall(s)
        a_pos = -1
        if obj_a.name in wordlist:
            a_pos = wordlist.index(obj_a.name)
        b_pos = -1
        if obj_b.name in wordlist:
            b_pos = wordlist.index(obj_b.name)
        if a_pos == -1 and b_pos == -1:
            sentences_to_delete.append(s)
            continue
        pos_first = min(a_pos, b_pos)
        pos_second = max(a_pos, b_pos)
        has_pos_marker = has_marker(s, pos_first, pos_second, POSITIVE_MARKERS)
        has_neg_marker = has_marker(s, pos_first, pos_second, NEGATIVE_MARKERS)
        if (has_pos_marker and has_neg_marker) or (not has_pos_marker and not has_neg_marker):
            sentences_to_delete.append(s)
    for s in sentences_to_delete:
        sentences.pop(s)
    return sentences
