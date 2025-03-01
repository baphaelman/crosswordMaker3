import time
from parser import common_words
from word_structure.tstrie import TSTrie
from word_structure.trie import Trie

# insertion
def trie_insertion_test():
    for len in common_words:
        for word in common_words[len]:
            t.insert(word)

def tst_insertion_test():
    for len in common_words:
        for word in common_words[len]:
            tst.insert(word)


t = Trie()
tst = TSTrie()
print("INSERTION:")

start_time = time.time()
trie_insertion_test()
print("Trie: --- %s seconds ---" % (time.time() - start_time))

start_time = time.time()
tst_insertion_test()
print("TST: --- %s seconds ---" % (time.time() - start_time))
print()

# BASIC SEARCHING
search_words = ['sonorant', 'sleepy', 'pompousness', 'callously', 'indignant', 'hi', 'nasa', 'discography']
def trie_search_test():
    result = []
    for word in search_words:
        result.append(t.search(word))
    print(result)

def tst_search_test():
    result = []
    for word in search_words:
        result.append(tst.search(word))
    print(result)

print("BASIC SEARCH:")
start_time = time.time()
trie_search_test()
print("Trie: --- %s seconds ---" % (time.time() - start_time))

start_time = time.time()
tst_search_test()
print("TST: --- %s seconds ---" % (time.time() - start_time))
print()