import re
from utils.regex_service import find_aspects

positive_contrary_comparatives = {
    'more': ['less', 'lower'],
    'higher': ['lower', 'smaller'],
    'bigger': ['smaller'],
    'faster': ['slower'],
    'quicker': ['slower'],
    'smarter': ['dumper'],
    'larger': ['smaller'],
    'harder': ['softer'],
    'better': ['worse'],
    'easier': ['more difficult'],
    'safer': ['more dangerous'],
    'superior': ['inferior'],
    'greater': ['smaller'],
    'lighter': ['heavier'],
    'taller': ['shorter'],
    'fatter': ['thinner'],
    'more beautiful': ['uglier'],
    'wetter': ['drier'],
    'more open': ['more closed'],
    'more expensive': ['cheaper'],
    'more modern': ['older'],
    'more awake': ['more tired'],
    'more exciting': ['more boring'],
    'more interesting': ['more boring'],
    'more polite': ['ruder', 'more impolite'],
    'much': ['less'],
    'many': ['fewer'],
    'wider': ['narrower'],
    'closer': ['further'],
    'nearer': ['further'],
    'cleaner': ['more polluted', 'dirtier'],
    'fuller': ['emptier'],
    'quieter': ['noisier', 'louder'],
    'happier': ['unhappier'],
    'more confortable': ['more uncomfortable'],
    'more patient': ['more impatient'],
    'healthier': ['unhealthier']
}


def move_assignment(sentences_to_move, from_object, to_object, aspect, aspects, threshold_score):

    points_to_move = 0
    points_for_multiple = 0

    print('For', '\'' + aspect + '\'', 'there were moved', len(sentences_to_move),
          'sentences from', from_object.name, 'to', to_object.name, '.')
    print('----')
    for sentence in sentences_to_move:

        points = (sentence.CAM_score) / 10 if sentence.confidence < threshold_score else sentence.CAM_score

        if len(find_aspects(sentence.text, aspects)) > 1:
            points_for_multiple = points_for_multiple + points
        else:
            points_to_move = points_to_move + points

        print('-' + re.sub(' +', ' ',
                           re.sub('[^a-zA-Z0-9 ]', ' ', sentence.text)))

    from_object.sentences = [
        sentence for sentence in from_object.sentences if sentence not in sentences_to_move]
    from_object.points[aspect] = from_object.points[aspect] - points_to_move
    from_object.totalPoints = from_object.totalPoints - \
        (points_to_move + points_for_multiple)

    to_object.sentences.extend(sentences_to_move)
    to_object.add_points(aspect, points_to_move)

    if points_for_multiple > 0:
        from_object.points['multiple'] = from_object.points['multiple'] - \
            points_for_multiple
        to_object.add_points('multiple', points_for_multiple)

    print((points_to_move / (to_object.totalPoints +
                             from_object.totalPoints)) * 100, '% moved (total)')
    print((points_to_move / (to_object.points[aspect] +
                             from_object.points[aspect])) * 100, '% moved for', aspect)
    print('----')


def negation_dissolve_heuristic(object_a, object_b, aspect, aspects, threshold_score):
    markers = positive_contrary_comparatives
    filtered_sentences = get_matching_sentences(
        object_a.name, object_b.name, aspect, object_a.sentences, markers, True)

    if len(filtered_sentences) > 0:
        for sentence in filtered_sentences:
            filtered_contrary = [
                v for k, v in markers.items() if k in sentence.text]
            filtered_contrary = [
                item for sublist in filtered_contrary for item in sublist]

            if len(filtered_contrary) > 0:
                same_meaning_sentences = get_matching_sentences(
                    object_b.name, object_a.name, aspect, object_b.sentences, filtered_contrary, False)
                if len(same_meaning_sentences) > 0:
                    move_assignment(same_meaning_sentences,
                                    object_b, object_a, aspect, aspects, threshold_score)


def get_matching_sentences(object_a, object_b, aspect, sentences, markers, is_positive):
    locked_out_markers = []
    if is_positive:
        locked_out_markers = [item for sublist in list(
            positive_contrary_comparatives.values()) for item in sublist]
    else:
        locked_out_markers = [
            marker for marker in positive_contrary_comparatives]
    re_locked_out_markers = '|'.join(
        [re.escape(x) for x in locked_out_markers])
    re_markers = '|'.join([re.escape(x) for x in markers])

    regex = re.compile(r'(?=.*(?:\b' + re.escape(object_a) + r'\b.*\b' + re.escape(aspect) +
                       r'\b.*\b' + re.escape(object_b) + r'\b))(?=.*(?:\b' + re_markers + r'\b))(?!.*(?:\b' + re_locked_out_markers + r'\b))', re.IGNORECASE)

    filtered_sentences = [
        x for x in sentences if regex.search(x.text) != None]

    return filtered_sentences
