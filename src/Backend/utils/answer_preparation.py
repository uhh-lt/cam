from pandas import DataFrame
from utils.link_extracter import extract_main_links

def build_final_dict(obj_a, obj_b):
    '''
    Builds the final dictionary containing all necessary information regarding the comparison to 
    be returned to the frontend.

    obj_a:  Argument
            the first object of the comparison

    obj_b:  Argument
            the second object of the comparison
    '''
    final_dict = {}  # the dictionary to be returned

    if obj_a.totalPoints > obj_b.totalPoints:
        final_dict['winner'] = obj_a.name
    elif obj_b.totalPoints > obj_a.totalPoints:
        final_dict['winner'] = obj_b.name
    else:
        final_dict['winner'] = 'No winner found'
    linked_words = extract_main_links(
        obj_a.sentences, obj_b.sentences, obj_a, obj_b)
    final_dict['object1'] = obj_a.name
    final_dict['object2'] = obj_b.name
    final_dict['totalScoreObject1'] = obj_a.totalPoints
    final_dict['totalScoreObject2'] = obj_b.totalPoints
    final_dict['scoreObject1'] = obj_a.points
    final_dict['scoreObject2'] = obj_b.points
    final_dict['extractedAspectsObject1'] = linked_words['A']
    final_dict['extractedAspectsObject2'] = linked_words['B']
    final_dict['sentencesObject1'] = obj_a.sentences
    final_dict['sentencesObject2'] = obj_b.sentences
    final_dict['sentenceCount'] = len(obj_a.sentences) + len(obj_b.sentences)

    return final_dict

def add_points(contained_aspects, winner, score, sentence, max_score, classification_score, score_function):
    '''
    Adds the points of the won sentence to the points of the winner.

    contained_aspects:  List
                        The aspects the user entered that are 
                        contained in the sentence

    winner:             Argument
                        The winner of the given sentence

    score:              Integer
                        The score of the given sentence

    sentence:           String
                        The given sentence to add

    max_score:          Integer
                        Max score over all sentences

    marker_count:       Integer
                        How many markers are countained in the 
                        Sentence
    '''

    points = 0
    if contained_aspects:
        if len(contained_aspects) == 1:
            aspect = contained_aspects[0]
            points = score_function(score, max_score, aspect.weight, classification_score)
            winner.add_points(aspect.name, points)
            winner.add_sentence([points, sentence])
        else:
            for aspect in contained_aspects:
                points = points + score_function(score, max_score, aspect.weight, classification_score)
            winner.add_points('multiple', points)
            winner.add_sentence([points, sentence])
    else:
        # multiple markers, multiple points
        points = score_function(score, max_score, 0, classification_score)
        winner.add_points('none', points)
        winner.add_sentence([points, sentence])


def prepare_sentence_list(sentences_with_score):
    sentences_with_score.sort(key=lambda elem: elem[0], reverse = True)
    return list(DataFrame(sentences_with_score, columns=['points', 'sentence'])['sentence'])