import re
from utils.regex_service import find_last_pos_in_sentence, find_pos_in_sentence


permissible_pattern = ['a_c_b', 'b_c_a']

def negation_dissolve_heuristic(object_a, object_b, aspect):
    print(object_a.name, object_b.name, aspect)

    tag_sentences_a = tag_sentences(
        object_a.sentences, object_a.name, object_b.name, aspect)
    tag_sentences_b = tag_sentences(
        object_b.sentences, object_a.name, object_b.name, aspect)

    if len(tag_sentences_a) == 0 or len(tag_sentences_b) == 0:
        return
    a_max_tag = max(tag_sentences_a.items(), key=lambda elem: len(elem[1]))[0]
    b_max_tag = max(tag_sentences_b.items(), key=lambda elem: len(elem[1]))[0]
    print(len(tag_sentences_a[a_max_tag]), len(tag_sentences_b[b_max_tag]))

    if a_max_tag in permissible_pattern or b_max_tag in permissible_pattern:
        if len(tag_sentences_a[a_max_tag]) > len(tag_sentences_b[b_max_tag]):
            print('A:', a_max_tag)
            move_assignment(a_max_tag, tag_sentences_b,
                            object_b, object_a, aspect)
        else:
            print('B:', b_max_tag)
            move_assignment(b_max_tag, tag_sentences_a,
                            object_a, object_b, aspect)


def move_assignment(from_max_tag, to_tag_sentences, from_object, to_object, aspect):
    turned_tag = turn_tag(from_max_tag)
    if turned_tag in to_tag_sentences:
        sentences_to_move = to_tag_sentences[turned_tag]
        points_to_move = 0
        print('For', '\'' + aspect + '\'', 'there were moved', len(sentences_to_move),
              'sentences from', from_object.name, 'to', to_object.name, '.')
        print('----')
        for sentence in sentences_to_move:
            print('-' + re.sub(' +', ' ',
                               re.sub('[^a-zA-Z0-9 ]', ' ', sentence[1])))
            points_to_move = points_to_move + sentence[0]
        print('----')
        from_object.sentences = [
            sentence for sentence in from_object.sentences if sentence not in sentences_to_move]
        from_object.points[aspect] = from_object.points[aspect] - \
            points_to_move
        from_object.totalPoints = from_object.totalPoints - points_to_move

        to_object.sentences.extend(sentences_to_move)
        to_object.points[aspect] = to_object.points[aspect] + points_to_move
        to_object.totalPoints = to_object.totalPoints + points_to_move

        print((points_to_move / (to_object.totalPoints +
                                 from_object.totalPoints)) * 100, '% moved (total)')
        print((points_to_move / (to_object.points[aspect] +
                                 from_object.points[aspect])) * 100, '% moved for', aspect)
    else:
        print('No sentences were moved.')


def tag_sentences(sentences, a_name, b_name, aspect):
    tag_sentences = {}
    for sentence in sentences:
        tag = get_tag(sentence[1], a_name, b_name, aspect)
        if tag == 'none':
            continue
        if tag in tag_sentences:
            tag_sentences[tag].append(sentence)
        else:
            tag_sentences[tag] = [sentence]
    return tag_sentences


def turn_tag(tag):
    return tag[-1:] + tag[1:-1] + tag[:1]

def get_tag(sentence, object_a, object_b, aspect):

    pos_a = find_pos_in_sentence(object_a, sentence)
    pos_b = find_pos_in_sentence(object_b, sentence)
    pos_c = find_pos_in_sentence(aspect, sentence)
    if pos_a != -1 and pos_b != -1 and pos_c != -1:
        if pos_a > pos_b:
            pos_a = find_last_pos_in_sentence(object_a, sentence)
        else:
            pos_b = find_last_pos_in_sentence(object_b, sentence)

        indices = [['a', pos_a], ['b', pos_b], ['c', pos_c]]
        indices.sort(key=lambda elem: elem[1])

        return '_'.join([x[0] for x in indices])
    return 'none'