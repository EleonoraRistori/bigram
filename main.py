import string

from joblib import Parallel, delayed
import numpy as np
import time
import csv



class NGramCounter:
    def __init__(self, length):
        self.nGramLength = length
        self.map = {}

    def extractNGramsFromWord(self, word):
        ngrams = []
        for i in range(0, len(word) - self.nGramLength + 1):
            ngrams.append(word[i:self.nGramLength + i])
        return ngrams

    def countNGrams(self, words):
        self.map = {}
        for word in words:
            if len(word) > self.nGramLength:
                ngrams = self.extractNGramsFromWord(word)
                for ngram in ngrams:
                    if ngram in self.map:
                        self.map[ngram] = self.map[ngram] + 1
                    else:
                        self.map[ngram] = 1

    def threadCountNgrams(self, words):
        map = {}
        for word in words:
            if len(word) > self.nGramLength:
                ngrams = self.extractNGramsFromWord(word)
                for ngram in ngrams:
                    if ngram in map:
                        map[ngram] = map[ngram] + 1
                    else:
                        map[ngram] = 1
        return map

    def parallelCountNGrams(self, words, n_jobs, window_size):
        slices = [slice(start, start + window_size)
          for start in range(0, len(words) - window_size+1, window_size)]
        slices.append(slice(len(words) - len(words) % window_size, len(words)))
        result = Parallel(n_jobs=n_jobs)(delayed(nGramCounter.threadCountNgrams)(words[sl]) for sl in slices)
        self.map = {}
        for i in range(len(result)):
            for ngram in result[i]:
                if ngram in self.map:
                    self.map[ngram] = self.map[ngram] + result[i][ngram]
                else:
                    self.map[ngram] = result[i][ngram]


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


if __name__ == '__main__':
    #words = read_book_n_times("./Text/Text.txt", 30)
    print("finito lettura")
    nGramCounter = NGramCounter(3)

    # n_jobs = 6

    # with open('window_size.csv', 'w', newline='') as file:
    #     writer = csv.writer(file)
    #     for i in range(len(words), 0, -len(words)//50):
    #         print(i)
    #         tic = time.time()
    #         nGramCounter.parallelCountNGrams(words, n_jobs, i)
    #         toc = time.time()
    #         writer.writerow([i, "{:.6f}".format(toc - tic)])



    # with open('n_jobs.csv', 'w', newline='') as file:
    #     writer = csv.writer(file)
    #     for n_jobs in range(1, 24):
    #         print(n_jobs)
    #         tic = time.time()
    #         nGramCounter.parallelCountNGrams(words, n_jobs, 644131)
    #         toc = time.time()
    #         writer.writerow([n_jobs, "{:.6f}".format(toc - tic)])

    n_jobs = 6
    with open('n_book.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for n in range(1, 20):
            words = read_book_n_times("./Text/Text.txt", n*5)
            print(n)
            tic = time.time()
            nGramCounter.parallelCountNGrams(words, n_jobs, 644131)
            toc = time.time()
            writer.writerow([n*5, "{:.6f}".format(toc - tic)])

    with open('n_book_sequential.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for n in range(1, 20):
            words = read_book_n_times("./Text/Text.txt", n*5)
            print(n)
            tic = time.time()
            nGramCounter.countNGrams(words)
            toc = time.time()
            writer.writerow([n*5, "{:.6f}".format(toc - tic)])
