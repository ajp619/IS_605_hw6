# -*- coding: utf-8 -*-

"""
IS 605: HW6

Assignment:
Take a document in English and print out the estimated probabilities
for each of the words that occur in that document.  Remove all
punctuation (quotes, commas, hyphens etc) before you perform your calculations.
Extend your program to calculate the probability of two words occurring adjacent to
each other. It should take in a document, and two words (say the and for) and compute
the probability of each of the words occurring in the document and the joint probability
of both of them occurring together. The order of the two words is not important
"""

__author__ = 'Aaron Palumbo'

# Import required modules
import codecs
import unicodedata
from collections import Counter
import pandas as pd
from ggplot import *


def read_text_file(file_name):
    with codecs.open(file_name, mode='r', encoding='utf-8') as myfile:
        return myfile.read().replace('\n', ' ')


def clean_text(mystring):
    # Check unicode category for each character and discard if the category starts with P or S.
    # P is punctuation, S is symbols
    mystring = u''.join(ch for ch in mystring if not unicodedata.category(ch).startswith(('P', 'S')))
    return mystring.lower()


def n_word_count(mytext, upto=1):
    words = mytext.split()
    word_list = words[:]

    for n in range(2, upto+1):
        add_to_list = [' '.join(words[i:i+n]) for i in range(0, len(words)) if i+n <= len(words)]
        # print add_to_list
        word_list = word_list + add_to_list
    return pd.DataFrame(Counter(word_list).most_common(), columns=['Word', 'Frequency'])


def main():
    file_name = "assign6.sample.txt"        #Expect file in same directory
    data = read_text_file(file_name)
    data = clean_text(data)
    wordcount = n_word_count(data, 3)
    print wordcount
    ggplot(aes(y='Frequency'), data=wordcount) + geom_point()


if __name__ == "__main__":
    main()