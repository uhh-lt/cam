import re


def move_assignment(sentences_to_move, from_object, to_object, aspect):
    points_to_move = 0
    print('For', '\'' + aspect + '\'', 'there were moved', len(sentences_to_move),
          'sentences from', from_object.name, 'to', to_object.name, '.')
    print('----')
    for sentence in sentences_to_move:
        # print('-' + re.sub(' +', ' ', re.sub('[^a-zA-Z0-9 ]', ' ', sentence[1])))
        points_to_move = points_to_move + sentence[0]

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
    print('----')


positive_contrary_comparatives = {
    'more': ['less', 'lower'],
    'higher': ['lower', 'smaller'],
    'bigger': ['smaller'],
    'faster': ['slower'],
    'quicker': ['slower'],
    'smarter': ['dumper'],
    'larger': ['smaller']
}

negative_contrary_comparatives = {
    'less': ['more'],
    'lower': ['more', 'higher'],
    'smaller': ['higher', 'bigger', 'larger'],
    'slower': ['faster', 'quicker'],
    'dumper': ['smarter']
}


def negation_dissolve_heuristic(object_a, object_b, aspect):
    markers = positive_contrary_comparatives
    filtered_sentences = get_matching_sentences(
        object_a.name, object_b.name, aspect, object_a.sentences, markers)

    # print(len(filtered_sentences))

    if len(filtered_sentences) > 0:
        for sentence in filtered_sentences:
            filtered_contrary = [
                v for k, v in markers.items() if k in sentence[1]]
            filtered_contrary = [
                item for sublist in filtered_contrary for item in sublist]
            # print('Filtered contrary:', filtered_contrary)

            if len(filtered_contrary) > 0:
                same_meaning_sentences = get_matching_sentences(
                    object_b.name, object_a.name, aspect, object_b.sentences, filtered_contrary)
                if len(same_meaning_sentences) > 0:
                    move_assignment(same_meaning_sentences,
                                    object_b, object_a, aspect)


def get_matching_sentences(object_a, object_b, aspect, sentences, markers):
    re_markers = '|'.join([x for x in markers])
    regex = re.compile('(?=.*' + re.escape(object_a) + r'.*' + re.escape(aspect) +
                       r'.*' + re.escape(object_b) + ')(?=.*(' + re_markers + '))', re.IGNORECASE)
    filtered_sentences = [x for x in sentences if regex.search(x[1]) != None]

    return filtered_sentences
