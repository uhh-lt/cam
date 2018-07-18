import re
from utils.regex_service import find_pos_in_sentence
from collections import Counter
from marker_approach.constants import STOPWORDS
from nltk import word_tokenize, pos_tag
import spacy

# STOPWORDS = ['the', 'and', 'in', 's', 'of', 'to', 'a', 'or', 'is', 'are', 'that', 'by', 'be', 'as', 'its', 'has', 'some', 'which', 'than', 'on', 'would']
not_filter = ['most', 'after', 'above', 'more', 'before', 'same', 'under', 'below']
stopwords = [word for word in STOPWORDS if word not in not_filter]




def find_most_frequent_words(object_a, object_b, sentences, aspect):

    find_most_frequent_comparative_word(object_a, object_b, sentences, aspect)
    
    frequent_words = {}
    labels = set()

    for sentence in sentences:
        word_list = word_tokenize(sentence)
        tag_list = pos_tag(word_list)

        if object_a in word_list and object_b in word_list and aspect in word_list:
            index_a = word_list.index(object_a)
            index_b = word_list.index(object_b)
            index_c = word_list.index(aspect)
            if index_a > index_b:
                index_a = len(word_list) - word_list[::-1].index(object_a) - 1
            else:
                index_b = len(word_list) - word_list[::-1].index(object_b) - 1
        else:
            continue

        indices = [['a', index_a], ['b', index_b], ['c', index_c]]
        indices.sort(key=lambda elem: elem[1])

        label = '_'.join([x[0] for x in indices])
        if '1_'+label not in frequent_words:
            labels.add(label)
            frequent_words['0_'+label] = []
            frequent_words['1_'+label] = []
            frequent_words['2_'+label] = []
            frequent_words['3_'+label] = []
        frequent_words['0_' + label].extend(get_words_between(word_list, tag_list, -1, indices[0][1], object_a, object_b))
        frequent_words['1_' + label].extend(get_words_between(word_list, tag_list, indices[0][1], indices[1][1], object_a, object_b))
        frequent_words['2_' + label].extend(get_words_between(word_list, tag_list, indices[1][1], indices[2][1], object_a, object_b))
        frequent_words['3_' + label].extend(get_words_between(word_list, tag_list, indices[2][1], len(word_list), object_a, object_b))

    for key in frequent_words:
        frequent_words[key] = Counter(frequent_words[key]).most_common(3)
    print_frequent_words(frequent_words, object_a, object_b, aspect, labels)


def get_words_between(word_list, tag_list, start, end, object_a, object_b):
    return [word for word in word_list[start+1:end] if word != object_a and word != object_b and check_tag(word, tag_list) or word =='than']

def check_tag(word, taglist):
    for tag in taglist:
        if word == tag[0] and tag[1] in ['JJR', 'RBR']:
            return True

def print_frequent_words(frequent_words, object_a, object_b, aspect, labels):
    for label in labels:
        if label == 'a_c_b':
            print(frequent_words['0_'+label], '...', object_a, '...', frequent_words['1_'+label], '...', aspect, '...', frequent_words['2_'+label], '...', object_b, '...', frequent_words['3_'+label])
        elif label == 'a_b_c':
            print(frequent_words['0_'+label], '...', object_a, '...', frequent_words['1_'+label], '...', object_b, '...', frequent_words['2_'+label], '...', aspect, '...', frequent_words['3_'+label])
        elif label == 'b_a_c':
            print(frequent_words['0_'+label], '...', object_b, '...', frequent_words['1_'+label], '...', object_a, '...', frequent_words['2_'+label], '...', aspect, '...', frequent_words['3_'+label])
        elif label == 'b_c_a':
            print(frequent_words['0_'+label], '...', object_b, '...', frequent_words['1_'+label], '...', aspect, '...', frequent_words['2_'+label], '...', object_a, '...', frequent_words['3_'+label])
        elif label == 'c_a_b':
            print(frequent_words['0_'+label], '...', aspect, '...', frequent_words['1_'+label], '...', object_a, '...', frequent_words['2_'+label], '...', object_b, '...', frequent_words['3_'+label])
        elif label == 'c_b_a':
            print(frequent_words['0_'+label], '...', aspect, '...', frequent_words['1_'+label], '...', object_b, '...', frequent_words['2_'+label], '...', object_a, '...', frequent_words['3_'+label])


def find_most_frequent_comparative_word(object_a, object_b, sentences, aspect):
    comparative_words = []
    for sentence in sentences:
        if find_pos_in_sentence(aspect, sentence) == -1:
            continue
        word_list = word_tokenize(sentence)
        tag_list = pos_tag(word_list)
        comparative_words.extend(get_words_between(word_list, tag_list, -1, len(word_list), object_a, object_b))
    comparative_words = Counter(comparative_words).most_common(3)
    print('>>>>>>>>>', comparative_words)


find_most_frequent_words("earth", "venus", [
                         "and venus has lower mass than earth and 90 bars of co2 pressure and it is 500 degress hot, why 1 mil.", "the diameter of venus is 12, 092 km ( sole 650 km less than the earth ' s ) and its mass is 81. 5 % of the earth ' s."], "mass")
nlp = spacy.load('en')
doc = nlp('and venus has lower mass than earth and 90 bars of co2 pressure and it is 500 degress hot, why 1 mil.'
    'the diameter of venus is 12, 092 km ( sole 650 km less than the earth \' s ) and its mass is 81. 5 % of the earth \' s.')
for token in doc:
    if token.dep_ in ['appos', 'nmod', 'acomp']:
        print(token.text)
    # print(token.text, token.dep_, token.head.text, token.head.pos_,
    #       [child for child in token.children])