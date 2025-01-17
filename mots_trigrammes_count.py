# -*- coding: utf-8 -*-

# Count the occurrence of ASCII characters trigrams in a text file

import os
import numpy as np

import codecs


def run():
    filepath = "names.txt"

    count = np.zeros((256, 256, 256), dtype='int32')
    res = []

    with codecs.open(filepath, "r", "utf-8") as lines:
        for line in lines:
            line: str
            if line.startswith("#"):
                continue
            i = 0
            j = 0
            for k in [ord(c) for c in list(line)]:
                count[i, j, k] += 1
                i = j
                j = k
    count.tofile("count.bin")


if __name__ == '__main__':
    run()
