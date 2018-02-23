import inflect
from nltk import word_tokenize
from nltk.corpus import stopwords


MARKERS = ['better', 'easier', 'faster', 'nicer', 'wiser', 'cooler', 'decent', 'safer', 'superior', 'solid', 'terrific',
           'worse', 'harder', 'slower', 'poorly', 'uglier', 'poorer', 'lousy', 'nastier', 'inferior', 'mediocre']
POSITIVE_MARKERS = ['better', 'easier', 'faster', 'nicer', 'wiser',
                  'cooler', 'decent', 'safer', 'superior', 'solid', 'terrific']
NEGATIVE_MARKERS = ['worse', 'harder', 'slower', 'poorly', 'uglier',
                 'poorer', 'lousy', 'nastier', 'inferior', 'mediocre']
NEGATIONS = ['didn\'t', 'couldn\'t', 'wasn\'t', 'haven\'t', 'wouldn\'t', 'can\'t'
                'did not', 'could not', 'was not', 'have not', 'would not', 'can not'
                'didnt', 'couldnt', 'wasnt', 'havent', 'wouldnt' 'cannot']
HOSTNAME = 'http://localhost:9222/'
CRAWL_DATA_REPOS = 'commoncrawl2/_search?q=text:'
STOPWORDS = set(stopwords.words('english'))
NON_ASPECTS = ['come', 'much', 'good', 'even', 'think', 'would', 'well', 'like', 'also', 'nice', 'great', 'made', 'could']
NUMBER_STRINGS = []
p = inflect.engine()
for i in range(0,1000):
    NUMBER_STRINGS.append(p.number_to_words(i))