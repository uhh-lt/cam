
negRemovers = ['didn\'t', 'couldn\'t', 'wasn\'t', 'haven\'t', 'wouldn\'t', 'did not', 'could not', 'was not', 'have not', 'would not'
'didnt', 'couldnt', 'wasnt', 'havent', 'wouldnt']

def clearSentences(sentences):
    for s in sentences:
        if '?' in s:
            sentences.remove(s)
        else:
            for neg in negRemovers:
                if neg in s:
                    sentences.remove(s)
    return sentences