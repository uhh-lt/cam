class Sentence:
    '''
    Sentence class to hold sentence related values
    '''

    def __init__(self, text, score, document_id, sentence_id):
        self.text = text
        self.score = score
        self.document_id = document_id
        self.sentence_id = sentence_id


class Argument:
    '''
    Argument Class for the objects to be compared
    '''

    def __init__(self, name):
        self.name = name.lower()
        self.points = {}
        self.totalPoints = 0
        self.sentences = []

    def add_points(self, aspect, points):
        self.totalPoints = self.totalPoints + points
        if aspect in self.points:
            self.points[aspect] = self.points[aspect] + points
        else:
            self.points[aspect] = points

    def add_sentence(self, sentence):
        self.sentences.append(sentence)


class Aspect:
    '''
    Aspect Class for the user entered aspects
    '''

    def __init__(self, name, weight):
        self.name = name.lower()
        self.weight = weight