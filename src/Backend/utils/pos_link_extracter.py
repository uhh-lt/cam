import operator
import re

import nltk

from marker_approach.constants import NON_LINKS, NUMBER_STRINGS, STOPWORDS
from utils.objects import Argument
from utils.sentence_context_getter import get_sentence_context

# POS tags that represent a comparative adjective or adverb
COMP_TAGS = ['JJR', 'RBR']
# POS tags that should be ignored when building successive aspects
UNUSED_COMPARATIVE_SUCCESSOR_POS_TAGS = ["''", "--", "FW", "SYM", "WP$"]
# POS tags that represent a pronoun
PRONOUNS = ['PRP', 'PRP$', 'WP']
# conjunctions that act as a trigger to make all subsequent nouns aspects
ASPECT_CONJUNCTIONS = ['because']
# conjunctions that only act as a trigger to make all subsequent nouns aspects
# if the conjunction is followed by a pronoun and a verb
ASPECT_CONJUNCTIONS_NEEDING_PR_VB_SUCCESSORS = ['as', 'since', 'for']

# we don't want negative comparative words as aspects but instead their
# positive counterpart
NEGATIVE_MARKER_MAP = {'harder': 'easier',
                       'slower': 'faster',
                       'poorer': 'richer',
                       'narrower': 'wider',
                       'smaller': 'bigger',
                       'shorter': 'longer'}

# list of words that seem inappropriate as aspects
UNUSED_ASPECTS = ['better', 'more', 'worse',
                  'less', 'way', 'somebody',
                  'people', 'stuff', 'folks',
                  'likes', 'fact', 'thing',
                  'things', 'someone', 'something',
                  'sucks', 'lol', 'idiot', 'myriad',
                  'one', 'ones', 'enough', 'lot',
                  'nothing', 'case', 'others',
                  'anything', 'matter', 'fewer',
                  'lesser', 'closer', 'later',
                  'reasons', 'everyone', 'whole',
                  'anyone', 'regards', 'anybody',
                  'yours', 'reason', 'need',
                  'lower', 'yea', 'why', 'everything',
                  'helluva', 'bc', 'hell',
                  'opinion', 'nothing', 'aspects',
                  'aspect']

# aspects should only contain letters, numbers and specific special characters
regex = re.compile('[^a-zA-Z0-9+#]+')


def extract_main_links(object_a: Argument, object_b: Argument):
    '''
    Extract the most common aspects for two lists of strings.

    object_a:       the first object to be compared

    object_b:       the second object to be compared
    '''
    # amount of sentences to use for context aspect generation
    context_sent_amount = 0
    # amount of sentences to use within each context (before and after the
    # actual sentence)
    context_size = 0

    object_a_aspect_dict = {}
    object_b_aspect_dict = {}
    sentence_scores_a = sorted(
        [sentence.ES_score for sentence in object_a.sentences], reverse=True)
    sentence_scores_b = sorted(
        [sentence.ES_score for sentence in object_b.sentences], reverse=True)
    min_points_for_context_aspect_extraction_a = 0
    min_points_for_context_aspect_extraction_b = 0
    if sentence_scores_a:
        min_points_for_context_aspect_extraction_a = sentence_scores_a[
            min(len(sentence_scores_a) - 1, context_sent_amount)]
    if sentence_scores_b:
        min_points_for_context_aspect_extraction_b = sentence_scores_b[
            min(len(sentence_scores_b) - 1, context_sent_amount)]

    aspect_dicts = [object_a_aspect_dict, object_b_aspect_dict]
    sentence_lists = [object_a.sentences, object_b.sentences]
    min_points_list = [min_points_for_context_aspect_extraction_a,
                       min_points_for_context_aspect_extraction_b]
    for aspect_dict, sentence_list, min_points in zip(aspect_dicts,
                                                      sentence_lists,
                                                      min_points_list):
        for sentence in sentence_list:
            get_aspects(
                sentence.text, aspect_dict, object_a.name, object_b.name)
            if sentence.ES_score >= min_points:
                document_id = list(sentence.id_pair.keys())[0]
                context = get_sentence_context(
                    document_id, sentence.id_pair[document_id],
                    context_size)
                for context_sentence in context:
                    sentence.add_context_aspects(get_aspects(
                        context_sentence['text'], aspect_dict,
                        object_a.name, object_b.name))
    do_tf_idf(object_a_aspect_dict, object_b_aspect_dict)

    object_a_aspects = get_top_10_aspects(object_a_aspect_dict)
    object_b_aspects = get_top_10_aspects(object_b_aspect_dict)

    result = {}
    result['A'] = object_a_aspects
    result['B'] = object_b_aspects
    return result


def get_aspects(sentence, aspect_dict, a_name, b_name):
    aspects = []

    tokenized_sentence = nltk.word_tokenize(sentence)
    tag_list = nltk.pos_tag(tokenized_sentence)

    aspects += get_comparative_aspects_with_successors(aspect_dict, tag_list)

    aspects += get_comparative_aspects(aspect_dict, tag_list, a_name, b_name)

    aspects += get_noun_aspects(aspect_dict, tag_list, a_name, b_name)

    return aspects


def get_comparative_aspects_with_successors(aspect_dict, tag_list):
    '''
    Get aspects that start with a comparative adjective or adverb that's
    followed by "for" or "to". Example: easier for typing.

    aspect_dict:    dictionary containing aspects and their frequencies

    tag_list:       list containing pairs of words and their POS tags
    '''
    aspects = []

    for comparative_pair in [pair for pair in tag_list
                             if pair[1] in COMP_TAGS]:
        index_of_comparative_pair = tag_list.index(comparative_pair)
        current_index = index_of_comparative_pair
        try:
            next_pair = tag_list[current_index + 1]
        except IndexError:
            # comparative pair was the last pair of the tag list and thus is
            # not relevant
            continue
        # currently only words followed by "for" or "to" are considered
        if next_pair[0].lower() == 'for' or next_pair[0].lower() == 'to':
            aspect = clean_word(comparative_pair[0])
            aspect = map_to_positive(aspect)
            while True:
                current_index += 1
                try:
                    next_pair = tag_list[current_index]
                except IndexError:
                    if current_index - index_of_comparative_pair > 2:
                        append_aspect(aspect, aspect_dict)
                        aspects.append(aspect)
                    break
                successor = clean_word(next_pair[0])
                successor = map_to_positive(successor)
                if successor_is_useful(next_pair):
                    aspect += ' ' + successor
                else:
                    append_aspect(aspect, aspect_dict)
                    aspects.append(aspect)
                    break
    return aspects


def successor_is_useful(successor):
    '''
    Check if a successor is useful for the comparative aspects with successors.
    '''
    return not(len(successor[1]) == 1
               or successor[1] in UNUSED_COMPARATIVE_SUCCESSOR_POS_TAGS
               or successor[0] == 'than')


def get_comparative_aspects(aspect_dict, tag_list,
                            a_name, b_name):
    '''
    Get comparative adjectives or adverbs as aspects.

    aspect_dict:    dictionary containing aspects and their frequencies

    tag_list:       list containing pairs of words and their POS tags
    '''
    aspects = []

    comparative_aspects = [pair[0]
                           for pair in tag_list if pair[1] in COMP_TAGS]
    comparative_aspects = [clean_word(comparative_aspect)
                           for comparative_aspect in comparative_aspects]
    comparative_aspects = [comparative_aspect for comparative_aspect
                           in comparative_aspects
                           if is_useful(comparative_aspect,
                                        a_name, b_name)]
    for comparative_aspect in comparative_aspects:
        comparative_aspect = map_to_positive(comparative_aspect)
        append_aspect(comparative_aspect, aspect_dict)
        aspects.append(comparative_aspect)
    return aspects


def get_noun_aspects(aspect_dict, tag_list, a_name, b_name):
    '''
    Get nouns as aspects.

    aspect_dict:    dictionary containing aspects and their frequencies

    tag_list:       list containing pairs of words and their POS tags
    '''
    aspects = []

    aspect_conjunction_index = get_index_for_aspect_conjunctions(tag_list)
    if aspect_conjunction_index != -1:
        # only nouns that appear after the triggering conjunction are relevant
        nouns = get_nouns_after_index(
            aspect_conjunction_index, tag_list, a_name, b_name)
        for noun in nouns:
            append_aspect(noun, aspect_dict)
            aspects.append(noun)

    reason_index, before = get_index_for_reason(tag_list, a_name, b_name)
    if reason_index != -1:
        if before:
            nouns = get_nouns_before_index(
                reason_index, tag_list, a_name, b_name)
        else:
            nouns = get_nouns_after_index(
                reason_index, tag_list, a_name, b_name)
        for noun in nouns:
            append_aspect(noun, aspect_dict)
            aspects.append(noun)
    return aspects


def get_index_for_aspect_conjunctions(tag_list):
    '''
    Get the index of the first triggering conjunction or -1 if there is none.
    '''
    indices = [tag_list.index(pair) for pair in tag_list if pair[0] in
               ASPECT_CONJUNCTIONS]
    pairs_needing_successors = [pair for pair in tag_list if pair[0] in
                                ASPECT_CONJUNCTIONS_NEEDING_PR_VB_SUCCESSORS]
    try:
        for pair in pairs_needing_successors:
            if tag_list[tag_list.index(pair) + 1][1] in PRONOUNS and 'VB' in \
                    tag_list[tag_list.index(pair) + 2][1]:
                indices.append(
                    tag_list.index(pair))
    except IndexError:
        pass
    remove_not_aspect_conjunction_indices(indices, tag_list)
    if indices:
        return min(indices)
    else:
        return -1


def get_index_for_reason(tag_list, a_name, b_name):
    '''
    Get the index of the first appearance of reason or -1 if there is none,
    as well as a Boolean that tells whether the relevant nouns should be looked
    for before (True) or after (False) this index.
    '''
    reason_pairs = [pair for pair in tag_list if pair[0] == 'reason']
    reasons_pairs = [pair for pair in tag_list if pair[0] == 'reasons']

    reason_indices = [tag_list.index(pair) for pair in reason_pairs]
    reason_index = len(tag_list) + 1
    if reason_indices:
        reason_index = min(reason_indices)
    reasons_indices = [tag_list.index(pair) for pair in reasons_pairs]
    reasons_index = len(tag_list) + 1
    if reasons_indices:
        reasons_index = min(reasons_indices)

    if not reason_indices and not reasons_indices:
        return -1, False

    index = min(reason_index, reasons_index)
    if reason_index < reasons_index:
        word_to_look_for = 'is'
    else:
        word_to_look_for = 'are'
    if index == -1:
        return -1, False
    try:
        # example: "... reason object is better than object ..."
        if (tag_list[index + 1][0] == a_name
                or tag_list[index + 1][0] == b_name) \
                and 'VB' in tag_list[index + 2][1] \
                and tag_list[index + 3][1] in COMP_TAGS \
                and tag_list[index + 4][0] == 'than' \
                and (tag_list[index + 5][0] == a_name
                     or tag_list[index + 5][0] == b_name) \
                and tag_list[index + 1][0] != tag_list[index + 5][0]:
            return index, get_before(tag_list, index, 5, word_to_look_for)
        if tag_list[index + 1][0] in ['for', 'why']:
            return index, get_before(tag_list, index, 1, word_to_look_for)
        return -1, False
    except IndexError:
        return -1, False


def get_before(tag_list, index, offset, word_to_look_for):
    indices_before = [tag_list.index(pair) for pair in tag_list
                      if pair[0] == word_to_look_for
                      and tag_list.index(pair) < index]
    indices_after = [tag_list.index(pair) for pair in tag_list
                     if pair[0] == word_to_look_for
                     and tag_list.index(pair) > index + offset]
    distance_before = len(tag_list) + 1
    if indices_before:
        distance_before = index - max(indices_before)
    distance_after = len(tag_list) + 1
    if indices_after:
        distance_after = min(indices_after) - index
    if distance_before < distance_after:
        return True
    return False


def remove_not_aspect_conjunction_indices(aspect_conjunction_indices,
                                          tag_list):
    '''
    Remove indices that belong to a conjunction that has a not before it.
    '''
    indices_to_remove = []
    for aspect_conjunction_index in aspect_conjunction_indices:
        if aspect_conjunction_index > 0 \
                and clean_word(
                    tag_list[aspect_conjunction_index - 1][0]) == 'not':
            indices_to_remove.append(aspect_conjunction_index)
    for index in indices_to_remove:
        aspect_conjunction_indices.remove(index)


def get_nouns_after_index(index, tag_list, a_name, b_name):
    '''
    Get all nouns that appear after the specified index.
    '''
    nouns = [pair[0] for pair in tag_list if 'NN' in pair[1]
             and tag_list.index(pair) > index]
    nouns = [clean_word(noun) for noun in nouns]
    return [noun for noun in nouns
            if is_useful(noun, a_name, b_name)]


def get_nouns_before_index(index, tag_list, a_name, b_name):
    '''
    Get all nouns that appear before the specified index.
    '''
    nouns = [pair[0] for pair in tag_list if 'NN' in pair[1]
             and tag_list.index(pair) < index]
    nouns = [clean_word(noun) for noun in nouns]
    return [noun for noun in nouns
            if is_useful(noun, a_name, b_name)]


def is_useful(word, a_name, b_name):
    '''
    Check if the word is useful as an aspect when object_a and object_b are
    compared.
    '''
    return word not in STOPWORDS \
        and word != a_name \
        and word != b_name \
        and word not in NON_LINKS \
        and word not in NUMBER_STRINGS \
        and word not in UNUSED_ASPECTS \
        and len(word) > 1


def clean_word(word):
    '''
    Put a word to lower case and removes all characters specified in regex.
    '''
    return regex.sub('', word.lower())


def append_aspect(aspect, aspect_dict):
    ''' Append an aspect to an aspect_dictionary. '''
    if len(aspect) > 0:
        if aspect not in aspect_dict.keys():
            aspect_dict[aspect] = 0
        aspect_dict[aspect] += 1


def map_to_positive(word):
    '''
    If the word is a negative marker, map it to its positive counterpart.
    '''
    if word in NEGATIVE_MARKER_MAP:
        word = NEGATIVE_MARKER_MAP[word]
    return word


def do_tf_idf(object_a_aspects, object_b_aspects):
    '''
    Apply the Term Frequency - Inverse Document Frequency to the frequencies of
    the words. Note that this is actually not strictly the original formula but
    instead uses a simplified metric: For each word, its frequency for one
    object is divided by the frequency of this word for the other object.

    To keep aspects unique among the objects, not only are those numbers
    calculated but after that the aspect is removed completely for the word
    that had the lower number for it. If numbers are equal for both objects the
    word is removed as an aspect for both objects instead as it doesn't seem to
    help distinguish between the objects.
    '''
    aspects_to_remove_for_object_a = []
    aspects_to_remove_for_object_b = []
    for aspect in object_a_aspects.keys():
        if aspect in object_b_aspects.keys():
            value_1 = object_a_aspects[aspect]
            value_2 = object_b_aspects[aspect]
            if value_1 > value_2:
                object_a_aspects[aspect] /= value_2
                aspects_to_remove_for_object_b.append(aspect)
            elif value_2 > value_1:
                object_b_aspects[aspect] /= value_1
                aspects_to_remove_for_object_a.append(aspect)
            else:
                aspects_to_remove_for_object_a.append(aspect)
                aspects_to_remove_for_object_b.append(aspect)
    for remove_list, aspect_dict in \
            zip([aspects_to_remove_for_object_a,
                 aspects_to_remove_for_object_b],
                [object_a_aspects, object_b_aspects]):
        for aspect in remove_list:
            aspect_dict.pop(aspect)


def get_top_10_aspects(aspect_dict):
    ''' Get the top 10 aspects of the specified dictionary. '''
    result = []
    while (len(result) < 10 and aspect_dict):
        top_aspect = max(aspect_dict, key=aspect_dict.get)
        result.append(top_aspect)
        aspect_dict.pop(top_aspect)
    return result
