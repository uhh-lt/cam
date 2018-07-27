import pandas as pd
from utils.regex_service import find_pos_in_sentence


def prepare_sentence_DF(sentences, obj_a, obj_b):
    index = 0
    temp_list = []
    for sentence in sentences:
        pos_a = find_pos_in_sentence(obj_a.name, sentence)
        pos_b = find_pos_in_sentence(obj_b.name, sentence)
        if pos_a < pos_b:
            temp_list.append([obj_a.name, obj_b.name, sentence])
        else:
            temp_list.append([obj_b.name, obj_a.name, sentence])
        index += 1
    sentence_df = pd.DataFrame.from_records(temp_list, columns=['object_a', 'object_b', 'sentence'])

    return sentence_df