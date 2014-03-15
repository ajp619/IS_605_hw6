__author__ = 'Aaron'
import collections

words = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
word_list = words[:]
upto = 1


for n in range(2, upto+1):
    add_to_list = [' '.join(words[i:i+n]) for i in range(0, len(words)) if i+n <= len(words)]
    print add_to_list
    word_list = word_list + add_to_list

print words
print word_list
print collections.Counter(word_list).most_common()