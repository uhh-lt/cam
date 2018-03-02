import constants
import marker_searcher


def clear_sentences(sentences, objA, objB):
    '''
    Removes sentences which (currently) cannot be properly analyzed from a list of sentences.

    sentences:  list
                a list of sentences
    '''
    sentences = remove_questions(sentences)
    sentences = remove_wrong_structures(sentences, objA, objB)
    return sentences


def remove_questions(sentences):
    '''
    Removes questions from a list of sentences.

    sentences:  list
                a list of sentences
    '''
    sentences_to_delete = []
    for s in sentences:
        if '?' in s:
            sentences_to_delete.append(s)
    for s in sentences_to_delete:
        sentences.pop(s)
    return sentences


def remove_wrong_structures(sentences, objA, objB):
    '''
    Removes sentences 1: in which no marker is between the objects from a list of sentences;
                      2: in which the marker is not between the objects.

    sentences:  list
                a list of sentences
    '''
    sentences_to_delete = []
    for s in sentences:
        aPos = s.find(objA.name)
        bPos = s.find(objB.name)
        if aPos == -1 and bPos == -1:
            sentences_to_delete.append(s)
            continue
        pos_first = min(aPos, bPos)
        pos_second = max(aPos, bPos)
        has_pos_marker = marker_searcher.has_marker(
            s, pos_first, pos_second, constants.POSITIVE_MARKERS)
        has_neg_marker = marker_searcher.has_marker(
            s, pos_first, pos_second, constants.NEGATIVE_MARKERS)
        if (has_pos_marker and has_neg_marker) or (not has_pos_marker and not has_neg_marker):
            sentences_to_delete.append(s)
    for s in sentences_to_delete:
        sentences.pop(s)
    return sentences
