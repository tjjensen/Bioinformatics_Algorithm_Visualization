import collections

class DictionaryTrie():

    def __init__(self, alphabet, lexicon):
        self.alphabet = alphabet
        self.lexicon = lexicon  
    
        self.index_map = dict((v,i) for i,v in enumerate(alphabet))
        self.node_list = list()
    
        root = TrieNode(None, False, '', len(self.alphabet))
        self.node_list.append(root)
        for word in lexicon:
            self.addWordQuick(word)
        self.setFailureTransitions()
        self.initialViz()

    def addWordQuick(self, word):
        current_index = 0
        next_index = 0
        for c in word:
            next_index = self.node_list[current_index].children[self.index_map[c]]
            if next_index is not None:
                current_index = next_index
                continue
            next_node = TrieNode(current_index, False, c, len(self.alphabet))
            self.node_list.append(next_node)
            next_index = len(self.node_list) - 1
            self.node_list[current_index].children[self.index_map[c]] = next_index
            current_index = next_index
        self.node_list[current_index].terminal = True

    def getPrefix(self, index):
        prefix = ''
        while self.node_list[index].parent is not None:
            prefix += self.node_list[index].previous_edge
            index = self.node_list[index].parent
        return prefix[::-1]

    def setFailureTransitions(self):

        queue = collections.deque()
    
        queue.append(0)
    
        map1 = dict()
    
        map1[self.getPrefix(0)] = 0
    
        while len(queue):
            current_node = queue.popleft()
            for child in self.node_list[current_node].children:
                if child is not None:
                    queue.append(child)
            current_word = self.getPrefix(current_node)
            for i in range(1,len(current_word)):
                try:
                    map1[current_word[i:]]
                except KeyError:
                    continue
                self.node_list[current_node].failure = self.getIndexOfWord(current_word[i:])
                break
            map1[self.getPrefix(current_node)] = current_node 
        self.node_list[0].failure = None



    def setFailure(self, index):
        current_word = self.getPrefix(index)

        for i in range(1, len(current_word)):
            suffix_index = self.getIndexOfWord(current_word[i:])
            if suffix_index:
                self.node_list[index].failure = suffix_index
                return suffix_index

    def getIndexOfWord(self, word):
        current_index = 0
        next_index = 0

        for c in word:
            next_index = self.node_list[current_index].children[self.index_map[c]]
            if next_index is None:
                return False
            current_index = next_index
        return current_index

    def dictionaryMatch(self, database):
        match_indices = list()
        startOfString = 0
        endOfString = 0
        currentNode = 0
        while endOfString < len(database):
            currentCharIndex = self.index_map[database[endOfString]]
            nextNode = self.node_list[currentNode].children[currentCharIndex]
            if nextNode is not None:
                currentNode = nextNode
                endOfString += 1
                if self.node_list[currentNode].terminal:
                    match_indices.append((startOfString, database[startOfString : endOfString]))
            elif currentNode == 0:
                endOfString += 1
                startOfString = endOfString
            else:
                currentNode = self.node_list[currentNode].failure
                startOfString = endOfString - len(self.getPrefix(currentNode))
                if self.node_list[currentNode].terminal:
                    match_indices.append((startOfString, database[startOfString : endOfString]))
        return match_indices

    def stepwiseMatch(self, database, match_indices, startOfString, endOfString, currentNode):
        currentCharIndex = self.index_map[database[endOfString]]
        nextNode = self.node_list[currentNode].children[currentCharIndex]
        if nextNode is not None:
            currentNode = nextNode
            endOfString += 1
            if self.node_list[currentNode].terminal:
                match_indices.append((startOfString, database[startOfString : endOfString]))
        elif currentNode == 0:
            endOfString += 1
            startOfString = endOfString
        else:
            currentNode = self.node_list[currentNode].failure
            startOfString = endOfString - len(self.getPrefix(currentNode))
            if self.node_list[currentNode].terminal:
                match_indices.append((startOfString, database[startOfString : endOfString]))
        return (startOfString, endOfString, currentNode)

    def getAllStepwise(self, database):
        match_indices = list()
        startOfString = 0
        endOfString = 0
        currentNode = 0
        steps = list()
        steps.append((startOfString, endOfString, currentNode, list(match_indices)))
        while endOfString < len(database):
            (startOfString, endOfString, currentNode) = self.stepwiseMatch(
                    database, match_indices, startOfString, endOfString, currentNode)
            steps.append((startOfString, endOfString, currentNode, list(match_indices)))
        return steps



    def initialViz(self):
        edges = list()
        back_edges = list()
        for i in range(len(self.node_list)):
            current_node = self.node_list[i]
            for child in current_node.children:
                if child is not None:
                    edges.append((i, child))
            if current_node.failure is not None:
                back_edges.append((i, current_node.failure))
        self.edges = edges
        self.back_edges = back_edges

    def __str__(self):
        return_str = ''
        for node in self.node_list:
            return_str += '{0}\n'.format(str(node))
        return return_str

class TrieNode():

    def __init__(self, parent, terminal, previous_edge, number_of_children):
        self.parent = parent
        self.terminal = terminal
        self.previous_edge = previous_edge
        self.failure= 0
        self.children = [None] * number_of_children

    def __str__(self):
        return '\nParent Index:{0}\nTerminality:{1}\nFailure Index:{2}\nPrevious Edge:{3}\nChildren:{4}'.format(
                str(self.parent), str(self.terminal), str(self.failure), str(self.previous_edge), str(self.children))


def main():
    alpha = ['A', 'C', 'G', 'T']
    lexicon = ['ACCGT', 'CGT', 'TGA', 'TGT', 'T', 'TG']
    trie = DictionaryTrie(alpha, lexicon)
    for word in lexicon:
        trie.addWordQuick(word)
    trie.setFailureTransitions()
    # for i in range(len(trie.node_list)):
    #    trie.setFailure(i)
    print trie

    print trie.dictionaryMatch('ACCGTGA')
    
    trie.initialViz()
    print trie.edges
    print trie.back_edges

    match_indices = list()
    startOfString = 0
    endOfString = 0
    currentNode = 0
    database = 'ACCGTGA'
    while endOfString < len(database):
        (startOfString, endOfString, currentNode) = trie.stepwiseMatch(database, match_indices, startOfString, endOfString, currentNode)
        print startOfString
        print endOfString
        print currentNode
    print match_indices


if __name__ == '__main__':
    main()      