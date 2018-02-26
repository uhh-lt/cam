import unittest
from object_comparer import is_better_than, find_winner
from sentence_clearer import clear_sentences
from main import Argument

class Test(unittest.TestCase):

    '''
    Testing different cases of possible object positioning as well as the presense 
    of the better/worse markers and negation (not excluded case)of the is_better_than
    method
    '''
    objA = Argument('dog')
    objB = Argument('cat')
    def test_is_better_than1(self):
        self.assertTrue(is_better_than('Dog is better than cat', self.objA, self.objB))
    
    def test_is_better_than2(self):
        self.assertTrue(is_better_than('not Dog is better than cat ', self.objA, self.objB))

    def test_is_better_than3(self):
        self.assertFalse(is_better_than('Dog is not better than cat ', self.objA, self.objB))
    
    def test_is_better_than4(self):
        self.assertFalse(is_better_than('Dog is better than cat', self.objB, self.objA))
    
    def test_is_better_than5(self):
        self.assertEqual(is_better_than('Dog is a cat', self.objA, self.objB), False)

    def test_is_better_than6(self):
        self.assertFalse(is_better_than('Dog is worse than cat', self.objA, self.objB))
    
    def test_is_better_than7(self):
        self.assertTrue(is_better_than('Dog is worse than cat', self.objB, self.objA))

    '''
    def test_is_better_than8(self):
        self.assertEqual(is_better_than('Dog is a cat solid', self.objB, self.objA), None)
    '''

    def test_is_better_than9(self):
        self.assertEqual(is_better_than('This tortoise sculpture is made of hammer formed copper sheet metal and filled solid with concrete.', self.objB, self.objA), False)

    def test_is_better_than10(self):
        self.assertFalse(is_better_than('Dogs are not better than cats', self.objA, self.objB))

    def test_is_better_than11(self):
        self.assertFalse(is_better_than('Dogs are nicer, not cats', self.objA, self.objB))
    
            

    '''
    Testing if the removal of the sentences containing '?' and negations from
    the list of constants  works (clear_sentences method)
    '''
    def test_clear_sentences1(self):
        s = ['Dog is worse than cat?']
        s = clear_sentences(s, self.objA, self.objB)
        self.assertFalse(s)
    
    def test_clear_sentences2(self):
        s = ['Dog is worse than cat', 'Dog didn\'t look better than cat']
        s = clear_sentences(s, self.objA, self.objB)
        self.assertFalse('Dog didn\'t look better than cat' in s)  
        self.assertTrue(s)
    
    def test_clear_sentences3(self):
        s = ['snowboarding is harder to learn but easier to master than skiing']
        s = clear_sentences(s, self.objA, self.objB)
        self.assertFalse(s)

    '''
    Testing if all parts of the find_winner method work properly
    '''
    def test_find_winner1(self):
        s = ['Dog is better than cat', 'Cat is definitely better than dog', 'Dogs are way better than cat']
        result = find_winner(s, self.objA, self.objB, [])
        self.assertEqual(result['object 1'], self.objA.name)
        self.assertEqual(result['object 2'], self.objB.name)
        self.assertEqual(result['score object 1'], 2)
        self.assertEqual(result['score object 2'], 1)
        self.assertEqual(result['main aspects object 1'], {'dogs': 1, 'way': 1})
        self.assertEqual(result['main aspects object 2'], {'definitely': 1})
        self.assertEqual(result['object 1 sentences'], ['Dog is better than cat', 'Dogs are way better than cat'])
        self.assertEqual(result['object 2 sentences'], ['Cat is definitely better than dog'])
        self.assertEqual(result['winner'], self.objA.name)

if __name__ == '__main__':
    unittest.main()