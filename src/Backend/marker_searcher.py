import re


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
    if get_marker_pos(sentence, pos_first, pos_second, markers) != -1:
        return True
    else:
        return False


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
    pos_marker = -1
    for m in markers:
        wordlist = re.compile('[A-Za-z]+').findall(sentence)
        if m in wordlist:
            pos_marker = wordlist.index(m)
            if pos_first < pos_marker < pos_second:
                break  # found a marker between the objects
            else:
                pos_marker = -1
    return pos_marker


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
    pos_marker = -1
    cnt = 0
    for m in markers:
        wordlist = re.compile('[A-Za-z]+').findall(sentence)
        if m in wordlist:
            pos_marker = wordlist.index(m)
            if pos_first < pos_marker < pos_second:
                cnt += 1
    return cnt
