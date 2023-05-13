import numpy as np
import string


def read_text(fileName):
    words = []
    with open(fileName, encoding='utf-8') as file:
        for line in file:
            for word in line.split():
                word = word.translate(str.maketrans('', '', string.punctuation))
                words.append(word)

    return words


def read_book_n_times(fileName, n):
    words = []
    text_words = read_text(fileName)
    for i in range(n):
        #print(i)
        words = np.append(words, text_words)
    return words
