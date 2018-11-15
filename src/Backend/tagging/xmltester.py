import re
from random import shuffle
from xml.dom import minidom

import nltk


def convert_train_and_test():
    xmldoc_train = minidom.parse(
        'semeval_dataset/train/Consumer Electronics/subtask1/English_ABSA16_Laptops_Train_SB1_v2.xml')
    sentence_list = xmldoc_train.getElementsByTagName('sentence')
    xmldoc_test = minidom.parse(
        'semeval_dataset/test/Consumer Electronics/subtask1/EN_LAPT_SB1_TEST_.xml.gold')
    sentence_list += xmldoc_test.getElementsByTagName('sentence')
    shuffle(sentence_list)
    seperate_index_1 = int(0.7 * len(sentence_list))
    seperate_index_2 = int(0.85 * len(sentence_list))
    with open('semeval_conll_train.txt', 'w') as train_file:
        convert_xml_to_conll(train_file, sentence_list[:seperate_index_1])
    with open('semeval_conll_test.txt', 'w') as test_file:
        convert_xml_to_conll(test_file, sentence_list[seperate_index_1:seperate_index_2])
    with open('semeval_conll_dev.txt', 'w') as dev_file:
        convert_xml_to_conll(dev_file, sentence_list[seperate_index_2:])


def convert_xml_to_conll(txt_file, sentence_list):
    for sentence in sentence_list:
        text_element = sentence.getElementsByTagName('text')
        text_value = text_element[0].firstChild.nodeValue

        opinion_list = sentence.getElementsByTagName('Opinion')

        for opinion in opinion_list:
            opinion_category = opinion.attributes['category'].value
            opinion_category_super, opinion_category_specific = opinion_category.split(
                '#', 1)
            opinion_polarity = opinion.attributes['polarity'].value
            if opinion_polarity == 'positive':
                aspect_rating = '+'
            else:
                aspect_rating = '-'
            tokenized_sentence = nltk.word_tokenize(text_value)
            tag_list = nltk.pos_tag(tokenized_sentence)
            if opinion_category_super.lower() != 'laptop':
                write_file(txt_file, tag_list, opinion_category_super, aspect_rating)
            if opinion_category_specific.lower() not in ['general', 'miscellaneous']:
                write_file(txt_file, tag_list, opinion_category_specific, aspect_rating)


def write_file(txt_file, tag_list, opinion_category, aspect_rating):
    for pos_tag in tag_list:
        txt_file.write(pos_tag[0] + ' ' + pos_tag[1] + ' _ ' + opinion_category.lower() + aspect_rating + '\n')
    txt_file.write('\n')
