from pandas import DataFrame
import json
from utils.pos_link_extracter import extract_main_links


def build_final_dict(obj_a, obj_b, sentences):
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
    linked_words = extract_main_links(obj_a, obj_b)

    obj_a.sentences = sentences_to_JSON(obj_a.sentences)
    obj_b.sentences = sentences_to_JSON(obj_b.sentences)
    final_dict['object1'] = obj_a.__dict__
    final_dict['object2'] = obj_b.__dict__
    final_dict['extractedAspectsObject1'] = linked_words['A']
    final_dict['extractedAspectsObject2'] = linked_words['B']
    final_dict['sentenceCount'] = len(obj_a.sentences) + len(obj_b.sentences)
    return final_dict


def sentences_to_JSON(sentences):
    return [sentence.__dict__ for sentence in sentences]


def add_points(contained_aspects, winner, sentence, max_score, classification_score, score_function, threshold_sentences=0, threshold_score=0):
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
    document_occurences = len(sentence.id_pair)
    document_occurences = 1 if document_occurences == 0 else document_occurences
    if contained_aspects:
        if len(contained_aspects) == 1:
            aspect = contained_aspects[0]
            points = score_function(
                sentence.score, max_score, aspect.weight, classification_score, threshold_sentences)
            if classification_score < threshold_score:
                winner.add_points(aspect.name, (points/10) * document_occurences)
            else:
                winner.add_points(aspect.name, points * document_occurences)
            winner.add_sentence([points, sentence])
        else:
            for aspect in contained_aspects:
                points += score_function(sentence.score, max_score,
                                         aspect.weight, classification_score, threshold_sentences)
            winner.add_points('multiple', points * document_occurences)
            winner.add_sentence([points, sentence])
    else:
        # multiple markers, multiple points
        points = score_function(
            sentence.score, max_score, 0, classification_score, threshold_sentences)
        # if classification_score > threshold_score:
        winner.add_points('none', points * document_occurences)
        winner.add_sentence([points, sentence])


def prepare_sentence_list(sentences_with_score):
    sentences_with_score.sort(key=lambda elem: elem[0], reverse=True)
    return list(DataFrame(sentences_with_score, columns=['points', 'sentence'])['sentence'])
