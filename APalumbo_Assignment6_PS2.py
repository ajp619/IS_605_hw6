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


def read_text_file(file_name):
    # Read in a text file. Assume utf-8 encoding
    with codecs.open(file_name, mode='r', encoding='utf-8') as myfile:
        return myfile.read().replace('\n', ' ')


def clean_text(mystring):
    # Check unicode category for each character and discard if the category starts with P or S.
    # P is punctuation, S is symbols
    mystring = u''.join(ch for ch in mystring if not unicodedata.category(ch).startswith(('P', 'S')))
    return mystring.lower()


def word_combos(word_list, combo_length):
    # Helper function to construct the ngrams
    return [' '.join(word_list[i:i+combo_length]) for i in range(len(word_list)) if i+combo_length <= len(word_list)]


def n_word_count(mytext, upto=1):
    # Break the text up into words. Expects clean text.
    words = mytext.split()

    # Summarize in a dictionary. key = ngram, value = another dictionary
    #       nested dictionary contains two keys, word_counts and total_words
    #           word_counts is a dictionary containing total occurrences for each word combo found
    #           total_words is a count of all word combos
    summary = {}
    for n in range(1, upto+1):
        add_to_list = word_combos(words, n)
        summary[n] = dict(word_counts={w:f for w,f in Counter(add_to_list).most_common()},
                          total_words=len(add_to_list))
    return summary


def get_input(n):
    # Get phrase from user. Return to quit. Limit to n words.
    # Clean user input so that it is lowercase and has no punctuation
    while True:
        input_phrase = raw_input('\nEnter up to a {0} word combination\nReturn to quit:'.format(n))
        input_list = clean_text(input_phrase.decode('utf-8')).split()
        if 0 <= len(input_list) <= n:
            return ' '.join(input_list)
        print 'Too many words'


def ngram_summary(input_value, summary):
    try:
        ngram = len(input_value.split())
        # summary[ngram] is a dict with key 'word_counts' which is a dict. lookup input_value here.
        occur = summary[ngram]['word_counts'][input_value]
        total_words = summary[ngram]['total_words']
        print "'{0}' \noccurred {2} times out of {3} total combinations of {4} words " \
              "for a probability of {1:.4f}".format(input_value,
                                                    float(occur)/float(total_words),
                                                    occur,
                                                    total_words,
                                                    ngram)
    except KeyError:
        if len(input_value) != 0:
            print '{0} does not exist in the text\n'.format(input_value)


def process_input(summary, n):
    # Process user input. Quit if no input.
    input_value = ' '
    while len(input_value) != 0:
        # Get input
        input_value = get_input(n)

        # Split input into words
        input_list = input_value.split()

        # Generate interrogation list
        entry_list = input_list[:]
        nwords = len(input_list)
        for i in range(2, nwords+1):
            entry_list = entry_list + word_combos(input_list, i)

        # Summarize for each entry
        for entry in entry_list:
            ngram_summary(entry, summary)


def main():
    file_name = "assign6.sample.txt"        # Expect file in same directory
    data = read_text_file(file_name)
    data = clean_text(data)
    n = 4
    # Create summary
    wordcount = n_word_count(data, n)

    # Let user interrogate summary
    process_input(wordcount, n)


if __name__ == "__main__":
    main()