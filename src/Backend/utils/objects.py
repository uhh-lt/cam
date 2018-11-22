class Sentence:
    '''
    Sentence class to hold sentence related values
    '''

    def __init__(self, text, ES_score, document_id, sentence_id):
        self.text = text
        self.ES_score = ES_score
        self.CAM_score = 0
        self.id_pair = {document_id: sentence_id}
        self.confidence = 0
        self.context_aspects = []

    def add_id_pair(self, document_id, sentence_id):
        self.id_pair[document_id] = sentence_id

    def set_confidence(self, confidence):
        self.confidence = confidence

    def add_context_aspects(self, context_aspects):
        self.context_aspects += context_aspects
    def set_CAM_score(self, CAM_score):
        self.CAM_score = CAM_score


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

    def add_sentence(self, sentence: Sentence):
        self.sentences.append(sentence)


class Aspect:
    '''
    Aspect Class for the user entered aspects
    '''

    def __init__(self, name, weight):
        self.name = name.lower()
        self.weight = weight