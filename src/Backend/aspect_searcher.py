from regex_service import find_pos_in_sentence


def find_aspects(sentence, aspects):
    '''
    Searches for the aspects the user entered within a given sentence.

    sentence:   String
                the sentence which shall be scanned for aspects

    aspects:    List
                list of Aspect objects
    '''
    ret_aspects = []
    for aspect in aspects:
        if find_pos_in_sentence(aspect.name, sentence) != -1:
            ret_aspects.append(aspect)
    return ret_aspects
