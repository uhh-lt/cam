import unittest
from object_comparer import what_is_better, find_winner
from sentence_clearer import clear_sentences, remove_wrong_structures
from main import Argument

class Test(unittest.TestCase):
    
    '''
    Testing different cases of possible object positioning as well as the presense 
    of the better/worse markers and negation (not excluded case)of the what_is_better
    method
    '''
    
    objA = Argument('dog')
    objB = Argument('cat')
    
    def test_what_is_better1(self):
        self.assertEqual(what_is_better('Dog is better than cat', self.objA, self.objB), {'winner': self.objA, 'marker_cnt': 1})
    
    def test_what_is_better2(self):
        self.assertEqual(what_is_better('not Dog is better than cat ', self.objA, self.objB), {'winner': self.objA, 'marker_cnt': 1})

    def test_what_is_better3(self):
        self.assertEqual(what_is_better('Dog is not better than cat ', self.objA, self.objB), {'winner': self.objB, 'marker_cnt': 1})
    
    def test_what_is_better4(self):
        self.assertEqual(what_is_better('Dogs are better than cats', self.objA, self.objB), {'winner': self.objA, 'marker_cnt': 1})
    
    def test_what_is_better5(self):
        self.assertEqual(what_is_better('Dog is a cat', self.objA, self.objB),  {'winner': self.objB, 'marker_cnt': 0})

    def test_what_is_better6(self):
        self.assertEqual(what_is_better('Dog is worse than cat', self.objA, self.objB), {'winner': self.objB, 'marker_cnt': 1})
    
    def test_what_is_better7(self):
        self.assertTrue(what_is_better('Dog is worse than cat', self.objB, self.objA))
    
    def test_what_is_better8(self):
        self.assertEqual(what_is_better('Dog is a cat solid', self.objB, self.objA), {'marker_cnt': 0, 'winner': self.objB})

    def test_what_is_better9(self):
        self.assertEqual(what_is_better('This tortoise sculpture is made of hammer formed copper sheet metal and filled solid with concrete.', self.objB, self.objA), {'marker_cnt': 0, 'winner': self.objA})

    def test_what_is_better10(self):
        self.assertEqual(what_is_better('Dogs are not better than cats', self.objB, self.objA), {'winner': self.objB, 'marker_cnt': 1})

    
    def test_what_is_better11(self):
        self.assertEqual(what_is_better('Dogs are nicer, not cats', self.objA, self.objB), {'winner': self.objB, 'marker_cnt': 1})
    

    '''
    Testing if the removal of the following sentences work:
    1.containing '?' 
    2.containing negations from the list of constants 
    3.containing two markers of different types between the objects
    4.containing no markers between the object
    '''

    def test_clear_sentences1(self):
        s = ['Dog is worse than cat?']
        s = clear_sentences(s, self.objA, self.objB)
        self.assertFalse(s)
        print(s)
    
    def test_clear_sentences2(self):
        s = ['Dog is worse than cat', 'Dog didn\'t look better than cat']
        s = clear_sentences(s, self.objA, self.objB)
        self.assertFalse('Dog didn\'t look better than cat' in s)  
        self.assertTrue(s)
    
    def test_clear_sentences3(self):
        s = ['snowboarding is harder to learn but easier to master than skiing']
        s = clear_sentences(s, self.objA, self.objB)
        self.assertFalse(s)

    def test_clear_sentences4(self):
        s = ['A better cat is still no dog', 'Cats are worse than dogs']
        s = clear_sentences(s, self.objA, self.objB)
        self.assertFalse('A better cat is still no dog' in s)
        self.assertTrue(s)
    
    def test_clear_sentences5(self):
        s = ['Cats and dogs work well together', 'Cats are worse than dogs']
        s = clear_sentences(s, self.objA, self.objB)
        self.assertFalse('Cats and dogs work well together' in s)
        self.assertTrue(s)
    
    def test_clear_sentences6(self):
        s = ['Cats are worse than dogs', 'Cats are more beautiful, but are harder to raise than cats']
        s = clear_sentences(s, self.objA, self.objB)
        self.assertFalse('Dogs are wiser, but are harder to raise than cats' in s)
        self.assertTrue(s)

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