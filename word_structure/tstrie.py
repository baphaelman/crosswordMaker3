# Ternary Search Tree
class TSTNode:
    def __init__(self, char):
        self.char = char
        self.left = None
        self.middle = None
        self.right = None
        self.is_end = False
    
class TSTrie:
    def __init__(self):
        self.root = None
    
    def insert(self, word):
        self.root = self.insert_helper(self.root, word, 0)
    
    def insert_helper(self, node, word, index):
        letter = word[index]
        if node is None:
            node = TSTNode(letter)
        
        if letter < node.char:
            node.left = self.insert_helper(node.left, word, index)
        elif letter > node.char:
            node.right = self.insert_helper(node.right, word, index)
        else: # next character
            if index + 1 < len(word):
                node.middle = self.insert_helper(node.middle, word, index + 1)
            else:
                node.is_end = True
        return node
    
    def search(self, word):
        return self.search_helper(self.root, word, 0)
    
    def search_helper(self, node, word, index):
        if node is None:
            return False
        letter = word[index]
        
        if letter < node.char:
            return self.search_helper(node.left, word, index)
        elif letter > node.char:
            return self.search_helper(node.right, word, index)
        else: # next character
            if index + 1 < len(word):
                return self.search_helper(node.middle, word, index + 1)
            else:
                return node.is_end
    
    def wildcard_search(self, pattern):
        results = []
        self.wildcard_search_helper(self.root, pattern, 0, "", results)
        return results
    
    def wildcard_search_helper(self, node, pattern, index, current_word, results):
        if node is None:
            return

        letter = pattern[index]
        if letter == '_':
            if node.left:
                self.wildcard_search_helper(node.left, pattern, index, current_word, results)
            self.wildcard_search_helper_middle(node, pattern, index, current_word, results)
            if node.right:
                self.wildcard_search_helper(node.right, pattern, index, current_word, results)
        elif letter < node.char:
            self.wildcard_search_helper(node.left, pattern, index, current_word, results)
        elif letter > node.char:
            self.wildcard_search_helper(node.right, pattern, index, current_word, results)
        else:
            self.wildcard_search_helper_middle(node, pattern, index, current_word, results)

    def wildcard_search_helper_middle(self, node, pattern, index, current_word, results):
        if index + 1 < len(pattern):
            self.wildcard_search_helper(node.middle, pattern, index + 1, current_word + node.char, results)
        elif index == len(pattern) - 1 and node.is_end:
            results.append(current_word + node.char)

def gpt_test():
    tst = TSTrie()
    words = ["cat", "car", "bat", "bar", "cart", "cap", 'cut']
    for word in words:
        tst.insert(word)

    print(tst.search("car"))  # True
    print(tst.search("can"))  # False
    print(tst.wildcard_search("c_t"))  # ['cat', 'cut'] (assuming 'cut' was added as an example)
    print(tst.wildcard_search("_a_"))  # ['bat', 'bar', 'cat', 'car', 'cap']

if __name__ == '__main__':
    gpt_test()