from joblib import Parallel, delayed


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
        result = Parallel(n_jobs=n_jobs)(delayed(self.threadCountNgrams)(words[sl]) for sl in slices)
        self.map = {}
        for i in range(len(result)):
            for ngram in result[i]:
                if ngram in self.map:
                    self.map[ngram] = self.map[ngram] + result[i][ngram]
                else:
                    self.map[ngram] = result[i][ngram]


