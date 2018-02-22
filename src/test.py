import unittest
from object_comparer import is_better_than, find_winner
from sentence_clearer import clear_sentences

class Test(unittest.TestCase):

    '''
    Testing different cases of possible object positioning as well as the presense 
    of the better/worse markers and negation (not excluded case)of the is_better_than
    method
    '''

    def test_is_better_than1(self):
        self.assertTrue(is_better_than('Dog is better than cat', 'dog', 'cat'))
    
    def test_is_better_than2(self):
        self.assertTrue(is_better_than('not Dog is better than cat ', 'dog', 'cat'))

    def test_is_better_than3(self):
        self.assertFalse(is_better_than('Dog is not better than cat ', 'dog', 'cat'))
    
    def test_is_better_than4(self):
        self.assertFalse(is_better_than('Dog is better than cat', 'cat', 'dog'))
    
    def test_is_better_than5(self):
        self.assertEqual(is_better_than('Dog is a cat', 'dog', 'cat'), None)

    def test_is_better_than6(self):
        self.assertFalse(is_better_than('Dog is worse than cat', 'dog', 'cat'))
    
    def test_is_better_than7(self):
        self.assertTrue(is_better_than('Dog is worse than cat', 'cat', 'dog'))

    def test_is_better_than8(self):
        self.assertEqual(is_better_than('Dog is a cat solid', 'cat', 'dog'), None)

    def test_is_better_than9(self):
        self.assertEqual(is_better_than('This tortoise sculpture is made of hammer formed copper sheet metal and filled solid with concrete.', 'hammer', 'tortoise'), None)
            

    '''
    Testing if the removal of the sentences containing '?' and negations from
    the list of constants works (clear_sentences method)
    '''
    def test_clear_sentences1(self):
        s = ['Dog is worse than cat?']
        s = clear_sentences(s)
        self.assertFalse(s)
    
    def test_clear_sentences2(self):
        s = ['Dog is worse than cat', 'Dog didn\'t look better than cat']
        s = clear_sentences(s)
        self.assertFalse('Dog didn\'t look better than cat' in s)  
        self.assertTrue(s)
    
    def test_clear_sentences3(self):
        s = ['snowboarding is harder to learn but easier to master than skiing']
        s = clear_sentences(s)
        self.assertFalse(s)

    '''
    Testing if all parts of the find_winner method work properly
    '''
    def test_find_winner1(self):
        s = ['Dog is better than cat', 'Cat is definitely better than dog', 'Dogs is way better than cat']
        result = find_winner(s, 'dog', 'cat')
        self.assertEqual(result['object 1'], 'dog')
        self.assertEqual(result['object 2'], 'cat')
        self.assertEqual(result['score object 1'], 2)
        self.assertEqual(result['score object 2'], 1)
        self.assertEqual(result['winner'], 'dog')

if __name__ == '__main__':
    unittest.main()