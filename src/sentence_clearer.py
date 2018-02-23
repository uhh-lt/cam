import constants


def clear_sentences(sentences):
    '''
    Removes sentences which (currently) cannot be properly analyzed from a list of sentences.

    sentences:  list
                a list of sentences
    '''
    sentences = remove_questions(sentences)
    sentences = remove_negations(sentences)
    return sentences


def remove_questions(sentences):
    '''
    Removes questions from a list of sentences.

    sentences:  list
                a list of sentences
    '''
    for s in sentences:
        if '?' in s:
            sentences.remove(s)
    return sentences


def remove_negations(sentences):
    '''
    Removes negations from a list of sentences.

    sentences:  list
                a list of sentences
    '''
    for s in sentences:
        for neg in constants.NEGATIONS:
            if neg in s:
                sentences.remove(s)
                break
    return sentences
