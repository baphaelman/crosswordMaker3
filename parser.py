from word_structure.tstrie import TSTrie
word_bank = TSTrie()

with open('30k.txt', 'r') as file:
    for line in file:
        word = line.strip()
        word_bank.insert(word)