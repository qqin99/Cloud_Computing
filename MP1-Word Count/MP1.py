import random
import os
import re
import string
import sys

stopWordsList = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours",
                 "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its",
                 "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this",
                 "that",
                 "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
                 "having",
                 "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until",
                 "while",
                 "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before",
                 "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under",
                 "again",
                 "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both",
                 "each",
                 "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so",
                 "than",
                 "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]

delimiters = " \t,;.?!-:@[](){}_*/"
delimiterRegex = re.compile("[\\t,;.:?!\\-@\\[\\](){}_*/]")


def getIndexes(seed):
    random.seed(seed)
    n = 10000
    number_of_lines = 50000
    ret = []
    for i in range(0, n):
        ret.append(random.randint(0, 50000 - 1))
    return ret


def process(userID):
    indexes = getIndexes(userID)
    ret = []
    # TODO
    # read in line
    cnt = 0
    list_words = []
    dict = {}

    for line in sys.stdin:
        #  this needs to add \\n
        parts = re.split('[\\t,;.:?!\\-@\\[\\](){}_*/\\n]', line.lower())
        # parts = line.lower().split(delimiters)
        # parts = delimiterRegex.split(line.lower().strip('\n').strip())  #this works
        results = list(filter(None, parts))
        filtered = [x for x in results if x not in stopWordsList]
        list_words.append(filtered)

    for i in indexes:
        for word in list_words[i]:
            # if word in dict:
            #     dict[word] += 1
            # else:
            #     dict[word] = 1
            dict[word] = dict.get(word, 0) + 1

    # top_20 = sorted(dict.iteritems(), key=lambda (k, v): v, reverse=True)[:20]
    # for k, v in top_20:
    #     print(k)
    # freq_list = sorted(dict, key=dict.get)
    # freq_list.reverse()
    #
    # cnt = 0
    # for word in freq_list:
    #     cnt += 1
    #     print(word)
    #     if cnt == 20:
    #         break

    # add first 20 of sorted list to ret
    index = 0
    # follow the lexicographical order if two words have the same frequency.
    for x in sorted(dict.items(), key=lambda x: (-x[1], x[0])):
        if index <= 19:
            ret.append(x[0])
            index += 1
        else:
            break

    for word in ret:
        print(word)


# Command line args are in sys.argv[1], sys.argv[2] ..36
# sys.argv[1] contains the first command line argument passed to your script.
# sys.argv[0] is the script name itself and can be ignored
process(sys.argv[1])
