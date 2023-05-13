import NGramCounter
import utilities
import time
import csv


if __name__ == '__main__':
    words = utilities.read_book_n_times("./Text/Text.txt", 10)
    print("finito lettura")
    nGramCounter = NGramCounter.NGramCounter(3)

    n_jobs = 6

    with open('window_size.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for i in range(1000, 0, -1000):
            print(i)
            tic = time.time()
            nGramCounter.parallelCountNGrams(words, n_jobs, i)
            toc = time.time()
            print("{:.6f}".format(toc - tic))
            writer.writerow([i, "{:.6f}".format(toc - tic)])



    # with open('n_jobs.csv', 'w', newline='') as file:
    #     writer = csv.writer(file)
    #     for n_jobs in range(1, 24):
    #         print(n_jobs)
    #         tic = time.time()
    #         nGramCounter.parallelCountNGrams(words, n_jobs, 644131)
    #         toc = time.time()
    #         writer.writerow([n_jobs, "{:.6f}".format(toc - tic)])

    # n_jobs = 6
    # with open('n_book.csv', 'w', newline='') as file:
    #     writer = csv.writer(file)
    #     for n in range(1, 20):
    #         words = read_book_n_times("./Text/Text.txt", n*5)
    #         print(n)
    #         tic = time.time()
    #         nGramCounter.parallelCountNGrams(words, n_jobs, 644131)
    #         toc = time.time()
    #         writer.writerow([n*5, "{:.6f}".format(toc - tic)])
    #
    # with open('n_book_sequential.csv', 'w', newline='') as file:
    #     writer = csv.writer(file)
    #     for n in range(1, 20):
    #         words = read_book_n_times("./Text/Text.txt", n*5)
    #         print(n)
    #         tic = time.time()
    #         nGramCounter.countNGrams(words)
    #         toc = time.time()
    #         writer.writerow([n*5, "{:.6f}".format(toc - tic)])
