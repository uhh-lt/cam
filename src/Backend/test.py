import unittest

from main import Argument
from marker_approach.object_comparer import what_is_better, find_winner
from ml_approach.sentence_preparation_ML import prepare_sentence_DF
from utils.link_extracter import extract_main_links
from utils.objects import Sentence
from utils.sentence_clearer import clear_sentences
from utils.url_builder import build_object_urlpart


class Test(unittest.TestCase):
    """
    Testing different cases of possible object positioning as well as the presense
    of the better/worse markers and negation (not excluded case)of the what_is_better
    method
    """

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
        self.assertEqual(what_is_better('Dog is a cat', self.objA, self.objB), {
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
        self.assertEqual(what_is_better(
            'This tortoise sculpture is made of hammer formed copper sheet metal and filled solid with concrete.',
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
        s = [Sentence('Dog is worse than cat?', 20, '', '')]
        s = clear_sentences(s, self.objA, self.objB)
        self.assertFalse(s)

    def test_clear_sentences2(self):
        s = [Sentence('Dog is worse than cat', 20, '', ''), Sentence(
            'Dog didn\'t look better than cat', 20, '', '')]
        s = clear_sentences(s, self.objA, self.objB)
        self.assertTrue('Dog didn\'t look better than cat' in [
            sentence.text for sentence in s])

    def test_clear_sentences3(self):
        s = [Sentence(
            'snowboarding is harder to learn but easier to master than skiing', 20, '', '')]
        s = clear_sentences(s, self.objA, self.objB)
        self.assertFalse(s)

    def test_clear_sentences4(self):
        s = [Sentence('A better cat is still no dog', 20, '', ''),
             Sentence('Cat are worse than dog', 20, '', '')]
        s = clear_sentences(s, self.objA, self.objB)
        self.assertFalse('A better cat is still no dog' in [
            sentence.text for sentence in s])
        self.assertTrue(s)

    def test_clear_sentences5(self):
        s = [Sentence('Cat and dog work well together', 10, '', ''),
             Sentence('Cat are worse than dog', 20, '', '')]
        s = clear_sentences(s, self.objA, self.objB)
        self.assertFalse('Cats and dogs work well together' in [
            sentence.text for sentence in s])
        self.assertTrue(s)

    def test_clear_sentences6(self):
        s = [Sentence('Cat is worse than dog', 10, '', ''),
             Sentence('Cat are more beautiful, but are harder to raise than dog', 20, '', '')]
        s = clear_sentences(s, self.objA, self.objB)
        self.assertFalse(
            'Cat are wiser, but are harder to raise than dog' in [sentence.text for sentence in s])
        self.assertTrue(s)

    def test_clear_sentences7(self):
        obj_a = Argument('cola light')
        obj_b = Argument('pepsi light')
        s = [Sentence('Cola light tastes better than pepsi light', 20, '', '')]
        s = clear_sentences(s, obj_a, obj_b)
        self.assertTrue(s)

    def test_clear_sentences8(self):
        obj_a = Argument('coca-cola light')
        obj_b = Argument('pepsi light')
        s = [
            Sentence('Coca Cola light tastes better than pepsi light', 20, '', '')]
        s = clear_sentences(s, obj_a, obj_b)
        self.assertTrue(s)

    def test_clear_sentences9(self):
        obj_a = Argument('coca-cola light')
        obj_b = Argument('pepsi light')
        s = [
            Sentence('Coca Cola™ light tastes better than Pepsi™ light', 20, '', '')]
        s = clear_sentences(s, obj_a, obj_b)
        self.assertTrue(s)

    '''
    Testing if all parts of the find_winner method work properly
    '''

    def test_find_winner1(self):
        s = [Sentence('Dog is better than cat', 10, 'http://test.com', 5),
             Sentence('Cat is beautiful better than dog', 10, 'http://test2.com', 7),
             Sentence('Dogs are way better than cat', 10, 'http://test3.com', 6)]
        result = find_winner(s, self.objA, self.objB, [])
        obj_1 = result['object1']
        obj_2 = result['object2']

        self.assertEqual(obj_1['name'], self.objA.name)
        self.assertEqual(obj_2['name'], self.objB.name)
        self.assertEqual(obj_1['totalPoints'], 2.0)
        self.assertEqual(obj_2['totalPoints'], 1.0)
        self.assertEqual(obj_1['points'], {'none': 2.0})
        self.assertEqual(obj_2['points'], {'none': 1.0})
        sentences1 = [sentence['text'] for sentence in obj_1['sentences']]
        sentences2 = [sentence['text'] for sentence in obj_2['sentences']]
        self.assertEqual(sorted(sentences1), sorted(
            ['Dog is better than cat', 'Dogs are way better than cat']))
        self.assertEqual(sorted(sentences2), sorted(
            ['Cat is beautiful better than dog']))
        self.assertEqual(result['winner'], self.objA.name)
        self.assertEqual(result['sentenceCount'], 3.0)

    def test_build_object_urlpart1(self):
        obj_a = Argument('ape')
        obj_b = Argument('gorilla')
        url = build_object_urlpart(obj_a, obj_b)
        self.assertTrue(
            url == 'http://ltdemos.informatik.uni-hamburg.de/depcc-index/depcc/_search?q=text:"ape"%20AND%20"gorilla"'
            or url ==
            'http://ltdemos.informatik.uni-hamburg.de/depcc-index/commoncrawl2/_search?q=text:"ape"%20AND%20"gorilla"')

    def test_build_object_urlpart2(self):
        obj_a = Argument('')
        obj_b = Argument('gorilla')
        with self.assertRaises(ValueError) as context:
            build_object_urlpart(obj_a, obj_b)

        self.assertTrue('Please enter both objects!' in str(context.exception))

    def test_extract_main_links(self):
        sentences_a = [
            Sentence('ObjA is better than ObjB because of more time', 10, '', '')]
        sentences_b = [
            Sentence('ObjA is worse than ObjB because of less power', 10, '', '')]
        obj_a = Argument('ObjA')
        obj_b = Argument('ObjB')
        self.assertEqual(extract_main_links(sentences_a, sentences_b, obj_a, obj_b), {
            'A': ['time'], 'B': ['power']})

    def test_extract_main_links2(self):
        sentences_a = [Sentence(
            'Coca Cola tastes better than pepsi, because of its ingredients', 20, '', '')]
        sentences_b = [Sentence(
            'Pepsi is worse than Coca-cola, because of the better sweeteners', 20, '', '')]
        obj_a = Argument('coca-cola')
        obj_b = Argument('pepsi light')
        self.assertEqual(extract_main_links(sentences_a, sentences_b, obj_a, obj_b), {
            'A': ['ingredients'], 'B': ['sweeteners']})

    def test_extract_main_links3(self):
        sentences_a = [Sentence(
            'Coca-Cola™ tastes better than pepsi, because of its ingredients', 20, '', '')]
        sentences_b = [Sentence(
            'Pepsi is worse than Coca-cola™, because of the better sweeteners', 20, '', '')]
        obj_a = Argument('coca-cola')
        obj_b = Argument('pepsi light')
        self.assertEqual(extract_main_links(sentences_a, sentences_b, obj_a, obj_b), {
            'A': ['ingredients'], 'B': ['sweeteners']})

    '''
    Test the ML parts
    '''

    def test_sentence_preparation_ML(self):
        sentence_a = [Sentence('Coca-Cola tastes better than pepsi, because of its ingredients', 20, '', ''),
                      Sentence('Pepsi is worse than Coca-cola, because of the better sweeteners', 20, '', '')]

        df = prepare_sentence_DF(sentence_a, Argument(
            'coca-cola'), Argument('pepsi'))
        self.assertNotEqual(df.loc[0]['object_a'], df.loc[1]['object_a'])


if __name__ == '__main__':
    unittest.main()
