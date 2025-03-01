class TrieNode:
    def __init__(self):
        self.children = [None] * 26
        self.isLeaf = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for letter in word:
            index = ord(letter) - ord('a')
            if not node.children[index]:
                node.children[index] = TrieNode()
            node = node.children[index]
        node.isLeaf = True
    
    def search(self, word):
        node = self.root
        for letter in word:
            index = ord(letter) - ord('a')
            if not node.children[index]:
                return False
            node = node.children[index]
        return node.isLeaf
    
    def search_prefix(self, word):
        node = self.root
        for letter in word:
            index = ord(letter) - ord('a')
            if not node.children[index]:
                return False
            node = node.children[index]
        return True


if __name__ == "__main__":
    from parser import common_words
    t = Trie()
    for word in common_words:
        t.insert(word)
    
    