# encoding=utf8

import unittest
from object_comparer import what_is_better, find_winner
from sentence_clearer import clear_sentences, remove_wrong_structures
from main import Argument, Aspect
from aspect_searcher import find_aspects
from es_requester import build_object_urlpart
from link_extracter import extract_main_links
from sentence_preparation_ML import prepare_sentence_DF
import classify


class Test(unittest.TestCase):

    '''
    Testing different cases of possible object positioning as well as the presense 
    of the better/worse markers and negation (not excluded case)of the what_is_better
    method
    '''

    objA = Argument('dog')
    objB = Argument('cat')

    def test_what_is_better1(self):
        self.assertEqual(what_is_better('Dog is better than cat', self.objA, self.objB), {
                         'winner': self.objA, 'marker_cnt': 1})

    def test_what_is_better2(self):
        self.assertEqual(what_is_better('not Dog is better than cat ', self.objA, self.objB), {
                         'winner': self.objA, 'marker_cnt': 1})

    def test_what_is_better3(self):
        self.assertEqual(what_is_better('Dog is not better than cat ', self.objA, self.objB), {
                         'winner': self.objB, 'marker_cnt': 1})

    def test_what_is_better5(self):
        self.assertEqual(what_is_better('Dog is a cat', self.objA, self.objB),  {
                         'winner': self.objB, 'marker_cnt': 0})

    def test_what_is_better6(self):
        self.assertEqual(what_is_better('Dog is worse than cat', self.objA, self.objB), {
                         'winner': self.objB, 'marker_cnt': 1})

    def test_what_is_better7(self):
        self.assertTrue(what_is_better(
            'Dog is worse than cat', self.objB, self.objA))

    def test_what_is_better8(self):
        self.assertEqual(what_is_better('Dog is a cat solid', self.objB, self.objA), {
                         'marker_cnt': 0, 'winner': self.objB})

    def test_what_is_better9(self):
        self.assertEqual(what_is_better('This tortoise sculpture is made of hammer formed copper sheet metal and filled solid with concrete.',
                                        self.objB, self.objA), {'marker_cnt': 0, 'winner': self.objA})

    def test_what_is_better10(self):
        obj_a = Argument('coca-cola light')
        obj_b = Argument('pepsi light')
        self.assertEqual(what_is_better(
            'Coca Cola light tastes better than pepsi light', obj_a, obj_b), {
            'marker_cnt': 1, 'winner': obj_a})

    def test_what_is_better11(self):
        obj_a = Argument('coca1-cola light')
        obj_b = Argument('pepsi light')
        self.assertEqual(what_is_better(
            'Coca1-Cola™ light tastes better than Pepsi™ light', obj_a, obj_b), {
            'marker_cnt': 1, 'winner': obj_a})

    '''
    Testing if the removal of the following sentences work:
    1.containing '?'
    2.containing two markers of different types between the objects
    3.containing no markers between the object
    '''

    def test_clear_sentences1(self):
        s = {'Dog is worse than cat?': 20}
        s = clear_sentences(s, self.objA, self.objB)
        self.assertFalse(s)

    def test_clear_sentences2(self):
        s = {'Dog is worse than cat': 20, 'Dog didn\'t look better than cat': 20}
        s = clear_sentences(s, self.objA, self.objB)
        self.assertTrue('Dog didn\'t look better than cat' in s)

    def test_clear_sentences3(self):
        s = {'snowboarding is harder to learn but easier to master than skiing': 20}
        s = clear_sentences(s, self.objA, self.objB)
        self.assertFalse(s)

    def test_clear_sentences4(self):
        s = {'A better cat is still no dog': 20, 'Cat are worse than dog': 20}
        s = clear_sentences(s, self.objA, self.objB)
        self.assertFalse('A better cat is still no dog' in s)
        self.assertTrue(s)

    def test_clear_sentences5(self):
        s = {'Cat and dog work well together': 10, 'Cat are worse than dog': 20}
        s = clear_sentences(s, self.objA, self.objB)
        self.assertFalse('Cats and dogs work well together' in s)
        self.assertTrue(s)

    def test_clear_sentences6(self):
        s = {'Cat is worse than dog': 10,
             'Cat are more beautiful, but are harder to raise than dog': 20}
        s = clear_sentences(s, self.objA, self.objB)
        self.assertFalse(
            'Cat are wiser, but are harder to raise than dog' in s)
        self.assertTrue(s)

    def test_clear_sentences7(self):
        obj_a = Argument('cola light')
        obj_b = Argument('pepsi light')
        s = {'Cola light tastes better than pepsi light': 20}
        s = clear_sentences(s, obj_a, obj_b)
        self.assertTrue(s)

    def test_clear_sentences8(self):
        obj_a = Argument('coca-cola light')
        obj_b = Argument('pepsi light')
        s = {'Coca Cola light tastes better than pepsi light': 20}
        s = clear_sentences(s, obj_a, obj_b)
        self.assertTrue(s)

    def test_clear_sentences9(self):
        obj_a = Argument('coca-cola light')
        obj_b = Argument('pepsi light')
        s = {'Coca Cola™ light tastes better than Pepsi™ light': 20}
        s = clear_sentences(s, obj_a, obj_b)
        self.assertTrue(s)

    '''
    Testing if all parts of the find_winner method work properly
    '''

    def test_find_winner1(self):
        s = {'Dog is better than cat': 10, 'Cat is beautiful better than dog': 10,
             'Dogs are way better than cat': 10}
        result = find_winner(s, self.objA, self.objB, [])
        self.assertEqual(result['object1'], self.objA.name)
        self.assertEqual(result['object2'], self.objB.name)
        self.assertEqual(result['scoreObject1'], 2)
        self.assertEqual(result['scoreObject2'], 1)
        self.assertEqual(
            sorted(result['extractedAspectsObject1']), sorted(['way', 'dogs']))
        self.assertEqual(result['extractedAspectsObject2'], [])
        self.assertEqual(sorted(result['sentencesObject1']), sorted([
                         'Dog is better than cat', 'Dogs are way better than cat']))
        self.assertEqual(sorted(result['sentencesObject2']), sorted([
                         'Cat is beautiful better than dog']))
        self.assertEqual(result['winner'], self.objA.name)

    '''
    Test if all aspects are correctly extracted.
    '''

    def test_find_aspects1(self):
        s = 'ObjA is better than ObjB because of lower pollution, lower price and higher speed.'
        aspect1 = Aspect('pollution', 5)
        aspect2 = Aspect('price', 1)
        aspect3 = Aspect('wurstsalat', 1)
        self.assertEqual(find_aspects(
            s, [aspect1, aspect2, aspect3]), [aspect1, aspect2])
        self.assertTrue(Aspect('speed', 1)
                        not in find_aspects(s, [aspect1, aspect2]))

    def test_find_aspects2(self):
        s = ''
        aspect1 = Aspect('pollution', 5)
        aspect2 = Aspect('price', 1)
        self.assertFalse(find_aspects(
            s, [aspect1, aspect2]))

    def test_find_aspects3(self):
        s = 'Finding dory was better than finding nemo, because of the higher worldwide gross'
        aspect1 = Aspect('worldwide gross', 5)
        self.assertTrue(find_aspects(s, [aspect1]))

    def test_build_object_urlpart1(self):
        obj_a = Argument('ape')
        obj_b = Argument('gorilla')
        self.assertEqual(build_object_urlpart(
            obj_a, obj_b), 'http://ltdemos.informatik.uni-hamburg.de/depcc-index/commoncrawl2/_search?q=text:"ape"%20AND%20"gorilla"')

    def test_build_object_urlpart2(self):
        obj_a = Argument('')
        obj_b = Argument('gorilla')
        with self.assertRaises(ValueError) as context:
            build_object_urlpart(obj_a, obj_b)

        self.assertTrue('Please enter both objects!' in str(context.exception))

    def test_extract_main_links(self):
        sentencesA = ['ObjA is better than ObjB because of more time']
        sentencesB = ['ObjA is worse than ObjB because of less power']
        obj_a = Argument('ObjA')
        obj_b = Argument('ObjB')
        self.assertEqual(extract_main_links(sentencesA, sentencesB, obj_a, obj_b), {
                         'A': ['time'], 'B': ['power']})

    def test_extract_main_links2(self):
        sentencesA = [
            'Coca Cola tastes better than pepsi, because of its ingredients']
        sentencesB = [
            'Pepsi is worse than Coca-cola, because of the better sweeteners']
        obj_a = Argument('coca-cola')
        obj_b = Argument('pepsi light')
        self.assertEqual(extract_main_links(sentencesA, sentencesB, obj_a, obj_b), {
                         'A': ['ingredients'], 'B': ['sweeteners']})

    def test_extract_main_links3(self):
        sentencesA = [
            'Coca-Cola™ tastes better than pepsi, because of its ingredients']
        sentencesB = [
            'Pepsi is worse than Coca-cola™, because of the better sweeteners']
        obj_a = Argument('coca-cola')
        obj_b = Argument('pepsi light')
        self.assertEqual(extract_main_links(sentencesA, sentencesB, obj_a, obj_b), {
                         'A': ['ingredients'], 'B': ['sweeteners']})


    '''
    Test the ML parts
    '''

    def test_sentence_preparation_ML(self):
        sentenceA = ['Coca-Cola tastes better than pepsi, because of its ingredients',
            'Pepsi is worse than Coca-cola, because of the better sweeteners']

        df = prepare_sentence_DF(sentenceA, Argument('coca-cola'), Argument('pepsi'))
        self.assertNotEqual(df.loc[0]['object_a'], df.loc[1]['object_a'])


if __name__ == '__main__':
    unittest.main()
