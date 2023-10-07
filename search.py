from collections import deque

from assets import load_board, load_boosts, load_dictionary, letter_values

# load in dictionary and redundant starters cache
dictionary = load_dictionary()
dictionary_caches = []

board = load_board()
board_boosts = load_boosts()

class SearchNode:
    def __init__(self, parent, x, y):
        self.parent = parent
        self.x = x
        self.y = y

    def letter(self):
        return board[self.y][self.x]

    def word(self):
        word = ""
        curr = self
        while True:
            word = curr.letter() + word
            if curr.parent is None:
                break
            else:
                curr = curr.parent
        return word
    
    def score(self):
        score = 0
        curr = self

        doubleWordScore = False
        while True:
            letter_multiplier = 1
            for doubleLetterBoost in board_boosts["+"]:
                if doubleLetterBoost[0] == curr.x and doubleLetterBoost[1] == curr.y:
                    letter_multiplier = 2
                    break
            for tripleLetterBoost in board_boosts["*"]:
                if tripleLetterBoost[0] == curr.x and tripleLetterBoost[1] == curr.y:
                    letter_multiplier = 3
                    break
            if not doubleWordScore:
                for doubleWordBoost in board_boosts["$"]:
                    if doubleWordBoost[0] == curr.x and doubleWordBoost[1] == curr.y:
                        doubleWordScore = True
                        break

            score += letter_values[curr.letter()] * letter_multiplier

            if curr.parent is None:
                break
            else:
                curr = curr.parent

        if doubleWordScore:
            score *= 2
        
        if len(self.word()) >= 6:
            score += 10

        return score

    def adjacent_nodes(self):
        adjacent = []
        adjacent.append(SearchNode(self, self.x, self.y - 1))
        adjacent.append(SearchNode(self, self.x + 1, self.y - 1))
        adjacent.append(SearchNode(self, self.x + 1, self.y))
        adjacent.append(SearchNode(self, self.x + 1, self.y + 1))
        adjacent.append(SearchNode(self, self.x, self.y + 1))
        adjacent.append(SearchNode(self, self.x - 1, self.y + 1))
        adjacent.append(SearchNode(self, self.x - 1, self.y))
        adjacent.append(SearchNode(self, self.x - 1, self.y - 1))

        valid_adjacent = []
        for node in adjacent:
            if node.x >= 0 and node.x < 5 and node.y >= 0 and node.y < 5:
                valid_adjacent.append(node)

        return valid_adjacent

    def chain_contains(self, target_node):
        curr = self
        while True:
            if curr.x == target_node.x and curr.y == target_node.y:
                return True
            elif curr.parent is None:
                return False
            else:
                curr = curr.parent


def search_from_node(root_node, depth):
    words = deque()

    frontier = deque()
    frontier.appendleft(root_node)

    while len(frontier) > 0:
        curr = frontier.pop()

        # if current branch is a word log its frontal node
        candidate_word = curr.word()
        if candidate_word in dictionary:
            words.appendleft(curr)

        # if maximum search depth reached, terminate search
        if len(candidate_word) > depth:
            break

        # queue adjacent nodes that are not in current's parent chain
        usefulBranch = True
        for i in range(2, depth):
            if len(candidate_word) < i:
                break
            if candidate_word[:i] not in dictionary_caches[i - 2]:
                usefulBranch = False
                break

        if usefulBranch:
            for adjacent_node in curr.adjacent_nodes():
                if not curr.chain_contains(adjacent_node):
                    frontier.appendleft(adjacent_node)

    return list(words)

def search_board(depth):
    global dictionary_caches
    dictionary_caches = [load_dictionary(x) for x in range(2, depth)]

    words = []
    for y in range(5):
        for x in range(5):
            print(f"Searching from root node at ({x}, {y})...")
            words += search_from_node(SearchNode(None, x, y), depth)
    return words