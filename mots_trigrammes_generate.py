# -*- coding: utf-8 -*-
"""
Generates word from trigramm transition matrix stored in a binary file
Checks whether the word already exists
"""

import numpy as np
from numpy.random import choice
import codecs

# Build a dictionary to check whether word already exists
filepath = "names.txt"
dictionary = []
with codecs.open(filepath, "r", "utf-8") as lines:
    for line in lines:
        dictionary.append(line[:-1])

# Load the trigram count matrix and normalize it (to be used as probability)
count = np.fromfile("count.bin", dtype="int32").reshape(256, 256, 256)
s = count.sum(axis=2)
st = np.tile(s.T, (256, 1, 1)).T
markov_chain = count.astype('float') / st
markov_chain[np.isnan(markov_chain)] = 0

# Build words
outfile = "output.txt"
f = codecs.open(outfile, "w", "utf-8")

# How many words for each target size
nb_words = 100
for word_size in range(4, 11):
    generated_words = 0
    while generated_words < nb_words:
        i = 0
        j = 0
        unicode_word = u''
        while not j == 10:
            unicode_code = choice(range(256), 1, p=markov_chain[i, j, :])[0]
            unicode_word = unicode_word + chr(unicode_code)
            i = j
            j = unicode_code
        if len(unicode_word) == 1 + word_size:
            # if the word exists in the dictionary, suffix it by *
            if unicode_word[:-1] in dictionary:
                x = unicode_word[:-1] + "*"
            else:
                x = unicode_word[:-1]
            generated_words += 1
            print(x)
            f.write(x + "\n")
f.close()
