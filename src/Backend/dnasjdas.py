import nltk
from nltk.tokenize import word_tokenize

wordlist = word_tokenize('This \'is a . test; some-thing')
wordlist = [word for word in wordlist if len(word) > 1]
print(wordlist)
