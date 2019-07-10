from utils.regex_service import find_pos_in_sentence


def has_marker(sentence, pos_first, pos_second, markers):
    '''
    checks if any one of a given list of markers exists in the given sentence between pos_first 
    and pos_second. Delegates work to get_marker_pos and qualifies result to boolean.

    sentence:   String
                the sentence to search for markers in.
    pos_first:  number
    pos_second: number
                positions between which the marker must be found.
    markers:    list
                list of the markers of which any one must be found.
    '''
    return get_marker_pos(sentence, pos_first, pos_second, markers) != -1


def get_marker_pos(sentence, pos_first, pos_second, markers):
    '''
    checks if any one of a given list of markers exists in the given sentence between pos_first 
    and pos_second, otherwise returns -1

    sentence:   String
                the sentence to search for markers in.
    pos_first:  number
    pos_second: number
                Positions between which the marker must be found.
    markers:    list
                list of the markers of which any one must be found.
    '''
    for m in markers:
        pos_marker = marker_pos(sentence, pos_first, pos_second, m)
        if pos_marker != -1:
            return pos_marker
    return -1


def get_marker_count(sentence, pos_first, pos_second, markers):
    '''
    Count the occurence of markers in a sentence between two positions: pos_first and pos_second

    sentence:   String
                the sentence to search for markers in.
    pos_first:  number
    pos_second: number
                Positions between which the marker must be found.
    markers:    list
                list of the markers of which any one must be found.
    '''
    cnt = 0
    for m in markers:
        if(marker_pos(sentence, pos_first, pos_second, m) != -1):
            cnt += 1
    return cnt

def marker_pos(sentence, pos_first, pos_second, marker):
    '''
    Checks if the given marker is contained in the sentence and between the given positions,
    if yes the position is returned, else -1 is returned
    '''
    pos_marker = find_pos_in_sentence(marker, sentence)
    if pos_marker != -1 and pos_first < pos_marker < pos_second:
        return pos_marker  # found a marker between the objects
    return -1

