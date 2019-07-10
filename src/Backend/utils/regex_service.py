import re



def get_regEx(sequence):
    return re.compile('\\b{}\\b|\\b{}\\b'.format(re.escape(sequence), re.sub('[^a-zA-Z0-9 ]', ' ', sequence)), re.IGNORECASE)

def find_pos_in_sentence(sequence, sentence):
    '''
    Searches the given sequence in the given sentence. If it is found (via regex) the start is returned,
    if not -1 is returned.

    sequence: the word sequence to search (can also be only one word)
    sentence: the sentence to search the sequence in
    '''
    regEx = get_regEx(sequence)
    match = regEx.search(sentence)    
    if match == None:
        match = regEx.search(re.sub(' +',' ', re.sub('[^a-zA-Z0-9 ]', ' ', sentence)))
        return match.start() if match != None else -1
    else:
        return match.start()

def find_last_pos_in_sentence(sequence, sentence):
    regEx = get_regEx(sequence)
    last_pos = -1
    for match in regEx.finditer(sentence):    
        last_pos = match.start()
    if last_pos == -1:
        for match in regEx.finditer(re.sub(' +',' ', re.sub('[^a-zA-Z0-9 ]', ' ', sentence))):
            last_pos = match.start()
    return last_pos


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