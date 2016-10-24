#!/usr/bin/env python
import collections, operator, re, string, sys

words = dict()
total_words = 0
regex = re.compile("[%s]" % re.escape(string.punctuation))

def addword(word):
    global words, total_words

    total_words += 1
    if word in words:
        words[word] += 1
    else:
        words[word] = 1

def main():
    if (len(sys.argv) != 2):
        print("Usage: %s filename" % sys.argv[0])
        sys.exit(1)

    filename = sys.argv[1]
    global words, total_words
    with open(filename, "r") as f:
        for line in f:
            for word in line.split():
                word = regex.sub("", word)
                addword(word.lower())

    print("Total Unique Words: %d\nTotal Words: %d" % (len(words), total_words))
    words = collections.OrderedDict(sorted(words.items(),
                                           key=operator.itemgetter(1),
                                           reverse=True))
    for word in words:
        if (len(word) > 4):
            print("%s: %d" % (word, words[word]))

if __name__ == "__main__":
  main()
