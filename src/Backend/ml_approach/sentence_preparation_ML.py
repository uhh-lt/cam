import pandas as pd
from utils.regex_service import find_pos_in_sentence
import re


def prepare_sentence_DF(sentences, obj_a, obj_b, aspects):
    temp_list = []
    for sentence in sentences:
        best_match = find_best_match(sentence, obj_a, obj_b, aspects)
        if not best_match:
            best_match = find_best_match(sentence, obj_b, obj_a, aspects)
            if not best_match:
                pos_a = find_pos_in_sentence(obj_a.name, sentence)
                pos_b = find_pos_in_sentence(obj_b.name, sentence)
                if pos_a < pos_b:
                    temp_list.append([obj_a.name, obj_b.name, sentence, pos_a, pos_b])
                else:
                    temp_list.append([obj_b.name, obj_a.name, sentence, pos_b, pos_a])
            else:
                temp_list.append([obj_b.name, obj_a.name, sentence, best_match[0], best_match[1]])
        else:
            temp_list.append([obj_a.name, obj_b.name, sentence, best_match[0], best_match[1]])

    sentence_df = pd.DataFrame.from_records(temp_list, columns=['object_a', 'object_b', 'sentence', 'pos_a', 'pos_b'])

    return sentence_df


def find_best_match(sentence, obj_a, obj_b, aspects):

    regex = re.compile(r'(' + obj_a.name + r').*?(' + '|'.join([aspect.name for aspect in aspects]) + r').*?(' + obj_b.name + r')')

    matches = re.finditer(regex, sentence)
    results = [match for match in matches]
    if len(results) == 0:
        return False
    lengthes = [match.span()[1]-match.span()[0] for match in results]
    min_index = lengthes.index(min(lengthes))

    return (results[min_index].span(1)[0], results[min_index].span(3)[0])